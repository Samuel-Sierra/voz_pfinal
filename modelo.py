import numpy as np
import librosa
from python_speech_features import mfcc

def segmentAudio(data, sr, seg_duration=0.05, hop_duration=0.025):

    seg_length = int(seg_duration * sr)
    hop_length = int(hop_duration * sr)
    segments = []
    for i in range(0, len(data) - seg_length + 1, hop_length):
        segment = data[i : i + seg_length]
        
        energy = np.sum(segment**2) / len(segment)
        if energy > 0.00001:
            segments.append(segment)
    return segments

def zero_crossing_rate(signal):
    return np.mean(np.abs(np.diff(np.sign(signal))))

def extractFeatures(segments, sr):
    features = []
    for segment in segments:
        energy = np.sum(segment**2) / len(segment)
        zcr_val = zero_crossing_rate(segment)
        mfcc_feat = mfcc(segment, samplerate=sr, numcep=12)
        mfcc_mean = np.mean(mfcc_feat, axis=0)
        feature_vector = [energy, zcr_val] + mfcc_mean.tolist()
        features.append(feature_vector)
    return np.array(features)

#analisis de señal, extraccion de caracteristicas, 
def Dataset(archivos, seg_duration=0.05, hop_duration=0.025):

    all_features = []
    for archivo in archivos:

        data, sr = librosa.load(archivo)
        print(f"{archivo}, duración = {len(data) / sr:.2f}s, sr = {sr}Hz")

        segments = segmentAudio(data, sr, seg_duration, hop_duration)

        features = extractFeatures(segments, sr)
        all_features.append(features)

    if len(all_features) > 0:
        all_features = np.vstack(all_features)
    else:
        all_features = np.array([])
    return all_features

archivos="direccion dataset"

from hmmlearn import hmm

def entrenar_modelos_hmm(archivos_dict, seg_duration=0.05, hop_duration=0.025):
    modelos = {}
    for fonema, lista_archivos in archivos_dict.items():
        print(f"Entrenando HMM para fonema: {fonema}")
        features = Dataset(lista_archivos, seg_duration, hop_duration)

        if len(features) > 0:
            modelo = hmm.GaussianHMM(n_components=3, covariance_type='diag', n_iter=100)
            modelo.fit(features)
            modelos[fonema] = modelo
    return modelos

def clasificar_audio(modelos, archivo, seg_duration=0.05, hop_duration=0.025):
    data, sr = librosa.load(archivo)
    segmentos = segmentAudio(data, sr, seg_duration, hop_duration)
    features = extractFeatures(segmentos, sr)

    scores = {}
    for fonema, modelo in modelos.items():
        try:
            score = modelo.score(features)  
            scores[fonema] = score
        except:
            scores[fonema] = float('-inf')  
    predicho = max(scores, key=scores.get)
    return predicho, scores

modelos = entrenar_modelos_hmm(archivos)
pred, scores = clasificar_audio(modelos, 'dataset/test_audio.wav')
