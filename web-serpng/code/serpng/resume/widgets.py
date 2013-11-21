"""
http://djangosnippets.org/snippets/1688/
"""
import datetime
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS_3 as MONTHS
from django.utils.safestring import mark_safe

__all__ = ('MonthYearWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')
# Add a blank value for months.
MONTHS[0] = ''

class MonthYearWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes for month and year,
    with 'day' defaulting to the first of the month.

    Based on SelectDateWidget, in 

    django/trunk/django/forms/extras/widgets.py


    """
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = [(num, month.capitalize()) for num, month in MONTHS.items()]
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        s = Select(choices=month_choices)
        # Hacky: Jan 02 is a guard date that signifies that the resume
        # had listed only the year.  Burning Glass interprets year only
        # durations as Jan 01 of that year.
        # See https://github.ksjc.sh.colo/apps-team/web-resumes/issues/71
        if hasattr(value, 'day') and value.month == 1 and value.day == 2:
            select_html = s.render(self.month_field % name, '', local_attrs)
        else:
            select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        # Hack.
        if m == "0" and y:
            return '%s-%s-%s' % (y, 1, 2)
        if y and m:
            return '%s-%s-%s' % (y, m, 1)
        return data.get(name, None)
