from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Radio, ProgramasRadiales

import time
import vlc
import sys

class IndexRadio(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'radio/radio.html'



#datos = ProgramasRadiales.objects.all().values()

def obtener_nombre_programa(codigo):

    datos = ProgramasRadiales.objects.filter(id=codigo).values()

    #lista = []

    for dat in datos:
        c = dat.get('nombre')
        nombre_programa = c.replace(' ', '')
        h = dat.get('inicio')
        hora = h.strftime('%H:%M')
        fecha_programa = time.strftime('%d-%m-%y')
        completo = nombre_programa+'-'+fecha_programa+'-'+hora
        #lista += [completo]

    return completo

#print(obtener_nombre_programa())

def obtener_tiempo_programa(codigo):

    datos = ProgramasRadiales.objects.filter(id=codigo).values()
    #lista = []

    for dat in datos:
        c = dat.get('duracion')
        #lista += [c]

    return c

#print(obtener_tiempo_programa())

def obtener_web_programa(codigo):

    url = ProgramasRadiales.objects.filter(id=codigo).values('radios__web')

    #lista = []

    for dat in url:
        c = dat.get('radios__web')
        #lista += [c]

    return c

#print(obtener_web_programa())

def grabar_audio(nombre, stream, tiempo):

    convertidor = "--sout=#transcode{acodec=flac,ab=128,channels=1,samplerate=32000}:std{access=file,mux=raw,dst='/home/eparionad/Descargas/ProyectoPython/%s.flac'} --run-time=%s --stop-time=%s" % (nombre, tiempo, tiempo)
    instancia = vlc.Instance(convertidor)
    reproductor = instancia.media_player_new()
    medios = instancia.media_new(stream)
    medios.get_mrl()
    reproductor.set_media(medios)
    reproductor.play()
    time.sleep(tiempo)

def programa_principal():

    datos1 = ProgramasRadiales.objects.all()

    #tiempo = time.time()

    dia = time.gmtime()
    #dia = time.localtime()

    dia_actual = dia.tm_wday

    hora = time.strftime('%H:%M')

    for dato in datos1:
        hora_pro = (dato.inicio).strftime('%H:%M')

        if hora_pro == hora:
            for x in dato.dias:
                if str(dia_actual) == str(x):

                    codigo = dato.id
                    nombre_archivo = obtener_nombre_programa(codigo)
                    url = obtener_web_programa(codigo)
                    inicio_pro = obtener_tiempo_programa(codigo)
                    audio = grabar_audio(nombre_archivo, url, inicio_pro)
                    print(nombre_archivo)
                    print(url)
                    print(inicio_pro)
                else:
                    print('No hace nada')

        else:
            print('No es el momento')

#print(programa_principal())
programa_principal()
