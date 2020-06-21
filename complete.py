import subprocess
from func import *
import os, sys
import ffmpeg



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
"Tamil":"ta",
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
"Tamil":"ta",
"Spanish":"es"
}

voicesmale={
    "Arabic":"ar-AR_OmarVoice",
    "Chinese":"zh-CN_WangWeiVoice",
    "Dutch":"nl-NL_LiamVoice",
    "English-UK":"en-US_MichaelVoice",
    "English-US":"en-US_MichaelVoice",
    "German":"de-DE_DieterVoice",
    "Korean":"ko-KR_YoungmiVoice",
    "Spanish":"es-ES_EnriqueVoice"
}

malevoicesavailable=["Arabic","Chinese","Dutch","English-UK","English-US","German","Korean","Spanish"]




def changemavoice(file_path,inputlanguage,outputlanguage):
    
    file_path="./media/"+str(file_path)
    orgfile=os.path.basename(str(file_path))
    filenaam='translated'+os.path.basename(str(file_path))
    data_preprocess(file_path)
    # myRecognizeCallback = MyRecognizeCallback()
    lang=inputlanguage
    lang1=outputlanguage
    
    languagemodel=optionsSTT[lang]
    languagemodel1=optionTTS[lang1]
    speechtotext(languagemodel)
    # with open('./output/testvideo/vocals.wav','rb') as audio_fill:
    #     audio_sauce = AudioSource(audio_fill)
    #     speech_to_text.recognize_using_websocket(audio=audio_sauce,content_type='audio/wav',recognize_callback=myRecognizeCallback,model=languagemodel,keywords=['colorado', 'tornado', 'tornadoes'],keywords_threshold=0.5,max_alternatives=1)
    print("-------------------------")
    print("SPEECH TO TEXT DONE")

    langa= texttotext(d,optionTTsl[lang],optionTTTtl[lang1])
    print("-------------------------")
    print("TEXT TO TEXT DONE")
    texttospeech(langa,languagemodel1)
    print("-------------------------")
    print("TEXT TO SPEECH DONE")

    gen= vidgender(file_path)
    if gen=="Male":     
        if outputlanguage in malevoicesavailable:
            texttospeechbluemix(langa,voicesmale[outputlanguage])
            shutil.copy('./result/audio/welcome.wav','./result/gan/welcome1.wav')
        xcv='python3 convert.py'
        subprocess.call(xcv,shell=True)
        #male()

    os.chdir('./result/')

    lipGAN='python3 batch_inference.py --checkpoint_path logs/lipgan_residual_mel.h5 --model residual --face "testvideo.mp4" --fps 24 --audio ./gan/welcome1.wav --results_dir ./video'
    subprocess.call(lipGAN,shell=True)
    commander="ffmpeg -i './video/result_voice.avi' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 './video/result_voice.mp4'"
    subprocess.call(commander,shell=True)
    commander2="ffmpeg -i './video/result.avi' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 './video/result.mp4'"
    subprocess.call(commander2,shell=True)
    os.chdir('..')
    input_video = ffmpeg.input('./result/video/result.mp4')
    # if gen=="Male":
    #     input_audio1 = ffmpeg.input('./result/audio/welcome.wav')
    # else:
    #     input_audio1 = ffmpeg.input('./result/gan/welcome.wav')
    input_audio1 = ffmpeg.input('./result/audio/welcome.wav')
    ffmpeg.concat(input_video, input_audio1, v=1, a=1).output('./media/Videos/LQ'+orgfile).run()

    transfilenaam='./media/Videos/'+filenaam
    shutil.copy('./result/video/result_voice.mp4',transfilenaam)

    finalpath=orgfile
    return gen,finalpath



def changemavoicever2(file_path,inputlanguage,outputlanguage):
    file_path="./media/"+str(file_path)
    orgfile=os.path.basename(str(file_path))
    filenaam='LQ'+os.path.basename(str(file_path))
    data_preprocess(file_path)
    lang=inputlanguage
    lang1=outputlanguage
    
    languagemodel=optionsSTT[lang]
    languagemodel1=optionTTS[lang1]
    speechtotext(languagemodel)
    
    print("-------------------------")
    print("SPEECH TO TEXT DONE")

    langa= texttotext(d,optionTTsl[lang],optionTTTtl[lang1])
    print("-------------------------")
    print("TEXT TO TEXT DONE")
    texttospeech(langa,languagemodel1)
    print("-------------------------")
    print("TEXT TO SPEECH DONE")

    gen= vidgender(file_path)
    if gen=="Male":     
        xcv='python3 convert.py'
        subprocess.call(xcv,shell=True)
        male()

    os.chdir('./result/')

    lipGAN='python3 batch_inference.py --checkpoint_path logs/lipgan_residual_mel.h5 --model residual --face "testvideo.mp4" --fps 24 --audio ./gan/welcome.wav --results_dir ./video'
    subprocess.call(lipGAN,shell=True)
    commander="ffmpeg -i './video/result_voice.avi' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 './video/result_voice.mp4'"
    subprocess.call(commander,shell=True)
    commander2="ffmpeg -i './video/result.avi' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 './video/result.mp4'"
    subprocess.call(commander2,shell=True)
    os.chdir('..')
    input_video = ffmpeg.input('./result/video/result.mp4')
    # if gen=="Male":
    #     input_audio1 = ffmpeg.input('./result/audio/welcome.wav')
    # else:
    #     input_audio1 = ffmpeg.input('./result/gan/welcome.wav')
    input_audio1 = ffmpeg.input('./result/audio/welcome.wav')
    ffmpeg.concat(input_video, input_audio1, v=1, a=1).output('./media/Videos/translated'+orgfile).run()

    transfilenaam='./media/Videos/'+filenaam
    if gen=="Male":
        shutil.copy('./result/video/result_voice.mp4',transfilenaam)

    finalpath=orgfile
    return gen,finalpath
