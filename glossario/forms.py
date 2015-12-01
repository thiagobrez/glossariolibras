# -*- coding: utf-8 -*-

from glossario.models import Glossario, Sinal
from django import forms
import datetime

class GlossarioForm(forms.ModelForm):

	class Meta:
		model = Glossario
		exclude = ['link','dataCriacao']

class PesquisaPortForm(forms.ModelForm):
	
	class Meta:
		model = Sinal
		fields = ['traducaoP']


class PesquisaIngForm(forms.ModelForm):
	
	class Meta:
		model = Sinal
		fields = ['traducaoI']

class SinalForm(forms.ModelForm):

	class Meta:
		model = Sinal
		fields = '__all__'

#


#	def clean_nome(self):
#		palavra = self.cleaned_data['nome']
		#tudo para minusculo
		#tirar espacos
		#tirar acentos
		
#		self.exclude.append('link')

#		return self.cleaned_data['nome']