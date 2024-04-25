import text_to_voice as ttv
import voice_to_text as vtt
import speech_recognition
from Data import IAM_TOKEN, FOLDER_ID, Api_key
import soundfile as sf
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

number_task = input('1 - Voice to text, 2 - Text to voice: ')
if number_task == "2":
    text_task = input('Введите текст, который необходиммо озвучить: ')
    ttv.enter_text(IAM_TOKEN,FOLDER_ID,text_task)


elif number_task == "1":
   # recognizer = speech_recognition.Recognizer()
   # microphone = speech_recognition.Microphone()

            # старт записи речи с последующим выводом распознанной речи
            voice_input = vtt.record_and_recognize_audio()
            data, samplerate = sf.read('unswer.ogg')  # Записываем запись с wav в переменную
            sf.write('unswer.wav', data, samplerate)
            song = AudioSegment.from_ogg("unswer.wav")
            play(song)
            print(voice_input)


