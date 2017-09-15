# -*- coding: utf-8 -*-
import requests
from xml.dom.minidom import parseString
import subprocess
import shutil
import time


# Размер блока данных (chunk).
CHUNK_SIZE = 2000
TMP_FILE = 'out/tmp.dat'
YANDEX_KEY = '34e2d365-85d7-42c8-8a57-21d3f5424788';
UUID = 'cafebabe253300000000000000000000'

def sound_to_text(filename, topic):
    # Сохраняет блок данных (chunk) в файл, который передан в argv[2].
    with open(TMP_FILE, 'w') as output:

        # Исходные аудио данные содержатся в файле, который передан в argv[1].
        with open(filename, 'r') as content_file:

            content = content_file.read()

            while len(content) > 0:
                size = min(len(content), CHUNK_SIZE)
                output.write(hex(size)[2:])
                output.write('\r\n')
                output.write(content[:size])
                output.write('\r\n')
                content = content[size:]
            output.write('0\r\n\r\n')

    with open(TMP_FILE, 'r') as chunked:
        headers = {
            'Transfer-Encoding': 'chunked',
            'Content-Type': 'audio/x-wav'
        }
        r = requests.post('https://asr.yandex.net/asr_xml?uuid={}&key={}&topic={}&lang=ru-RU&disableAntimat=true'.format(
            UUID, YANDEX_KEY, topic
        ), data=chunked, headers=headers, verify=False)

        dom = parseString(r.text.encode('utf-8'))
        return [v.firstChild.nodeValue for v in dom.getElementsByTagName('variant')]


# print sound_to_text('out/output_1505479615.wav', 'numbers')

def play_text(text):
    r = requests.get(
        url='https://tts.voicetech.yandex.net/generate?format=wav&lang=ru-RU&speaker=zahar&emotion=good&key={}'.format(YANDEX_KEY),
        params={'text': text},
        verify=False,
        stream=True
    )

    file_name = 'out/recognized_{}.wav'.format(str(int(time.time())))
    with open(file_name, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    subprocess.call(["afplay", file_name])


# play_text("Привет, детка! Как дел+а? Давай дружить?")