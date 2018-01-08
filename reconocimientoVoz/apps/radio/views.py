from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Radio, ProgramasRadiales

import time

class IndexRadio(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'radio/radio.html'


"""class GrabarProgramaRadial():

    datos = ProgramasRadiales.objects.filter(id='1').values()

    def obtener_nombre_programa():
        for dat in datos:
            c = dat.get('nombre')
            nombre_programa = c.replace(' ','')
            print (nombre_programa)

            return nombre_programa"""

datos = ProgramasRadiales.objects.all().values()

def obtener_nombre_programa():

    lista = []

    for dat in datos:
        c = dat.get('nombre')
        nombre_programa = c.replace(' ', '')
        h = dat.get('inicio')
        hora = h.strftime('%H:%M')
        fecha_programa = time.strftime('%d-%m-%y')
        completo = nombre_programa+'-'+fecha_programa+'-'+hora
        lista += [completo]

    return lista

print(obtener_nombre_programa())

def obtener_tiempo_programa():
    lista = []

    for dat in datos:
        c = dat.get('duracion')
        lista += [c]

    return lista

print(obtener_tiempo_programa())

def obtener_web_programa():

    lista = []

    for dat in datos:
        c = dat.get('radios_id')
        lista += [c]

    return lista

print(obtener_web_programa())
