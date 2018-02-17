from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Radio, ProgramasRadiales

import time
import vlc
import sys
import os
import io
import threading
import fnmatch

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/eparionad/Dropbox/Tesis/CredencialesApiGoogle/Tesis-59cc7659afbc.json'

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
        completo = str(codigo)+'-'+nombre_programa+'-'+fecha_programa+'-'+hora
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

def grabar_audio(carpeta, nombre, stream, tiempo):

    convertidor = "--sout=#transcode{acodec=flac,ab=128,channels=1,samplerate=16000}:std{access=file,mux=raw,dst='%s/%s.flac'} --run-time=%s --stop-time=%s" % (carpeta, nombre, tiempo, tiempo)
    instancia = vlc.Instance(convertidor)
    reproductor = instancia.media_player_new()
    medios = instancia.media_new(stream)
    medios.get_mrl()
    reproductor.set_media(medios)
    reproductor.play()
    time.sleep(tiempo)

def crear_carpetas(nombre):
    
    dia = time.gmtime()
    fecha = time.strftime('%d-%m-%Y', dia)
    carpeta = '/home/eparionad/Descargas/%s' % os.path.join(fecha, nombre)

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    return carpeta


def programa_principal():

    datos1 = ProgramasRadiales.objects.all()


    #dia = time.gmtime()
    dia = time.localtime()

    dia_actual = dia.tm_wday

    hora = time.strftime('%H:%M')

    for dato in datos1:
        hora_pro = (dato.inicio).strftime('%H:%M')

        if hora_pro == hora:
            for x in dato.dias:
                if str(dia_actual) == str(x):

                    codigo = dato.id
                    nc = dato.nombre
                    nombre_carpeta = nc.replace(' ', '')
                    nombre_archivo = obtener_nombre_programa(codigo)
                    url = obtener_web_programa(codigo)
                    inicio_pro = obtener_tiempo_programa(codigo)
                    carpeta = crear_carpetas(nombre_carpeta)
                    audio = threading.Thread(target=grabar_audio, args=(carpeta, nombre_archivo, url, inicio_pro))
                    audio.start()
                    print(nombre_archivo)
                    print(url)
                    print(inicio_pro)
                    print(nombre_carpeta)
                else:
                    print('No hace nada')

        else:
            print('No es el momento')

#print(programa_principal())
programa_principal()

def transcribe_file():
        #Transcribe the given audio file asynchronously.
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    speech_file = '/home/eparionad/Descargas/05-02-2018/MatinalNoticias/2-MatinalNoticias-04-02-18-21:18.flac'

    # [START migration_async_request]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='es-PE')

    # [START migration_async_response]
    operation = client.recognize(config, audio)
    # [END migration_async_request]

    print('Waiting for operation to complete...')
    #response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in operation.results:
        # The first alternative is the most likely one for this portion.
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END migration_async_response]
# [END def_transcribe_file]

def enviar_audio():

    datos =  ProgramasRadiales.objects.all()

    ruta_parcial = '/home/eparionad/Descargas'
    tiempo = time.gmtime()
    fecha = time.strftime('%d-%m-%Y', tiempo)

    for dato in datos:
        nc = dato.nombre
        programa = nc.replace(' ', '')

        ruta_total = os.path.join(ruta_parcial, '05-02-2018', programa)

        for carpetas in os.walk(ruta_total):
            for carpeta in carpetas:
                for archivos in carpeta:
                    if fnmatch.fnmatch(archivos, '*.flac'):
                        nombre = archivos.replace('flac', 'txt')
                        #print(nombre)
                        if not os.path.exists(os.path.join(ruta_total,nombre)):
                            #audio_grabado = transcribe_file()
                            print('LLamo a la funcion')

                        else:
                            print('No hago nada')

        #print(ruta_total)

print(enviar_audio())