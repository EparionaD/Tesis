from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Radio, ProgramasRadiales

import time

class IndexRadio(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'radio/radio.html'



datos = ProgramasRadiales.objects.all().values()

def obtener_nombre_programa(codigo):

    datos = ProgramasRadiales.objects.filter(id=codigo).values()

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

#print(obtener_nombre_programa())

def obtener_tiempo_programa():
    lista = []

    for dat in datos:
        c = dat.get('duracion')
        lista += [c]

    return lista

print(obtener_tiempo_programa())

def obtener_web_programa():

    url = ProgramasRadiales.objects.all().values('radios__web')

    lista = []

    for dat in url:
        c = dat.get('radios__web')
        lista += [c]

    return lista

print(obtener_web_programa())

def comparar_fechas_horas():

    datos1 = ProgramasRadiales.objects.all()

    tiempo = time.time()

    dia = time.gmtime(tiempo)

    dia_actual = dia.tm_wday

    hora = time.strftime('%H:%M')

    for dato in datos1:
        hora_pro = (dato.inicio).strftime('%H:%M') #esta es la forma correcta de darle formato.

        if hora_pro == hora:
            for x in dato.dias:
                if str(dia_actual) == str(x):
                    #print('Logica que me falta desarrollar') #insertar la otra funcion o llamarla
                    codigo = dato.id
                    nombre_archivo = obtener_nombre_programa(codigo)
                    print(nombre_archivo)
                else:
                    print('No hace nada')
        else:
            print('No es el momento')

print(comparar_fechas_horas())
