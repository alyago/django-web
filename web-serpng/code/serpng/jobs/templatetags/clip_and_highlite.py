# Copyright (c) 2013, Simply Hired, Inc. All rights reserved
"""
Clips and Highlites

The clipping algorithm works in 3 parts:

    1: Process keywords
        - In this step we split keywords based on spaces. Then remove extranious characters
    2: Locate Keywords
        - We iterate through the list of keywords storing the location we found each keyword
        - We then sort the 'found array (foundloc)' based on the location we found.
        - We also merge found locations together in case a part of a keyword is a substring
            of antoher. ie. sign design
    3: Choose Window
        - Finally we take our window (the clip size) and starting at each found location, we
            find how many keywords are within the window. We then find the 'best' and store the
            first found keyword and the position of the last character of the last keyword.
        - Because the previous step might be a very small string (if the keyword was only
            found once), we grow the window to a maximum of 1/10th the clip size, stopping at
            the first word break.

The highliting process:

    Knowing the locations of the found keywords within the window, we chop up the clipped
    string based on the keywords found within. As we are chopping, we are reassembling
    the string surrounded by <strong></strong> tags.

    The goal is to end up scanning the string only when nessesary (finding keywords).

    TODO: Perhaps its possible to find keywords in parallel. In practice, people rarely
        search for more then two keywords, so this seems to add complexity.


"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Max size of the ending clip
CLIP_SIZE = 180

# Minimum Keyword size
MIN_KEYWORD_SIZE = 3


def dedupe_keywords(keywords):
    """
    @return copy of keywords with duplicates removed.
    """

    sort_kw = sorted(keywords, key=len, reverse=True)
    good = []
    while sort_kw:
        word = sort_kw.pop()
        found = False
        for w in sort_kw:
            if word in w:
                found = True
        if not found:
            good.append(word)
    return good


def merge_locations(locations):
    """
    Merge overlapping locations together
    """

    ln = len(locations)
    if ln == 1:
        return locations

    gloc = []  # good locations
    sk = 1     # skips
    i = 0
    loc = locations[i]
    while i < ln - 1:

        nloc = locations[i+sk]     # Next location
        le = loc['l'] + loc['ks']  # le is the end of found keyword
        if le >= nloc['l'] and le <= nloc['l'] + nloc['ks']:
            # if le overlaps the next location
            # merge the two together
            loc = {
                'l': loc['l'],
                'ks': nloc['l'] + nloc['ks'] - loc['l']
            }

            # increment the number we'll skip
            sk += 1
        else:
            gloc.append(loc)
            i += sk
            sk = 1
            loc = locations[i]
        # if that was the last one, add it and quit
        if sk + i >= ln:
            gloc.append(loc)
            break

    return gloc


def process_keywords(keywords):
    """
    This method filters out bay characters and splits the keywords
    """

    for val in ["'", '"', "(", ")"]:
        keywords = keywords.replace(val, " ")
    for val in [" OR ", " NOT ", " AND "]:
        keywords = keywords.replace(val, " ")

    keywords.replace("  ", " ")

    key_array = keywords.split(" ")
    key_array = [k for k in key_array if len(k) >= MIN_KEYWORD_SIZE]

    return key_array


def find_word_breaks(start, end, bstart, bend, desc):
    """
    Expand a window in a block of text to the next word break
    Example:
        Total size is 'clip_size'
            v <-start   end-> v
    |-------|=================|---------|
    ^ ----- ^
    ^ bstart                       bend ^
    'start' and 'end' are pointers in the string calculated
        based off of the 'best' clip in the desc + some padding

    bstart: 'best start'
    bend: 'best end'
        bstart is the calulated max start to keep the ending clip at clip_size
        bend is the caluated max end to keep the ending clip at clip_size

    We want to clip at word breaks so we scan from start to bstart ending at first word break, 0 or bstart

    """

    terms = (" ", ",", ";", ":", ".")
    # find word break
    desc_size = len(desc)

    while start >= bstart and start > 0:  # needs to be >
        #local specific word break probably needed
        if desc[start] in terms:
            break
        else:
            start -= 1

    while end <= bend and end < desc_size:
        if desc[end] in terms:
            break
        else:
            end += 1

    return (start, end)


# Main Code

@register.filter()
def clip_and_highlite(desc, keywords, config=None):
    """ Run clipping and highlighting on desc """
    if config is None:
        config = {}
    try:
        return clip_and_highlite_inner(desc, keywords, True, config)
    #pylint: disable=W0703
    except Exception:
        if desc:
            return desc[:CLIP_SIZE]
        else:
            return ""


@register.filter()
def highlite(desc, keywords, config=None):
    """ Run highlighting on desc """
    if config is None:
        config = {}
    try:
        return clip_and_highlite_inner(desc, keywords, False, config)
    #pylint: disable=W0703
    except Exception:
        if desc:
            return desc[:CLIP_SIZE]
        else:
            return ""


#pylint: disable=R0912
def clip_and_highlite_inner(desc, keywords, clip=False, config=None):
    """ Clipping and highlighting internal implementaiton """
    if config is None:
        config = {}
    clip_size = config.get("clip_size", CLIP_SIZE)
    # Setup the sizes
    if not desc:
        return None
    if not keywords:
        (start, end) = find_word_breaks(0, clip_size - 10, 0, clip_size, desc)
        return desc[start:end]

    desc_size = len(desc)
    lkeywords = keywords.lower()
    lkeys = process_keywords(lkeywords)
    opt_endword = config.get("opt_endword")

    # Make this case insensitive
    lower_desc = desc.lower()

    # start the window defaulting to the first chunk. If we don't find the keyword
    # we'll just use this
    start = 0
    end = clip_size

    # Create our array of found locations. These need to be relative to the start
    # So we need to create an off-set
    foundlocs = []

    # This runs multiple searches for multple keywords
    # Maybe a way to carry information from one to the next
    for lkey in lkeys:
        off = 0
        ldesc = lower_desc
        length = len(lkey)
        a = ldesc.find(lkey)
        while a >= 0:
            off = off + a
            t_length = length

            if off == 0 or (off > 0 and not desc[off - 1].isalnum()):

                # Match the entire word, even if our keyword is only a prefix
                if opt_endword == "stem":
                    while (off + t_length <= desc_size and desc[off + t_length].isalnum()):
                        t_length += 1

                if opt_endword == "whole":
                    # In mathcing only the whole word there are two conditions we need to look for
                    # 1: That we're at the end of the description, thus at the end of a 'word'
                    # 2: That we're not at the end, and the character at the end of the match is not an
                    #    alphanumeric character
                    if off + t_length == desc_size or \
                            (off + t_length < desc_size and not desc[off + t_length].isalnum()):
                        foundlocs.append({
                            'l': off,
                            'ks': t_length
                        })
                else:
                    # ks is the key-size
                    foundlocs.append({
                        'l': off,   # l is the location where we found it
                        'ks': t_length
                    })

            off += t_length  # We're past the key, add the length
            ldesc = ldesc[a + t_length:]
            a = ldesc.find(lkey)

    if foundlocs:
        # Have to sort the array based on location
        if len(lkeys) > 1:
            foundlocs = sorted(foundlocs, key=lambda d: d['l'] + d['ks'])
            foundlocs = merge_locations(foundlocs)

        # this array keeps track of our 'best' find
        # 0 - starting location
        # 1 - ending location
        # 2 - number of matches we found in that location
        # 3 - where in the found location array we started

        best = [start, end, 0, 0]

        if len(desc) <= clip_size or not clip:
            best = [start, end, len(foundlocs), 0]
        else:
            t = 0
            while t < len(foundlocs):
                t_start = foundlocs[t]['l']  # start of our range
                t_end = 0                    # length of the range
                c = 0                        # number of keywords in range

                for loc in foundlocs[t:]:    # Now loop through remaining found locations
                    if abs((loc['l'] + loc['ks']) - t_start) < clip_size:
                        c = c + 1
                        t_end = loc['l'] + loc['ks']
                    else:
                        break
                if c > best[2]:
                    best = [t_start, t_end, c, t]
                t = t + 1

            overage = int((clip_size - (best[1] - best[0])) / 2)

            start = best[0]
            end = best[1]

            # if we found a lot of space, we need to pad before we find word break
            if overage > clip_size / 10:
                start -= int(overage / 3 * 2)
                end += int(overage / 3 * 2)

            (start, end) = find_word_breaks(start, end, best[0] - overage, best[1] + overage, desc)

            #Fix start and end if we went over
            if start < 0:
                end -= start
                start = 0
            elif end > desc_size:
                start = start + (end - desc_size)
                end = desc_size

        # Now highlite

        # Go through the locations in the winning range
        # and build a string using <strong> as the keyword
        # the goal is since we already know the locations of the
        # keywords we don't need to search for them again
        pre = desc[start:foundlocs[best[3]]['l']]

        # loop through our matches. best[2] is the number of matches we found
        for cl in range(0, best[2]):
            clt = cl + best[3]           # add array offset to our current range
            l = foundlocs[clt]['l']      # grab the locaiton from foundlocs
            ks = foundlocs[clt]['ks']    # grab the key-size

            pre += "<strong>"
            pre += desc[l:l+ks]          # cut out keyword
            pre += "</strong>"

            if cl < best[2]-1:           # if we're have another element after,
                                         # append the characters between the end of the keyword
                                         # and the next keyword
                pre += desc[l+ks:foundlocs[clt + 1]['l']]

        pre_end = best[3] + best[2] - 1
        pre += desc[(foundlocs[pre_end]['l'] + foundlocs[pre_end]['ks']):end]

        if clip:
            if start > 0:
                pre = "... " + pre
            if end < desc_size:
                pre += " ..."

        return mark_safe(pre)
    else:

        if end < desc_size:
            (start, end) = find_word_breaks(start, end - clip_size / 15, start, end - 4, desc)
            return desc[start:end] + " ..."
        else:
            return desc[start:end]
