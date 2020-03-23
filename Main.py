import requests
from bs4 import BeautifulSoup

import json
from os.path import join, dirname

#IBM-Watson
from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource

#Audio-Tools
from playsound import playsound
import time

#------------------------End-Of-Imports---------------------------

'''
Program-flow:
mic-input[F] -> stt[F](command) -> process -> tts response -> play the audio (if saved, rm)
'''

#---------------------AUTHENTICATION FOR IBM-----------------------
#TTS
API_KEY = '' #Can be found on the IBM service manage page
API_URL = ''

authenticator = IAMAuthenticator(API_KEY)
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
text_to_speech.set_service_url(API_URL)

#STT - Future
''' 
API_KEY = ''
API_URL = ''

authenticator = IAMAuthenticator(API_KEY)
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(API_URL)
'''
#------------------------------------------------------------------


def TTS_IBM_WATSON(Line):
    with open('res.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                Line,
                voice='en-US_AllisonVoice',
                accept='audio/wav'        
            ).get_result().content)
    return 1


def get_covid_update():
    url = "https://www.worldometers.info/coronavirus/"
    page = requests.get(url)
    page_source = page.text
    soup = BeautifulSoup(page_source, "lxml")
    Cases = {
        'Total Number of COVID-19 Cases': 0,
        ' and Total Number of Deaths': 0,
        ' and Total Number of Recovered Cases': 0,
    }
    emp = [] + list(Cases.keys())
    num = 0
    for place in soup.find_all('div', class_='maincounter-number'):
        Cases[emp[num]]=str(place.span.string).strip(' ')
        num+=1
    result = ''
    k = Cases.keys()
    keys = []+list(k)
    v = Cases.values()
    values = []+list(v)

    for idx in range(len(keys)):
        current_key = keys[idx]
        result+= " "+(current_key+": " + Cases[current_key])
    return result


def main():
    command = str(input(">"))
    if "update on corona" in command:
        data_line = get_covid_update()
        if TTS_IBM_WATSON(data_line) == 1: time.sleep(1); playsound('res.wav')
        else: print("I am lazy, I have to quit sorry")

main()
        