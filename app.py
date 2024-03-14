from flask import Flask, render_template, Response, request, redirect,url_for
import argparse
from jinja2 import Environment, FileSystemLoader
from googletrans import Translator
#import base64
#import json
import whisper
import os
import struct
import io
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import speech_recognition as sr
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

def remove_bytes(buffer, start, end):
    fmt = '%ds %dx %ds' % (start, end-start, len(buffer)-end)  # 3 way split
    return b''.join(struct.unpack(fmt, buffer))

app = app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
 

@app.route("/")
def index():
    return render_template('index2.html')
@app.route('/test', methods=['GET'])
def test():
  mp3_file=AudioSegment.from_mp3('media/sampleSuper.mp3')
  
  wav_file=mp3_file.export('media/sampleSuper.wav',format='wav')
  sample_rate,audio_data=wavfile.read('media/sampleSuper.wav')
  np_data=np.asarray(audio_data,dtype=np.float32)
  print(mp3_file.duration_seconds)
  return Response(str(mp3_file.duration_seconds))
@app.route('/reci',methods=['POST'])
def receiver():
  
  data = request.get_data()
  data=remove_bytes(data,0,176)
  data=remove_bytes(data,len(data)-62,len(data))

  
  audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
  with open('media/voice.ogg','wb') as f:
    
    f.write(data)
    f.close()

     
  
  #print(data)
  
  
  return Response('data recived')
  
  

@app.route("/result",methods=['GET'])


def result():
    #print(data)
    #options=whisper.DecodingOptions(language='ja',task='translate', fp16=False)
    #results = whisper.decode(model,'sampleSuper.mp3', options)
    try:
      # file=io.BytesIO(data)
       model=whisper.load_model("small")
       result_src=model.transcribe('media/voice.ogg', language='ja', fp16=False)
       
       if len(result_src)!=0 :
          translator=Translator()
          result_tr=translator.translate(result_src['text'],dest="en")
          return render_template('index.html',result_jp=result_src['text'],result_en=result_tr.text)

       #print(result_en.text)
       #print(result_en)
       #print(result['text'])
       #content={result_jp:result_jp['text'],result_en:result_en}
    except :
        print ('an exception has been occured')

    return Response('There is something wrong')
   
# ...
    
    
 


if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
