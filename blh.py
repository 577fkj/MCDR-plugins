# -*- coding: utf-8 -*-
#encoding=utf8
import sys
import os
import requests
import json
import time
#sys.path.append('..')
#import blivedm
import asyncio

startblh = []
stopallblh = False
stopblh = []

helpmsg ='''§4------577-B站弹幕插件------
§6!!blh list -查看列表
§6!!blh add [ID] [Name] -添加房间
§6!!blh start [ID] -启动弹幕姬
§6!!blh stop [ID] -停止弹幕姬
§6!!blh stop-all -停止全部房间弹幕姬
§4-------------------------'''

def on_load(server, old):
  server.add_help_message('!!blh', 'BiliBili弹幕姬')

def on_info(server, info):
  if info.is_player == 1:
    if info.content.startswith('!!blh'):
      blhlist = []
      with open('./plugins/blh/list.json') as handle:
        for line in handle.readlines():
          blhlist.append(line.replace('\n','').replace('\r',''))
      args = info.content.split(' ')
      if (len(args) == 1):
        for line in helpmsg.splitlines():
          server.tell(info.player, line)
      elif (len(args)==2):
        if args[1] == 'list':
          num = 0
          server.tell(info.player, '§bID-名字-房间号')
          for line in blhlist:
            llist = line.split('-')
            server.tell(info.player, '§7' + str(num) + ' §6' + llist[1] + ' §b' + llist[0])
            num += 1
        if args[1] == 'stop-all':
          global stopallblh
          stopallblh = True
      elif (len(args) == 4):
        if args[1] == 'add':
          if server.get_permission_level(info) >= 3:
            os.system('cd plugins/blh && echo ' + args[2] + '-' + args[3] + '>> list.json')
            server.say('§b[BLH]§r添加成功!')
          else:
            server.say('§b[BLH]§r你没有权限!')
      elif (len(args) == 3):
        lst = []
        if args[1] == 'start':
          for line in blhlist:
            llist = line.split('-')
            lst.append(llist)
          try:
            if lst[int(args[2])][1] == '':
              print('1')
          except:
            server.say('[§bBLH§r] §4ID§r错误')
          global startblh
          global stopblh
          stopallblh = False
          try:
            stopblh.remove(args[2])
          except:
            print('error remove stop list')
          if lst[int(args[2])][1] in startblh:
            server.say('[§bBLH§r] §c' + lst[int(args[2])][1] + '§r的直播间已被订阅')
          else:
            #asyncio.get_event_loop().run_until_complete(blh(server,lst[int(args[2])][0],lst[int(args[2])][1],int(args[2])))
            blh(server,lst[int(args[2])][0],lst[int(args[2])][1],int(args[2]))
        elif args[1] == 'stop':
          stopblh.append(args[2])
        else:
          server.say('[§bBLH§r] §r未知命令,请输入!!blh查看帮助!')

def blh(server,id,name,id1):
  global startblh
  startblh.append(name)
  url='https://api.live.bilibili.com/ajax/msg'
  form={'roomid': id}
  requests.adapters.DEFAULT_RETRIES = 5
  requests.packages.urllib3.disable_warnings()
  try:
    html = requests.post(url,data=form)
    json1=html.json()
    old = json1['data']['room'][len(json1['data']['room']) - 1]['nickname'] + ':' + json1['data']['room'][len(json1['data']['room']) - 1]['text'] + '|' + json1['data']['room'][len(json1['data']['room']) - 1]['timeline']
  except:
    print('post error!')
  server.say('[§bBLH§r]§r已订阅:§c' + name + '§r的直播间')
  server.say('[§bBLH§r]§c[' + name + ']§r' + json1['data']['room'][len(json1['data']['room']) - 1]['nickname'] + ':' + json1['data']['room'][len(json1['data']['room']) - 1]['text'])
  while True:
    global stopblh
    global stopallblh
    if stopallblh == True:
      server.say('[§bBLH§r] §r已停止对§c' + name + '§r直播间的订阅')
      break
    if str(id1) in stopblh:
      stopblh.remove(str(id1))
      server.say('[§bBLH§r] §r已停止对§c' + name + '§r直播间的订阅')
      break
    requests.adapters.DEFAULT_RETRIES = 5
    requests.packages.urllib3.disable_warnings()
    try:
      html = requests.post(url,data=form)
      json1=html.json()
      if old != json1['data']['room'][len(json1['data']['room']) - 1]['nickname'] + ':' + json1['data']['room'][len(json1['data']['room']) - 1]['text'] + '|' + json1['data']['room'][len(json1['data']['room']) - 1]['timeline']:
        old = json1['data']['room'][len(json1['data']['room']) - 1]['nickname'] + ':' + json1['data']['room'][len(json1['data']['room']) - 1]['text'] + '|' + json1['data']['room'][len(json1['data']['room']) - 1]['timeline']
        server.say('[§bBLH§r]§c[' + name + ']§r' + json1['data']['room'][len(json1['data']['room']) - 1]['nickname'] + ':' + json1['data']['room'][len(json1['data']['room']) - 1]['text'])
    except:
      print('post error!')
    s = requests.session()
    s.keep_alive = False
    time.sleep(0.5)

    

# async def blh(server,id,name,id1):
#   client = MyBLiveClient(id, ssl=True, server=server, idm=name)
#   future = client.start()
#   server.say('[§bBLH§r]§r已订阅:§c' + name + '§r的直播间')
#   while True:
#     global stopblh
#     global stopallblh
#     if stopallblh == True:
#       server.say('[§bBLH§r] §r已停止对§c' + name + '§r直播间的订阅')
#       future.cancel()
#       break
#     if str(id1) in stopblh:
#       stopblh.remove(str(id1))
#       server.say('[§bBLH§r] §r已停止对§c' + name + '§r直播间的订阅')
#       future.cancel()
#       break

# class MyBLiveClient(blivedm.BLiveClient):
#     async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
#         #print(f'{danmaku.uname}：{danmaku.msg}')
#         server.say(f'[§bBLH§r]§c[' + self.idm + ']§r{danmaku.uname}：{danmaku.msg}')
