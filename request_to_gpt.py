import requests
import os
import json
from Connect_DB import connecting
from Data import Api-key

def gpt(text):
    

    headers = {
        'Authorization': f'Api-Key {Api_key}',
    }

    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    #file_object = open('file_1.json', 'a', encoding='utf-8')
    #file_object.write(', \n' + "    " + '{ \n' + "      " + '"role": "user",\n' + "      " + '"text": "' + text + '" \n' + "    " + '}')
    #file_object.close()

    file_object_1 = open('file_1.json', 'r', encoding='utf-8')
    tmp = file_object_1.read()

    file_time = open('file_time.json', 'w', encoding='utf-8')

    file_time.write(tmp)
    file_time.write(', \n' + "    " + '{ \n' + "      " + '"role": "user",\n' + "      " + '"text": "' + text + '" \n' + "    " + '}') # copy from 13-16
    file_time.write('\n' + "  " + ']\n }')

    file_object_1.close()
    file_time.close()

    with open('file_time.json', 'r', encoding='utf-8') as f:
        data = json.dumps(json.load(f))

    resp = requests.post(url, headers=headers, data=data)

    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {resp.status_code}, {resp.text}
            )
        )
    data = json.loads(resp.text)
    data = data['result']
    data = data['alternatives'][0]
    data = data['message']
    data1 = data['text']

   # file_object = open('file.json', 'a', encoding='utf-8')
   # file_object.write( ', \n' + "    " + '{ \n' + "      " + '"role": "assistant",\n' + "      " + '"text": "' + data1 + '" \n' + "    " + '}')
   # file_object.close()
    data1 = data1.replace("```\n","")
    data1 = data1.replace("\n```", "")

    print(data1)
    result = connecting(data1)

    return result
