import subprocess
from func import *
import os

optionsSTT={"Arabic":"ar-AR_BroadbandModel",
"Brazilian Portuguese":"pt-BR_BroadbandModel",
"Chinese":"zh-CN_BroadbandModel",
"Dutch":"nl-NL_BroadbandModel",
"English-UK":"en-GB_BroadbandModel",
"English-US":"en-US_BroadbandModel",
"French":"fr-FR_BroadbandModel",
"German":"de-DE_BroadbandModel",
"Italian":"it-IT_BroadbandModel",
"Japanese":"ja-JP_BroadbandModel",
"Korean":"ko-KR_BroadbandModel",
"Spanish":"es-AR_BroadbandModel"
}

optionTTsl={"Arabic":"ar",
"Brazilian Portuguese":"pt",
"Chinese":"zh",
"Dutch":"nl",
"English-UK":"en",
"English-US":"en",
"French":"fr",
"German":"de",
"Italian":"it",
"Japanese":"ja",
"Korean":"ko",
"Spanish":"es"
}
optionTTTtl={"Arabic":"ar",
"Brazilian Portuguese":"pt",
"Chinese":"zh",
"Dutch":"nl",
"English-UK":"en",
"English-US":"en",
"French":"fr",
"German":"de",
"Italian":"it",
"Japanese":"ja",
"Korean":"ko",
"Hindi":"hi",
"Spanish":"es"
}

optionTTS={"Arabic":"ar",
"Brazilian Portuguese":"pt",
"Chinese":"zh",
"Dutch":"nl",
"English-UK":"en",
"English-US":"en",
"French":"fr",
"German":"de",
"Italian":"it",
"Japanese":"ja",
"Korean":"ko",
"Hindi":"hi",
"Spanish":"es"
}


def changemavoice(file_path,inputlanguage="English-US",outputlanguage="hi"):
    file_path="./media/"+str(file_path)
    filenaam=os.path.basename(str(file_path))
    data_preprocess(file_path)
    myRecognizeCallback = MyRecognizeCallback()
    lang=inputlanguage
    languagemodel=optionsSTT[lang]
    with open('./output/testvideo/vocals.wav','rb') as audio_fill:
        audio_sauce = AudioSource(audio_fill)
        speech_to_text.recognize_using_websocket(audio=audio_sauce,content_type='audio/wav',recognize_callback=myRecognizeCallback,model=languagemodel,keywords=['colorado', 'tornado', 'tornadoes'],keywords_threshold=0.5,max_alternatives=1)
    print("-------------------------")
    print("SPEECH TO TEXT DONE")

    langa= texttotext(d)
    print("-------------------------")
    print("TEXT TO TEXT DONE")
    texttospeech(langa)
    print("-------------------------")
    print("TEXT TO SPEECH DONE")

    gen= vidgender(file_path)
    if gen=="Male":
        xcv='python3 convert.py'
        subprocess.call(xcv,shell=True)
        male()

    os.chdir('./result/')

    lipGAN='python3 batch_inference.py --checkpoint_path logs/lipgan_residual_mel.h5 --model residual --face "testvideo.mp4" --fps 24 --audio ./audio/welcome.wav --results_dir ./video'
    subprocess.call(lipGAN,shell=True)
    os.chdir('..')
    transfilenaam='./media/Videos/translated'+filenaam
    shutil.copy('./result/video/result_voice.avi',transfilenaam)

    return transfilenaam

#changemavoice('./media/Videos/obama.mp4')
    