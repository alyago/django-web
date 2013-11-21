# -*- coding: utf-8 -*-

from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import StyleSheet1, ParagraphStyle

styles = StyleSheet1()

styles.add(ParagraphStyle(name='Normal', fontName='Helvetica'))
styles.add(ParagraphStyle(name='ContactName', parent=styles['Normal'], alignment=TA_CENTER, fontSize=18, spaceAfter=12))
styles.add(ParagraphStyle(name='ContactInfo', parent=styles['Normal'], alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Header', parent=styles['Normal'], fontSize=13, spaceBefore=2, spaceAfter=4))
styles.add(ParagraphStyle(name='ExperienceDate', parent=styles['Normal'], alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='Bullet',
                          parent=styles['Normal'],
                          bulletFontName = 'Symbol',
                          bulletIndent = 0,
                          bulletFontSize = 13,
                          bulletOffsetY = -1.5,
                          leftIndent = 15.8,
                          firstLineIndent = 0,))

hr = HRFlowable(width='100%', spaceBefore=4, spaceAfter=4)

def write_contact(contact):
    content = []
    if contact.first_name and contact.last_name:
        content.append(Paragraph(u'{0} {1}'.format(contact.first_name, contact.last_name), styles['ContactName']))

    if contact.address:
        address = []
        if contact.address.street:
            address.append(contact.address.street)
        if contact.address.street2:
            address.append(contact.address.street2)
        if contact.address.city:
            address.append(contact.address.city)
        if contact.address.state:
            address.append(contact.address.state)
        address = ', '.join(address)
        if contact.address.postcode:
            address += ' ' + contact.address.postcode

        content.append(Paragraph(address, styles['ContactInfo']))

    phone_number = contact.cell_phone or contact.home_phone
    if contact.email and phone_number:
        content.append(Paragraph(u'{0} | {1}'.format(contact.email, phone_number), styles['ContactInfo']))
    elif contact.email:
        content.append(Paragraph(u'{0}'.format(contact.email), styles['ContactInfo']))
    elif phone_number:
        content.append(Paragraph(u'{0}'.format(phone_number), styles['ContactInfo']))

    return content

def write_summary(summary):
    content = []

    if not summary:
        return content

    # if summary.headline:
    #     content.append(Paragraph('{0}'.format(summary.headline), styles['Header']))
    if summary.description:
        content.append(hr)
        content.append(Paragraph(u'<b>Highlights</b>', styles['Header']))
        content.append(Spacer(1, 4))
        content.append(Paragraph(u'{0}'.format(summary.description), styles['Normal']))

    return content

def write_experience(job_set):
    content = []

    if job_set.count():
        content.append(hr)
        content.append(Paragraph(u'<b>Experience</b>', styles['Header']))
        content.append(Spacer(1, 4))
        for job in job_set.iterator():
            start_date = job.start_date if job.start_date else ''
            end_date = job.end_date if job.end_date else ''

            date_range = []
            if start_date:
                if start_date.month == 1 and start_date.day == 2:
                    date_range.append(start_date.strftime('%Y'))
                else:
                    date_range.append(start_date.strftime('%B %Y'))
            if job.current:
                date_range.append(u'Present')
            elif end_date:
                if end_date.month == 1 and end_date.day == 2:
                    date_range.append(end_date.strftime('%Y'))
                else:
                    date_range.append(end_date.strftime('%B %Y'))

            job_exp = []
            if job.title:
                job_exp.append(u'<b>{0}</b>'.format(job.title))
            if job.employer:
                job_exp.append(u'<b>{0}</b>'.format(job.employer))

            data = [[
                Paragraph(u'{0}'.format(' at '.join(job_exp)), styles['Normal']), Paragraph(' - '.join(date_range), styles['ExperienceDate'])
            ]]
            table = Table(data, colWidths=[290, 178])
            content.append(table)

            if job.description:
                # Turn newlines into bulleted sentences.
                for line in job.description.split('\n'):
                    content.append(Paragraph(line, styles['Bullet'], bulletText=u'•'))

            content.append(Spacer(1, 8))

    return content

def write_education(education_set):
    content = []

    if education_set.count():
        content.append(hr)
        content.append(Paragraph(u'<b>Education</b>', styles['Header']))
        content.append(Spacer(1, 4))
        for education in education_set.iterator():
            start_date = education.start_date if education.start_date else ''
            end_date = education.end_date if education.end_date else ''
            date_range = []
            if start_date:
                date_range.append(start_date.strftime('%Y'))
            if education.current:
                date_range.append(u'Present')
            elif end_date:
                date_range.append(end_date.strftime('%Y'))

            data = [[Paragraph(u'{0}'.format(education.institution), styles['Normal']),
                     Paragraph(u' - '.join(date_range), styles['ExperienceDate'])
                    ]]
            table = Table(data, colWidths=[317, 150])
            content.append(table)
            if education.degree:
                content.append(Paragraph(education.degree, styles['Normal']))
            content.append(Spacer(1, 4))

    return content

def write_additional_info(additional_info):
    content = []

    if additional_info and additional_info.description:
        content.append(hr)
        content.append(Paragraph(u'<b>Additional Information</b>', styles['Header']))
        content.append(Spacer(1, 4))
        content.append(Paragraph(additional_info.description, styles['Normal']))

    return content

def generate_pdf(resume, buffer):
    content = []
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    content += write_contact(resume.contact)
    content += write_summary(resume.summary)
    content += write_experience(resume.job_set)
    content += write_education(resume.education_set)
    content += write_additional_info(resume.additional_info)

    pdf.build(content)
    return buffer
