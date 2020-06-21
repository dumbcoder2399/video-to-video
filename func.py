import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
import subprocess
import shutil
from IPython.display import Audio
import requests
from gtts import gTTS
import os
import math
import argparse
import parselmouth
from parselmouth.praat import call 
import librosa
import cv2

def data_preprocess(audio_file_path):
    shutil.copy(audio_file_path,'result/testvideo.mp4')
    command = "ffmpeg -i result/testvideo.mp4 -ab 160k -ac 2 -ar 44100 -vn testvideo.wav"
    subprocess.call(command,shell=True)
    command2 = "spleeter separate -h "
    subprocess.call(command2,shell=True)
    command3="spleeter separate -i testvideo.wav -o output/"
    subprocess.call(command3,shell=True)
    print("-------------------------")
    print("DATA PREPROCESSING DONE")



d=[]
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        for res in range(len(data["results"])):
            print(data["results"][res]["alternatives"][0]["transcript"])
            r=data["results"][res]["alternatives"][0]["transcript"]
            word='%HESITATION'
            line_list=r.split()
            r=(' '.join([i for i in line_list if i not in word]))
            d.append(str(r))


    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

def speechtotext(languagemodel):
    authenticator = IAMAuthenticator('6vGtDAgc9UpxbdGX5x00ULZOAdV2U_Jaz1CE0T6_sdpu')
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )
    speech_to_text.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/a2cc1293-2cef-4b7b-90b1-ae97d16b3081')

    myRecognizeCallback = MyRecognizeCallback()
    with open('./output/testvideo/vocals.wav','rb') as audio_fill:
        audio_sauce = AudioSource(audio_fill)
        speech_to_text.recognize_using_websocket(audio=audio_sauce,content_type='audio/wav',recognize_callback=myRecognizeCallback,model=languagemodel,keywords=['colorado', 'tornado', 'tornadoes'],keywords_threshold=0.5,max_alternatives=1)


def texttotext(langadata,la,lb):
    headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    base_url="https://translate.googleapis.com/translate_a/single"
    stree=""
    for i in range(len(langadata)):
        data={
            
            "client": "gtx",
            "sl": la,
            "tl": lb,
            "dt": "t",
            "q": langadata[i]
            
        }


        r= requests.get(url=base_url,headers=headers,params=data)
        stree+=r.json()[0][0][0]+",  "
    
    return stree



def texttospeechbluemix(lang,voices):
    authenticator1 = IAMAuthenticator('kpRLyx_BAPxZWgSZRkPoARPW43U8_vDzuZv87BiNfS39')
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator1
    )

    text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/4173c65b-56e0-4a7c-869b-1aa5d1e6750e')

    with open('result/audio/welcome.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text=lang,
                voice=voices,
                accept='audio/wav'        
            ).get_result().content)


def texttospeech(words,l):
    mytext=words
    language = l
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("result/audio/welcome.wav") 
    myobj.save("result/gan/welcome.wav") 

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes

faceProto="gendermodel/opencv_face_detector.pbtxt"
faceModel="gendermodel/opencv_face_detector_uint8.pb"
ageProto="gendermodel/age_deploy.prototxt"
ageModel="gendermodel/age_net.caffemodel"
genderProto="gendermodel/gender_deploy.prototxt"
genderModel="gendermodel/gender_net.caffemodel"


MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)


def vidgender(videopath):
    cam= cv2.VideoCapture(videopath)

    padding=20

    hasframe,frame=cam.read()


    resultImg,faceBoxes=highlightFace(faceNet,frame)
    if not faceBoxes:
        print("No face detected")

    for faceBox in faceBoxes:
        face=frame[max(0,faceBox[1]-padding):
                min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                :min(faceBox[2]+padding, frame.shape[1]-1)]

        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds=genderNet.forward()
        gender=genderList[genderPreds[0].argmax()]
        print(f'Gender: {gender}')

        ageNet.setInput(blob)
        agePreds=ageNet.forward()
        age=ageList[agePreds[0].argmax()]
        print(f'Age: {age[1:-1]} years')

        cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
        cv2.imshow("Detecting age and gender", resultImg)
        return gender

def male():
    sampling_rate= 44100
    y, sr = librosa.load('result/audio/welcome.wav', sr=sampling_rate) 

    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=-11, bins_per_octave=24)
    librosa.output.write_wav('result/audio/welcome.wav', y_shifted, sr=sampling_rate, norm=False)

def malelow():
    sampling_rate= 44100
    y, sr = librosa.load('result/gan/welcome.wav', sr=sampling_rate) 

    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=-19, bins_per_octave=24)
    librosa.output.write_wav('result/gan/welcomelow.wav', y_shifted, sr=sampling_rate, norm=False)




