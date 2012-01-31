# -*- coding: utf-8 -*-
from .forms import OrariFormField
from .models import Orari
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
import datetime
import time


class PagamentoWidget(forms.widgets.MultiWidget):
	def __init__(self, attrs=None):
		widgets = (
			forms.widgets.Select(
				choices=(
					('Ri. ba.', 'Ri. ba.',),
					('rimessa diretta', 'rimessa diretta',),
					('bonifico bancario', 'bonifica bancario'),
					('contanti', 'contanti',),
					('assegno', 'assegno'),
				)
			),
			forms.widgets.Select(
				choices=(
					('', '----',),
					('alla consegna', 'alla consegna',),
					('anticipato', 'anticipato',),
					('30','30'),
					('60','60'),
					('90','90'),
					('120','120'),
				)
			),
			forms.widgets.Select(
				choices=(
					('', '----',),
					('10','10'),
					('20','20'),
				)
			),
			forms.widgets.Select(
				choices=(
					('', '----',),
					('60','60'),
					('90','90'),
					('120','120'),
				)
			),
			forms.widgets.Select(
				choices=(
					('', '----',),
					('10','10',),
					('20','20',),
				)
			))
		super(PagamentoWidget, self).__init__(widgets)

	def decompress(self, value):
		"""
		Takes the text from the database and fills the various selects
		with the right values.

		The value in the database is something like

			Ri. ba.|30+10/60+10
		"""
		values = [None]*5
		if not value:
			return values

		lr = value.split("/")
		if len(lr) > 1:
			mb = lr[1].split('+')
			values[3] = mb[0].strip()

			if len(mb) > 1:
				values[4] = mb[1].strip()

		fs = lr[0].split('|')

		values[0] = fs[0].strip()

		mb = fs[1].split('+')
		values[1] = mb[0].strip()

		if len(mb) > 1:
			values[2] = mb[1].strip()

		return values

	def format_output(self, rendered_widgets):
		return rendered_widgets[0] + ' ' + rendered_widgets[1] + ' + ' + rendered_widgets[2] + ' / ' + rendered_widgets[3] + ' + ' + rendered_widgets[4]


# TODO: write a real model custom field https://docs.djangoproject.com/en/1.3/howto/custom-model-fields/
class PagamentoFormField(forms.fields.MultiValueField):
	"""
	This field describes the terms of payment of a client.
	"""
	widget = PagamentoWidget

	def __init__(self, *args, **kwargs):
		# it's a bug? otherwise fails validation with a field empty
		# see http://code.djangoproject.com/ticket/15511
		kwargs['required'] = False
		_fields = (
			forms.fields.CharField(),
			forms.fields.CharField(),
			forms.fields.CharField(),
			forms.fields.CharField(),
			forms.fields.CharField())
		super(PagamentoFormField, self).__init__(_fields, *args, **kwargs)
	
	def compress(self, data_list):
		"""
		From the various values inserted is possible to obtain the
		following entries

		 30 gg d.f.f.m.
		 30 +10 gg d.f.f.m.
		 60 gg d.f.f.m.
		 60 + 10 gg d.f.f.m.
		 60 / 90  gg d.f.f.m.
		 60 + 10 / 90 + 10 gg d.f.f.m.
		 90 gg d.f.f.m
		 90 + 10 gg d.f.f.m.
		 90 / 120  gg d.f.f.m.
		 90 + 10/120 + 10 gg d.f.f.m.
		 120 gg d.f.f.m.
		 120 + 10 gg d.f.f.m.
		 alla consegna
		 anticipato
		"""
		if data_list[0] in validators.EMPTY_VALUES or data_list[1] in validators.EMPTY_VALUES:
			raise ValidationError('Almeno il primo termine di pagamento va impostato')

		if (data_list[1] == 'alla consegna' or data_list[1] == 'anticipato') \
				and (
					data_list[2] not in validators.EMPTY_VALUES
					or data_list[3] not in validators.EMPTY_VALUES
					or data_list[4] not in validators.EMPTY_VALUES 
				):
					raise ValidationError('Valori impostati inutili')

		if data_list[3] not in validators.EMPTY_VALUES and int(data_list[3]) <= int(data_list[1]):
			raise ValidationError('la seconda scadenza non può essere precedente o uguale alla prima')



		final = data_list[0] + ' | ' + data_list[1]

		if data_list[2]:
			final += ' + ' + data_list[2]
		if data_list[3]:
			final += ' / ' + data_list[3]
		if data_list[4]:
			final += ' + ' + data_list[4]


		return final

# NOTE: using models.Field doesn't create database column
class PagamentoModelField(models.CharField):

	def __init__(self, *args, **kwargs):
                # chose a better value for max_length
		kwargs['max_length'] = kwargs.get('max_length', 50)
		super(PagamentoModelField, self).__init__(*args, **kwargs)

#	def formfield(self, **kwargs):
#		defaults = {'form_class': PagamentoFormField}
#		defaults.update(kwargs)

#		return super(PagamentoModelField, self).formfield(**defaults)

# without this South can't migrate the field
# http://south.aeracode.org/docs/tutorial/part4.html#tutorial-part-4
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_gipi_custom_fields\.PagamentoModelField"])
except ImportError:
    pass


###########
class DatiBancariWidget(forms.widgets.MultiWidget):
	def __init__(self, attrs=None):
		print "DatiBancariWidget.__init__"
		_widgets = (
			forms.widgets.TextInput(),
			forms.widgets.TextInput(),
		)
		super(DatiBancariWidget, self).__init__(_widgets, attrs)

	def decompress(self, value):
		"""
		This must be split the value from DB (using the space as
		separator) and full the textfield with the two values obtained.
		"""
		if value is None:
			return ["", ""]

		return value.split("$")

	def format_output(self, rendered_widgets):
		return 'IBAN ' + rendered_widgets[0] + ' Istituto ' + rendered_widgets[1] 

class DatiBancariFormField(forms.fields.MultiValueField):
	widget = DatiBancariWidget
	def __init__(self, *args, **kwargs):
		_fields = (
			forms.fields.CharField(),
			forms.fields.CharField(),
		)
		super(DatiBancariFormField, self).__init__(_fields, *args, **kwargs);

	def compress(self, data_list):
		"""
		Build up the value to save into the DB joining the two mandatory values
		passed from the user with the char "$" (I hope is not used into the
		input).
		"""
		if data_list[0] in validators.EMPTY_VALUES or data_list[1] in validators.EMPTY_VALUES:
			raise ValidationError('Inserire tutti e due i valori')

		return data_list[0] + "$" + data_list[1]

class DatiBancariModelField(models.Field):
        __metaclass__ = models.SubfieldBase
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 100
		super(DatiBancariModelField, self).__init__(*args, **kwargs)

        def to_python(self, value):
                if isinstance(value, DatiBancari):
                        return value
                if value == "":
                        values = ["", ""]
                else:
                        values = value.split('$')
                return DatiBancari(*values)

        def get_prep_value(self, value):
                return '$'.join([value.name, value.iban])

class DatiBancari(object):
        """
        Bank related data like bank's name and IBAN.

        >>> db = DatiBancari('Banca Sella', '666')
        >>> db
        <django_gipi_custom_fields.DatiBancari object at ...>

        """
        def __init__(self, name, iban):
                self.name = name
                self.iban = iban

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_gipi_custom_fields\.DatiBancariModelField"])
except ImportError:
    pass



class OrariModelField(models.Field):
	"""
	This field is intended to save information about opening hours and
	stuffs like that.

	Internally it saves the information into a Char with each hours comma
	separated and each day (with 4 hours) separated by the pipe character.

	When a day has not hours it is represented as an empty string.
	"""
	__metaclass__ = models.SubfieldBase
	description = "Describes oraries"
	def __init__(self, *args, **kwargs):
		kwargs["max_length"] = 50
		super(OrariModelField, self).__init__(*args, **kwargs)

	def db_type(self):
		return "varchar(30)"

	def _datetime_from_string(self, value):
		try:
			a = time.strptime(value, "%H:%M:%S")
		except:
			return None

		return datetime.time(a.tm_hour, a.tm_min)

	def to_python(self, value):
		"""
		Transforms the value from the DB or when assigned to the field.
		"""
		if value is None:
			return value

		if isinstance(value, basestring):
			if value == "":
				return None

			days = value.split("|")
			orari = []

			for day in days:
				orariostr = day.split(",")
				if len(orariostr) != 4:
					orari.append(None)
				else:
					orari.append(map(self._datetime_from_string, orariostr))
			return Orari(
				monday=orari[0],
				tuesday=orari[1],
				wednesday=orari[2],
				thursday=orari[3],
				friday=orari[4],
				saturday=orari[5],
				sunday=orari[6]
			)
		elif not isinstance(value, Orari):
			raise ValidationError("I need an Orario!!!")

		return value

	def get_prep_value(self, value):
		days = []
		# below we obtain ["08:00,12:00,14:00,18:00", "...", ...]
		for k in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
			orari_for_day = value.orari[k]
			if orari_for_day is not None:
				days.append(",".join([o.isoformat() for o in orari_for_day]))
			else:
				days.append("")

		return "|".join(days)

	def formfield(self, form_class=OrariFormField, **kwargs):
		defaults = {"help_text": "Seleziona i giorni utili ed inserisci i rispettivi orari"}
		defaults.update(kwargs)
		return form_class(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_gipi_custom_fields\.OrariModelField"])
except ImportError:
    pass
