#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# omikuji_get.py  : おみくじ収集
# function        : cotogotoのボットNovyからおみくじデータを取得する。
#                   https://app.cotogoto.ai/webapi/console.do
# 2019/01/16 New Create K.Ohe
#
import requests
import json
import types

ENDPOINT = 'https://www.cotogoto.ai/webapi/noby.json'
MY_KEY = 'ba11c91a702220bba16d0769d8ebf92f'

for i in range(800) :
  payload = {'text': 'おみくじ引きたいな。', 'app_key': MY_KEY}
  r = requests.get(ENDPOINT, params=payload)
  data = r.json()
  text = data['text'].splitlines()
  fname = text[0].split()
  fname = 'data/' + text[0] + '.txt'
  f = open(fname, mode='w')
  f.write(data['text'])
  f.close()
  print (i + 1, fname)
  #print (text[1])