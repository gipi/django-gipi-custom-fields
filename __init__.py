# -*- coding: utf-8 -*-
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


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


class PagamentoField(forms.fields.MultiValueField):
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
		super(PagamentoField, self).__init__(_fields, *args, **kwargs)
	
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
