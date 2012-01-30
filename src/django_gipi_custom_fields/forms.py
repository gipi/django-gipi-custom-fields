from django_gipi_custom_fields.models import Orari

from django import forms
from django.contrib.admin.widgets import AdminTimeWidget

from itertools import islice


class OrariFormWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.CheckboxInput(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            forms.widgets.CheckboxInput(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            forms.widgets.CheckboxInput(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            forms.widgets.CheckboxInput(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            forms.widgets.CheckboxInput(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            forms.widgets.CheckboxInput(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            forms.widgets.CheckboxInput(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
            AdminTimeWidget(),
        )
        super(OrariFormWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        """
         Orari -> 7*[boolean and 4 datetime fields]
        """
        empty_row = [False, None, None, None, None]
        if value is None:
            return empty_row

        days = []
        fields_values = []
        if isinstance(value, Orari):
            for k in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                if value.orari[k] is not None:
                    orari = value.orari[k]
                    orari.insert(0, True)
                    days.append(orari)
                else:
                    days.append(empty_row)

            # now we flatten the list
            for day in days:
                for orario in day:
                    fields_values.append(orario)
            return fields_values

    def format_output(self, rendered_widgets):
        """
        Divides the 35 form field in 7 rows and creates a table from it.
        """
        rows = []
        for count in xrange(7):
            rows.append("".join(map(lambda x: "<td>%s</td>" % x, [x for x in islice(rendered_widgets, count*5, count*5 + 5, 1)])))

        rows = map(lambda x: "<tr>%s</tr>" % x, rows)

        return "<table>" + ("".join(rows)) + "</table>"

class OrariFormField(forms.fields.MultiValueField):
    widget = OrariFormWidget
    def __init__(self, *args, **kwargs):
        fields = (
            forms.fields.BooleanField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.BooleanField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.BooleanField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.BooleanField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.BooleanField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.BooleanField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.BooleanField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
            forms.fields.TimeField(required=False),
        )
        super(OrariFormField, self).__init__(fields, required=False, *args, **kwargs)

    def compress(self, data_list):
        """
        Instead of call clean(), calls this
        """
        days = {}
        if data_list[0]:
            days["monday"] = data_list[1:5]

        if data_list[5]:
            days["tuesday"] = data_list[6:10]

        if data_list[10]:
            days["wednesday"] = data_list[11:15]

        if data_list[15]:
            days["thursday"] = data_list[16:20]

        if data_list[20]:
            days["friday"] = data_list[21:25]

        if data_list[25]:
            days["saturday"] = data_list[26:30]

        if data_list[30]:
            days["sunday"] = data_list[31:35]

        return Orari(**days)
