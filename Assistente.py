import datetime

import matplotlib.pyplot as plt

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

sns.set()
from modules import comandos_respostas

comandos = comandos_respostas.comandos
resposta = comandos_respostas.respostas
# print(comandos)
# print(resposta)

meu_nome = 'TechZurlo'

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


#predict_sound('triste.wav', loaded_model[2], plot=True)  # caso nao queira ver o grafico colocar false

def play_music_youtube(emocao):
    play = False
    if emocao == 'triste' or emocao == 'medo':
        wb.get(chrome_path).open('https://youtu.be/KWjV25q34Hw')
        play = True

    if emocao == 'nervosa' or emocao == 'surpreso':
        wb.get(chrome_path).open('https://youtu.be/EqPyyh9x88A')
        play = True

    return play


#play_music_youtube('triste')
#emocao = predict_sound('triste.wav', loaded_model[2], plot=True)
#print(emocao)
#play_music_youtube(emocao[1])


















