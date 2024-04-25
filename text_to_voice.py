import argparse
import requests
import time
from Data import Api_key



def synthesize(text):
   url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
   headers = {
       'Authorization': 'Api-key ' + Api_key,
   }


   data = {
       'text': text,
       'lang': 'ru-RU',
       'voice': 'filipp',
   }

   with requests.post(url, headers=headers, data=data, stream=True) as resp: #Генерируем POST запрос к серверу и посылаем его
       if resp.status_code != 200:
           raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

       for chunk in resp.iter_content(chunk_size=None):
           yield chunk # Возврашаем полученные чанки


   #args = parser.parse_args()
def enter_text(text):
  output_name = "unswer"

  with open(output_name + ".ogg", "wb") as f:
      for audio_content in synthesize(text): # Записываем чанки в переменную
         f.write(audio_content) #Записываем чанки в файл
         print("success")


