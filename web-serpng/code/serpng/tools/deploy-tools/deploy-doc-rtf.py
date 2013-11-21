#!/usr/bin/env python

"""
 deploy-doc-rtf.py : Automatically generate our weekly deploy doc.
 NOTE! This script is very rough around the edges, still very much a WIP.
 TODO(delaney): Talk to the Google Drive API directly instead of generating a .rtf.

 Instructions on how to use can be found here:
   https://docs.google.com/a/simplyhired.com/document/d/1ntYLf8FvNYKFB7uxWmWflNFJRlYizBBiTuudmYlI48s/edit#
"""

import datetime
import getopt
import re
import requests
import sys

from PyRTF import Cell, Document, LINE, Paragraph, Renderer, Section, Table, TabPS, TEXT


# Super lame command line argument processing.
try:
    opts, args = getopt.getopt(sys.argv[1:], 'v')
except getopt.GetoptError:
    pass

# Commits to compare (default is master...integration)
commit_l = args[0] if len(args) > 0 else 'master'
commit_r = args[1] if len(args) > 1 else 'integration'

# Define a vprint function that prints if opts[-v] is set, otherwise it's a no-op.
if opts and '-v' in [o[0] for o in opts]:
    def vprint(*arg_list):
        """Verbose print. Set -v option to enable."""
        for arg in arg_list:
            print arg,
        print
else:   
    vprint = lambda *arg_list: None

# Get next Monday's date, which is the release date.
today = datetime.date.today()
monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
date = monday.strftime("%Y%m%d")

def text(string, **attrs):
    """Wrap text in a paragraph element."""
    p = Paragraph()
    p.append(TEXT(string, **attrs))
    return p

def print_row(pr, desc, reviewers, owner, bug, repo):
    """Adds a single commit result as a row in the main table."""

    link = '{\\field{\*\\fldinst{HYPERLINK "%s"}}{\\fldrslt{\ul %s}}}'

    table.AddRow(
        Cell(Paragraph(ss.ParagraphStyles.Normal, '')),
        Cell(Paragraph(ss.ParagraphStyles.Normal, str(desc))),
        Cell(Paragraph(ss.ParagraphStyles.Normal, str(repo))),
        Cell(Paragraph(ss.ParagraphStyles.Normal, str(owner))),
        Cell(Paragraph(ss.ParagraphStyles.Normal,
            str(link % ('http://bugzilla.ksjc.sh.colo/show_bug.cgi?id=' + bug, bug)) if bug else '', LINE,
            str(link % ('https://github.ksjc.sh.colo/apps-team/' + repo + '/pull/' + pr, 'pull ' + pr)), LINE,
            str(reviewers)
        )),
        Cell(Paragraph(ss.ParagraphStyles.Normal, '')),
        Cell(Paragraph(ss.ParagraphStyles.Normal, ''))
    )

def get_string(pattern, haystack, default):
    """Extract string from given haystack."""
    match = pattern.search(haystack)
    return match.group(1) if match else default

def compare_repo(repo, left, right):
    """Compare two commits in specified repo using GitHub API."""
    url = 'https://github.ksjc.sh.colo/api/v3/repos/apps-team/' + repo + '/compare/' + left + '...' + right
    vprint("compare {0} {1}...{2}".format(repo, left, right))
    headers = {'Authorization' : 'token 61609d5d659dbbe7127420745130ca77160d10fe'}
    return requests.get(url, headers=headers, verify=False).json()

def print_repo(repo, left, right):
    """Print all commits for a given repo."""
    pull_pattern = re.compile(r"Merge pull request #(\d+) from (\S+)[\r|\n]*(.*)[\r|\n]*", re.MULTILINE)
    review_pattern = re.compile(r"(r\s*=\s*[\w, ]*)", re.MULTILINE | re.IGNORECASE)
    bug_pattern = re.compile(r"(bug\D*\d+)", re.MULTILINE | re.IGNORECASE)
    submodule_pattern = re.compile(r"\-Subproject commit (\w+)\n\+Subproject commit (\w+)", re.MULTILINE)

    response_json = compare_repo(repo, left, right)
    if 'commits' not in response_json:
        return

    for commit in response_json['commits']:
        if not 'commit' in commit or not 'message' in commit['commit']:
            continue

        # Commit owner (first name only)
        owner = commit['commit']['author']['name'].partition(' ')[0]
        msg = commit['commit']['message']
        pull_match = pull_pattern.match(msg)
        if pull_match:
            (pull, branch, desc) = pull_match.groups()

            reviewers = get_string(review_pattern, msg, 'NO REVIEW?')

            # Re-purpose reviewers column to say 'HOTFIX' when branch == master.
            if branch.endswith('/master'):
                reviewers = 'HOTFIX'

            bug = get_string(bug_pattern, msg, None)
            if desc:
                desc = desc.replace(reviewers, '') if reviewers else desc
                desc = desc.replace(bug, '') if bug else desc
                desc = re.sub(r"[\(\)\-_:;]*", '', desc, 0, re.IGNORECASE)
                desc = re.sub(r"^\s*|\s*$", '', desc)
            print_row(pull, desc, reviewers, owner, bug, repo)

    # Scan for submodules.
    for file_diff in response_json['files']:
        if not 'filename' in file_diff or not 'patch' in file_diff:
            continue

        if file_diff['patch'][0:30] == "@@ -1 +1 @@\n-Subproject commit":
            submodule = file_diff['filename'][file_diff['filename'].rfind('/') + 1:]
            submodule_match = submodule_pattern.search(file_diff['patch'])
            if submodule_match:
                print_repo(submodule, submodule_match.group(1), submodule_match.group(2))

# Crate RTF document.
doc     = Document()
ss      = doc.StyleSheet
section = Section()
doc.Sections.append(section)

# Header section.
section.append(text('Release Notes', size=48))
section.append(text('Date: ' + date, size=24, bold=True))

# Main table.
table = Table(TabPS.DEFAULT_WIDTH * 2,
              TabPS.DEFAULT_WIDTH * 3,
              TabPS.DEFAULT_WIDTH * 2,
              TabPS.DEFAULT_WIDTH * 2,
              TabPS.DEFAULT_WIDTH * 2,
              TabPS.DEFAULT_WIDTH * 1,
              TabPS.DEFAULT_WIDTH * 2)

# Table header.
table.AddRow(
    Cell(text('Project Name', bold=True)),
    Cell(text('Change', bold=True)),
    Cell(text('Repo', bold=True)),
    Cell(text('Owner', bold=True)),
    Cell(text('Bug / Diffs / Reviewer', bold=True)),
    Cell(text('OK', bold=True)),
    Cell(text('Notes', bold=True))
)

# Standard deploy repos.
# TODO(delaney): Expose this via command line arguments.
print_repo('php-platform', commit_l, commit_r)
print_repo('web-serpng', commit_l, commit_r)
print_repo('incredible-bulk', commit_l, commit_r)

# Output RTF.
section.append(table)
DR = Renderer()
DR.Write(doc, file('deploy-web-' + date + '.rtf', 'w'))
