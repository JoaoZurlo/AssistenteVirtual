import datetime
import random

import matplotlib.pyplot as plt
import pyttsx3
import speech_recognition
from django.conf.locale import sr
from playsound import playsound
import pygame

from modules.comandos_respostas import respostas

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
import seaborn as sns
import speech_recognition as sr
sns.set()
from modules import comandos_respostas

comandos = comandos_respostas.comandos
resposta = comandos_respostas.respostas
# print(comandos)
# print(resposta)

meu_nome = 'Ana'

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'


def search(frase):
    wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)


# search('linguagem python')

MODEL_TYPES = ['EMOÇÃO']


def load_model_by_name(model_type):
    global model, model_dict, SAMPLE_RATE
    if model_type == MODEL_TYPES[0]:
        model = tf.keras.models.load_model('models/speech_emotion_recognition.hdf5')
        model_dict = sorted(list(['neutra', 'calma', 'feliz', 'triste', 'nervosa', 'medo', 'nojo', 'surpreso']))
        SAMPLE_RATE = 48000
    return model, model_dict, SAMPLE_RATE


# print(load_model_by_name('EMOÇÃO'))
# print(load_model_by_name('EMOÇÃO')[0].summary())

model_type = 'EMOÇÃO'
loaded_model = load_model_by_name(model_type)


def predict_sound(AUDIO, SAMPLE_RATE, plot=True):
    results = []
    wav_data, sample_rate = librosa.load(AUDIO, sr=SAMPLE_RATE)
    # print(wav_data)
    # print(wav_data.shape)
    clip, index = librosa.effects.trim(wav_data, top_db=60, frame_length=512, hop_length=64)
    splitted_audio_data = tf.signal.frame(clip, sample_rate, sample_rate, pad_end=True, pad_value=0)
    for i, data in enumerate(splitted_audio_data.numpy()):
        # print('Audio split: ', i)
        # print(data)
        # print(data.shape)
        mfccs_features = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=48)
        # print(mfccs_features.shape)
        # print(mfccs_features)
        mfccs_scalad_features = np.mean(mfccs_features.T, axis=0)
        mfccs_scalad_features = mfccs_scalad_features.reshape(1, -1)
        # print(mfccs_scalad_features.shape)
        mfccs_scalad_features = mfccs_scalad_features[:, :, np.newaxis]
        # print(mfccs_scalad_features.shape)

        predictions = loaded_model[0].predict(mfccs_scalad_features, batch_size=32)
        # print(predictions)
        # print(predictions.sum())
        if plot:
            plt.figure(figsize=(len(splitted_audio_data), 5))
            plt.barh(loaded_model[1], predictions[0])
            plt.tight_layout()
            plt.show()

        predictions = predictions.argmax(axis=1)
        # print(predictions)
        predictions = predictions.astype(int).flatten()
        predictions = loaded_model[1][predictions[0]]
        results.append(predictions)
        # print(results)

        result_str = 'PARTE' + str(1) + ': ' + str(predictions).upper()
        # print(result_str)

    count_resuts = [[results.count(x), x] for x in set(results)]
    # print(count_resuts)

    print(max(count_resuts))
    return max(count_resuts)


# predict_sound('triste.wav', loaded_model[2], plot=True)  # caso nao queira ver o grafico colocar false

def play_music_youtube(emocao):
    play = False
    if emocao == 'triste' or emocao == 'medo':
        wb.get(chrome_path).open('https://youtu.be/KWjV25q34Hw')
        play = True

    if emocao == 'nervosa' or emocao == 'surpreso':
        wb.get(chrome_path).open('https://youtu.be/EqPyyh9x88A')
        play = True

    return play


# play_music_youtube('triste')
# emocao = predict_sound('triste.wav', loaded_model[2], plot=True)
# print(emocao)
# play_music_youtube(emocao[1])

def speak(audio):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180) #controla a velocidade de reprodução da assistente
    engine.setProperty('volume', 1)  # valor min=0, max=1
    engine.say(audio)
    engine.runAndWait()


#speak('Testando o sintetizador de voz da assistente')

def listen_microphone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source, duration=0.8)
        print('Ouvindo: ')
        audio = microfone.listen(source)
        with open('recordings/speach.wav', 'wb') as f:
            f.write(audio.get_wav_data())


        try:
            frase = microfone.recognize_google(audio, language='pt-BR')
            print('Você disse: ' + frase)
        except speech_recognition.UnknownValueError:
          frase = ''
          print('Não entendi')
        return frase

#listen_microphone()

def test_modal():
    audio_source = 'C:/Users/jzurlo/Downloads/Curso IA/Pycharm/Assistente_Virtual/recordings/speach.wav'
    prediction = predict_sound(audio_source, loaded_model[2], plot=True)
    return prediction

#print(test_modal())

paying = False
mode_control = False

print('[INFO] Pronto para começar!')
pygame.mixer.init()

# Carrega e reproduz o arquivo MP3
pygame.mixer.music.load("n1.mp3")
pygame.mixer.music.play()

# Aguarda o final da reprodução
pygame.mixer.init()

# Carrega e reproduz o arquivo MP3
pygame.mixer.music.load("n1.mp3")
pygame.mixer.music.play()

# Aguarda o término da reprodução
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def speak(audio):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1)
    engine.say(audio)
    engine.runAndWait()



while (1):
    result = listen_microphone()

    if meu_nome in result:
        result = str(result.split(meu_nome + ' ')[1])
        result = result.lower()
        #print('Após o processamento: ', result)

        if result == 'encerrar':
            play_sound('n2.mp3')
            speak(''.join(random.sample(respostas[4], k=1)))
            break


        if result in comandos[0]:
            play_sound('n2.mp3')
            speak('Até agora minhas funções são: ' + respostas[0])



    else:
        play_sound('n3.mp3')








