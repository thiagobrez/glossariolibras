# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from glossario.models import Glossario, Sinal, Usuario, Tema
from glossario.forms import PesquisaPortForm, PesquisaIngForm
from django.template import RequestContext
from django.http import JsonResponse
import json

def index(request, glossario=None):
	if glossario:
		try:
			glossario = Glossario.objects.get(link=glossario)
			return render_to_response("glossario.html", dict(glossario=glossario))
		except Glossario.DoesNotExist:
			glossarios = Glossario.objects.all()
	else:		
		glossarios = Glossario.objects.all()

	return render_to_response("index.html", dict(glossarios=glossarios, glossario=glossario))

def pesquisa(request, glossario=None, tipopesq=None):
	try:
		glossario = Glossario.objects.get(link=glossario)
	except Glossario.DoesNotExist:
		glossario = None
	if request.method == "POST":
			
		if tipopesq == "p":
			formulario = PesquisaPortForm(request.POST)
			if formulario.is_valid():
				sinais = Sinal.objects.filter(traducaoP__contains=formulario.cleaned_data['traducaoP'])
				resultado = len(sinais)
				return render_to_response(
					"pesquisa.html", 
					context_instance=RequestContext(
					request, 
					{ 'glossario':glossario, 'formulario':formulario, "sinais":sinais, 'resultado':resultado}
					))
				
		elif tipopesq == "e":
			formulario = PesquisaIngForm(request.POST)
			if formulario.is_valid():
				sinais = Sinal.objects.filter(traducaoI__contains=formulario.cleaned_data['traducaoI'])
				resultado = len(sinais)
				return render_to_response(
					"pesquisa.html", 
					context_instance=RequestContext(
					request, 
					{ 'glossario':glossario, 'formulario':formulario, "sinais":sinais, 'resultado':resultado}
					))

		elif tipopesq == "s":
				sinais = None
		
		else:
			sinais = None
	else:
		formulario = PesquisaPortForm()
		sinais = None
	return render_to_response(
		"pesquisa.html", 
		context_instance=RequestContext(
		request, 
		{ 'glossario':glossario, 'formulario':formulario}
		))

def equipe(request):
	usuario = Usuario.objects.all()
	return render_to_response("equipe.html", dict(usuario=usuario))

def contato(request):
	return render_to_response("contato.html")

def historia(request):
	return render_to_response("historia.html")

def criaNodo(nodoPai):
	filhosPai = queryTemas.filter(temaPai=nodoPai)
	filhos = list()
	for filho in filhosPai:
		filhos.append(criaNodo(filho))
	nodoPai.filhos = filhos
	return nodoPai
	
#Metodo simples para exibição da lista no terminal
def mostraNodo(nodoTema1, n):
	txt = " - "*n
	if nodoTema1.filhos:
		print str(n) + txt +nodoTema1.nome
		filhos = nodoTema1.filhos
		for filho in filhos:
			mostraNodo(filho, n+1)
	else:
		print str(n) + txt +nodoTema1.nome

def mostraNodoJson(nodoTema1):
	if nodoTema1.filhos:
		filhos = nodoTema1.filhos
		jsonTemas['edges'][nodoTema1.nome] = {}
		for filho in filhos:
			mostraNodoJson(filho)
			jsonTemas['edges'][nodoTema1.nome][filho.nome] = {}
	jsonTemas['nodes'][nodoTema1.nome] = {"color":"green", "shape":"dot", "alpha":1, "link":"www.libras.ufsc.br" }

def temas(request, temas=None):
	global queryTemas
	queryTemas = Tema.objects.all()
	try:
		raiz = criaNodo(queryTemas.get(id=1))
		mostraNodo(raiz, 0)
	except Tema.DoesNotExist:
		raiz = None
	return render_to_response("temas.html", dict(raiz=raiz))

def sinal(request, sinal=None):
	if sinal:
		try:
			sinal = Sinal.objects.get(id=sinal)
			
		except Sinal.DoesNotExist:
			sinal = None
			
		return render_to_response("sinal.html", dict(sinal=sinal))

def temasjson(request):
	global jsonTemas
	jsonTemas = {"nodes":{},"edges":{}}
	data = {
		"nodes":{
			"joao" : {"color":"red", "shape":"dot", "alpha":1 },
			"ramon" : {"color":"green", "shape":"dot", "alpha":1, "link":"ramon" },
			"glossario" :{"color":"#b2b19d", "shape":"dot", "alpha":1},
			"NALS" :{"color":"#b2b19d", "shape":"dot", "alpha":1}
		},
		"edges":{
			"glossario":{"joao":{},"ramon":{}}
		}
	}
	data['nodes']['glossario'] = {"color":"green", "shape":"dot", "alpha":1, "link":"ramon" }
	raiz = criaNodo(Tema.objects.get(id=1))
	mostraNodoJson(raiz)
	print jsonTemas
	return JsonResponse(jsonTemas)
