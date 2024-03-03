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

