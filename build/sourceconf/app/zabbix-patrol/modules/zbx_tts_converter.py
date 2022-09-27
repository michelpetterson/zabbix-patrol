# coding=utf-8
from __future__ import print_function
import os
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
import extras.ftp_upload as ftp
import datetime
from datetime import date
import time

from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config/zpconfig.ini')

timenow = datetime.datetime.now()

def tts_converter(triggeridlist):
    service = TextToSpeechV1(
        url = cfg.get('ibm-watson', 'watson_api_url'),
        iam_apikey = cfg.get('ibm-watson', 'watson_api_token'))

    filename = "/tmp/issue_tid" + '_'.join(map(str, triggeridlist)) + ".txt"
    with open(filename, "r") as f:
        data = f.readlines()
    #print(data)

    # Synthesize using websocket. Note: The service accepts one request per connection
    if os.path.exists("/tmp/issue.mp3"):
        os.remove("/tmp/issue.mp3")
    file_path = join(dirname(__file__), "/tmp/issue.mp3")

    class MySynthesizeCallback(SynthesizeCallback):
        def __init__(self):
            SynthesizeCallback.__init__(self)
            self.fd = open(file_path, 'ab')

        def on_connected(self):
            print(timenow, '- Watson API: The connection was established.')

        def on_error(self, error):
            print(timenow, '- Watson API:  Error received: {}'.format(error))

        def on_content_type(self, content_type):
            print(timenow, '- Watson API: Content type: {}'.format(content_type))

        def on_timing_information(self, timing_information):
            print(timing_information)

        def on_audio_stream(self, audio_stream):
            self.fd.write(audio_stream)

        def on_close(self):
            self.fd.close()
            print(timenow, '- Watson API: Text conversion successful.')

    my_callback = MySynthesizeCallback()
    service.synthesize_using_websocket(str(data),
                                       my_callback,
                                       accept='audio/mp3',
                                       voice='pt-BR_IsabelaV3Voice'
                                       )
    ftp.ftp_upload(triggeridlist)
    if os.path.exists(filename):
        os.remove(filename)
