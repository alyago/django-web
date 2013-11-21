"""Handle sending emails and retrieving resumes for SimplyApply."""

import logging
import mimetypes
import smtplib
from cStringIO import StringIO
from email import encoders as Encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from django.db.models import F

import resume.models as models
import resume.jbb_models as jbb
from resume.services.pdf import generate_pdf
from resume.services.sponsorship import decode_cparm

logger = logging.getLogger('resume')

EMAIL_BODY = u"""Greetings,

{job_company} has a new application for:
Title: {job_title}
Location: {job_location}

==============================================================

Name: {first_name} {last_name}
Email: {email}
Message: {message}

==============================================================


This job application was brought to you by {source}.
"""

def get_pdf_resume(resume):
    """Get the PDF."""
    attachment = {'mimetype': 'application/pdf'}
    content = models.Content.objects.get(resume=resume.id)

    if not content.pdf:
        content.pdf = generate_pdf(resume, StringIO()).getvalue().decode('latin-1').encode('utf-8')
        content.save()

    attachment['raw_resume'] = content.pdf
    if content.file_name:
        attachment['filename'] = content.file_name.rsplit('.', 1)[0] + '.pdf'
    else:
        _filename = []
        if resume.contact.first_name:
            # Remove non filename chars.
            _filename.append(
                ''.join([c for c in resume.contact.first_name if c.isalpha()]))
        if resume.contact.last_name:
            _filename.append(
                ''.join([c for c in resume.contact.last_name if c.isalpha()]))

        attachment['filename'] = '_'.join(_filename) + '.pdf'

    return attachment

def simplyapply(request, job, resume, mobile=False):
    """Handles both JBB and regular job applies."""
    apply_info = get_apply_info(request)
    if not apply_info['email']:
        if resume.contact and resume.contact.email:
            apply_info['email'] = resume.contact.email
        else:
            apply_info['email'] = 'Not Provided'

    apply_info['job_company'] = job.company
    apply_info['job_title'] = job.title
    apply_info['job_location'] = job.location
    apply_info['source'] = job.source if hasattr(job, '_jobpost') else 'Simply Hired' # JBB/Publishers get a different source in the email.

    if resume.source == 'Linkedin':
        attachment = get_pdf_resume(resume)
    else:
        # TODO: handle the case where the resume has no content entry.
        content = models.Content.objects.get(resume=resume.id)
        attachment = {}
        mimetypes.init()
        attachment['mimetype'] = mimetypes.guess_type(content.file_name)
        try:
            attachment['raw_resume'] = content.raw_resume.decode('utf-8').encode('latin-1')
        except UnicodeDecodeError:
            attachment['raw_resume'] = content.raw_resume
        attachment['filename'] = content.file_name

    subject = u"Application for {0} at {1}".format(job.title, job.company)
    send_email('Simply Hired <noreply@simplyhired.com>', job.apply_email, subject, EMAIL_BODY.format(**apply_info), attachment,
               reply_to=resume.contact.email if resume.contact.email else None)

    try:
        # JBB job.
        if hasattr(job, '_jobpost'):
            jbb.JobPostMetrics.objects.filter(jobpostid=job._jobpost.jobpostid).update(count_apply_email=F('count_apply_email')+1)

        # Log for generic tracking.
        log_apply(request, job, apply_info, attachment, resume, mobile)
    except Exception, msg:
        logger.exception('Error in writing to tracking: %s %s' % (Exception, msg))

    if resume.contact.email:
        send_confirmation(resume.contact.email, apply_info)

    return

def send_confirmation(send_to, apply_info):
    """Send the applicant a confirmation email."""
    msg = """Hello,

This is a friendly confirmation for your Simply Apply application for position '{job_title}' at {job_company}.

Thank you,
The Simply Hired Team""".format(**apply_info)

    send_email('Simply Apply <noreply@simplyhired.com>', send_to, 'Simply Apply Confirmation', msg)

def log_apply(request, job, apply_info, attachment, resume, mobile):
    cparm = request.session.get(job.key) or {}
    if cparm:
        try:
            cparm = decode_cparm(cparm.get('cparm'))
            assert isinstance(cparm, dict)
        except AssertionError:
            pass
        finally:
            del request.session[job.key]

    models.ApplyTracking(
        user_id=resume.user,
        user_email=apply_info['email'] if apply_info['email'] != 'Not Provided' else '',
        apply_source='mobile' if mobile else 'web',
        user_agent=request.META['HTTP_USER_AGENT'],
        resume_type=resume.source,
        filename=attachment['filename'],
        refind_key=job.refindkey,
        job_title=job.title,
        employer=job.company,
        job_location=job.location,
        cpc=cparm.get('cpc'),
        search_position=cparm.get('pos'),
        advertiser_id=cparm.get('a_id'),
        campaign_id=cparm.get('c_id'),
        resume=resume,
    ).save()

    return

def get_apply_info(request):
    """Get the applicant's apply information from a request object."""
    apply_info = {}
    apply_info['first_name'] = request.POST.get('first_name')
    apply_info['last_name'] = request.POST.get('last_name')
    apply_info['email'] = request.POST.get('email')
    apply_info['message'] = request.POST.get('message') if request.POST.get('message') else 'No Message Provided'

    return apply_info

def send_email(send_from, send_to, subject, body, attachment=None, server='localhost', reply_to=None):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    if reply_to:
        msg.add_header('reply-to', reply_to)

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    if attachment:
        part = MIMEBase('application', attachment['mimetype'])
        part.set_payload(attachment['raw_resume'])
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', u'attachment; filename="{0}"'.format(attachment['filename']))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

    return
