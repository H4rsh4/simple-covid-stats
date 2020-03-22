#import pandas as pd
from bs4 import BeautifulSoup
#from selenium import webdriver

#from ibm_watson import TextToSpeechV1
#from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import requests




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
    
    with open('test.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                result,
                voice='en-US_AllisonVoice',
                accept='audio/wav'        
            ).get_result().content)

def covid_cases()->dict:
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
    return Cases

data = covid_cases()
result = ''
k = data.keys()
keys = []+list(k)
v = data.values()
values = []+list(v)

for idx in range(len(keys)):
    current_key = keys[idx]
    result+= " "+(current_key+": " + data[current_key])
print(result)


with open('test.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            result,
            voice='en-US_AllisonVoice',
            accept='audio/wav'        
        ).get_result().content)
