#百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json



def translate(text,source_language,dest_language):
    appid = '20200114000375394'  # 填写你的appid
    secretKey = '4RZfDTeh4ZE1ZSB6NWuO'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = source_language   #原文语种
    toLang = dest_language   #译文语种
    salt = random.randint(32768, 65536)
    q=text
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        return result['trans_result'][0]['dst']

    except Exception as e:
        return e
    finally:
        if httpClient:
            httpClient.close()