import pyttsx3
import speech_recognition as sr
from playsound import playsound
import random
import datetime
hour = datetime.datetime.now().strftime('%H:%M')
print(hour)
date = datetime.date.today().strftime('%d/%B/%y')
print(date)
date = date.split('/')
print(date)

import webbrowser as wb
import tensorflow as tf
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from modules import comandos_respostas
comandos = comandos_respostas.comandos
resposta = comandos_respostas.respostas
#print(comandos)
#print(resposta)

meu_nome = 'TechZurlo'

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

def search(frase):
    wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)


#search('linguagem python')

MODEL_TYPES = ['EMOÇÃO']

def load_model_by_name(model_type):
    if model_type == MODEL_TYPES[0]:
        model = tf.keras.models.load_model('models/speech_emotion_recognition.hdf5')
        model_dict = sorted(list(['neutra', 'calma', 'feliz', 'triste', 'nervosa', 'medo', 'nojo', 'surpreso']))
        SAMPLE_RATE = 48000
    return model, model_dict, SAMPLE_RATE

#print(load_model_by_name('EMOÇÃO'))
#print(load_model_by_name('EMOÇÃO')[0].summary())

model_type = 'EMOÇÃO'
loaded_model = load_model_by_name(model_type)

def predict_sound(AUDIO, SAMPLE_PATE, plot = True):
    results = []
    wav_data, sample_rate = librosa.load(AUDIO, sr=SAMPLE_PATE)
    #print(wav_data)
    #print(wav_data.shape)
    clip, index = librosa.effects.trim(wav_data, top_db=60, frame_length=512, hop_length=64)
    splitted_audio_data = tf.signal.frame(clip, sample_rate, sample_rate, pad_end=True, pad_value=0)
    for i, data in enumerate(splitted_audio_data.numpy()):
        print('Audio')




predict_sound('triste.wav', loaded_model[2], plot=True)
