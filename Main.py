#WEB
import requests
from bs4 import BeautifulSoup

#base
import json
from os.path import join, dirname

#IBM-TOOLS
from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource

#Audio
from playsound import playsound
import time

#------------------------End-Of-Imports---------------------------

'''
Program-flow:
mic-input -> stt -> process -> tts response -> play the audio (if saved, rm)
'''


def TTS_IBM_WATSON(Line):
    #AUTHENTICATION FOR IBM
    API_KEY = 'OgqZLEBuJbeP4tQnrNNYUMjmJcb6lBTQLOwrycTHMq_1'
    API_URL = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/832cd92b-0ae6-45e1-bfac-796a66b0b465'

    authenticator = IAMAuthenticator(API_KEY)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )
    text_to_speech.set_service_url(API_URL)
    
    #--------------------------------------------------------------------------------
    
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
        