# encoding:utf-8
import base64
import time
import wave

import requests
from pyaudio import PyAudio, paInt16

framerate = 160000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度 2bytes
FILEPATH = 'speech.wav'  # 设置语音文件保存位置
base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "eyzfnUmvEGS2P7XsGm3WQ4Pd"
SecretKey = "4uuEqKSbmLkkQWyY7Yrp3DWgrc7sLIg5"
HOST = base_url % (APIKey, SecretKey)


def getToken(host):
    res = requests.post(host)  # 获取 access_token
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=channels, rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []
    # count = 0
    t = time.time()
    print('正在录音...')
    while time.time() < t + 5:  # 秒
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def speech2text(speech_data, token, dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = 'ag2s'
    SPEECH = base64.b64encode(speech_data).decode('utf‐8')
    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }

    url = "https://vop.baidu.com/server_api"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # r=requests.post(url,data=json.dumps(data),headers=headers)
    print('正在识别...')
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result


if __name__ == '__main__':
    flag = 'y'
    while flag.lower() == 'y':
        print('请输入数字选择语言：')
        devpid = input('1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话\n')
        my_record()
        TOKEN = getToken(HOST)
        speech = get_audio(FILEPATH)
        result = speech2text(speech, TOKEN, int(devpid))
        print(result)
        flag = input('Continue?(y/n):')
