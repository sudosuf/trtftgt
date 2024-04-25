import urllib.request
import json
import soundfile as sf
from pydub import AudioSegment
import speech_recognition
from Data import IAM_TOKEN, FOLDER_ID
import asyncio
from request_to_gpt import gpt as GPT
from text_to_voice import enter_text as ET

recognizer = speech_recognition.Recognizer()
microphone = speech_recognition.Microphone()


def recognite_voice(audio, token, folder_id):
    """Данная функция принимает записанный голос с микрофона, привотит к формату ogg (Изначально аудиозапись записываеться в формат wav) и посылает его на распознавание в Yandex SpeechKit"""
    with open('your_file.wav', 'wb') as file:
        wav_data = audio.get_wav_data()  # Приводим запись к wav формату
        file.write(wav_data)  # Записываем запись в файл
    data, samplerate = sf.read('your_file.wav')  # Записываем запись с wav в переменную
    sf.write('your_file.ogg', data, samplerate)
    #sound = AudioSegment.from_wav('your_file.wav')
    #sound.export('your_file.ogg', format='ogg')

    with open("your_file.ogg", "rb") as f:
        data = f.read()

    params = "&".join([
        "topic=general",
        "folderId=%s" % folder_id,
        "lang=ru-RU"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data) # Формируем тело запроса к серверу
    # Аутентификация через IAM-токен.
    url.add_header("Authorization", "Bearer %s" % token) # Добавляем заголовок для файла запроса

    responseData = urllib.request.urlopen(url).read().decode('UTF-8') # Отправляем запрос на сервер и получаем от него ответ.
    decodedData = json.loads(responseData) # Приводим ответ к JSON структуре
    print(json.loads(responseData))
    if decodedData.get("error_code") is None:
        print(decodedData.get("result")) # Печатаем груфу rezult из JSON файла

        result = GPT(decodedData.get("result"))
        ET(result)


def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=0.5)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 29)  # Запись звука с микрофона в еременную audio listen(ресурс, время ожидания, время записи)

            print("Started recognition...")
            recognite_voice(audio, IAM_TOKEN, FOLDER_ID)  # Запрос к библионеки vvt для передачи audio на тексторизацию

        except speech_recognition.WaitTimeoutError:  # Ошибка доступа к микрофону
            print("Can you check if your microphone is on, please?")
            return
        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data
