#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===================================================================
#
# omikuji_print.py  : おみくじをレシートプリンタPOS-5805DDで印刷する。
#                     i以下のWebAPIを利用
#                   https://app.cotogoto.ai/webapi/console.do
#  History    : v0.9  2019/01/16 New Create K.Ohe
#               v1.0  2019/01/17 例外処理を追加 
#===================================================================
#
from escpos import *
from pathlib import Path
import random
import numpy
import nkf
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

from time import sleep
import datetime

import requests
import json
import types

#========================================
# global definition
#========================================
g_pos_y = 0
ENDPOINT = 'https://www.cotogoto.ai/webapi/noby.json'
MY_KEY = 'ba11c91a702220bba16d0769d8ebf92f'

#========================================
# function : draw_text : text to img
#========================================
def draw_text(img, text, align='left', size=24):
  global g_pos_y
  draw = PIL.ImageDraw.Draw(img)
#  draw.font = PIL.ImageFont.truetype('ume-hgo5.ttf', size)
  draw.font = PIL.ImageFont.truetype('UtsukushiFONT.otf', size)
#    'AquaKana.ttc', size)

  img_size = numpy.array(img.size)
  txt_size = numpy.array(draw.font.getsize(text))
#  pos = (img_size - txt_size) / 2

  if align == 'center':
    x = ((img_size - txt_size) / 2)[0]
  elif align == 'right':
    x = (img_size - txt_size)[0]
  else:
    x = 0

  #draw.text(pos, text, (0, 0, 0))
  draw.text((x, g_pos_y), text, (0, 0, 0))
  g_pos_y += (size + 4)

#========================================
# function : creat_img : make omikuji bitmap
#========================================
def create_img(name, tenki, kuji, honbun):
  global g_pos_y
  g_pos_y = 0

  img = PIL.Image.new('RGB', (384, 1000), (255,255,255))
  date = datetime.datetime.today().strftime("%Y/%m/%d")

#  draw_text(img, ' ')
  draw_text(img, ' ')
  draw_text(img, date, align='center', size=28)
  draw_text(img, ' ')
  draw_text(img, name + ' 局長殿', align = 'center', size=40)
  draw_text(img, ' ')
  u = tenki.split('、')
  for v in u:
    draw_text(img, v, align = 'center', size = 32)
  draw_text(img, ' ')
  draw_text(img, '================================')
  draw_text(img, 'ＫＤＮおみくじ', align='center', size=48)
  draw_text(img, '================================')
  draw_text(img, ' ')
  kuji = kuji.split()
  draw_text(img, kuji[0], align='center', size = 36)
  draw_text(img, ' ')
  draw_text(img, kuji[1], align='center', size = 36)
  draw_text(img, ' ')
  u = nkf.nkf('-f22', honbun).decode('utf-8').splitlines() 
  for v in u:
    draw_text(img, v, size = 32)
  
  gray = img.convert('L')
  img = gray.point(lambda x: 0 if x < 128 else 255)
#  img.show()
  img.save('output.png')
  return img


#========================================
# function : put_file : save omikuji data
#========================================
def put_file(data):
  text = data['text'].splitlines()
  fname = text[0].split()
  fname = 'data/' + text[0] + '.txt'
  f = open(fname, mode='w')
  f.write(data['text'])
  f.close()

#========================================
# function : get_file : get 1 of files
#========================================
def get_file() :
  p = Path('data/')
  try :
    l = list(p.glob("*.txt"))
    r = random.randrange(len(l))
    f = open(l[r], mode = 'r')
    data = f.readlines()
  except :
    data = ['第零番　大凶', '最悪の運勢です。今日はろくなことがありません。一日家にこもって外出を控えましょう。']
  return data

#========================================
# function : main : get omikuji data and print
#========================================
def main():
  names = [
    'JA1AOQ',
#    'JA1AOQ',
  ]

  for name in names:
    payload = {'text': '今日の東京の天気は', 'app_key': MY_KEY}
    try :
      r = requests.get(ENDPOINT, params=payload)
      data = r.json()
      tenki = data['text']
    except :
      tenki = '、'
  
    payload = {'text': 'おみくじ引きたいな。', 'app_key': MY_KEY}
    try :
      r = requests.get(ENDPOINT, params=payload)
      data = r.json()
      put_file(data)
      work = data['text'].splitlines()
    except :
      work = get_file()

    kuji = work[0]
    honbun = work[1]

    img = create_img(name, tenki, kuji, honbun)
    sleep(0.5)
    try :
      p = printer.Serial("/dev/tty.BlueToothPrinter-HS_SPP")
      p.image('output.png')
#      p.text('\n\n\n')
#      sleep(0.5)
    except :
      img.show()

#    p.qr(data['text'])

#========================================
# function : main routine
#========================================
main()
