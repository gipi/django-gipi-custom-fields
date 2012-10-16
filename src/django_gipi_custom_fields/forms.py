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
        days_list = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        header = '<thead><th colspan="2"></th><th style="text-align:center" colspan="2">mattina</th><th style="text-align:center" colspan="2">pomeriggio</th></thead>'
        for count in xrange(7):
            rows.append(("<td>%s:</td>" % days_list[count]) + "".join(map(lambda x: "<td>%s</td>" % x, [x for x in islice(rendered_widgets, count*5, count*5 + 5, 1)])))

        rows = map(lambda x: "<tr>%s</tr>" % x, rows)

        return "<table>" + header + ("".join(rows)) + "</table>"

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
        days_list = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        days = {}
        for count in range(0, 35, 5):
            if data_list[count]:
                values = data_list[count + 1:count + 5]
                """
                # TODO: add variable to manage when all the time are needed for row
                if None in values:
                    raise forms.ValidationError("Devi inserire tutti gli orari per il dato giorno")
                """
                days[days_list[count/5]] = values

        return Orari(**days)
