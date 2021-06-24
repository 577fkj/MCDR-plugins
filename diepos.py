# -*- coding: utf-8 -*-

import re
import time

die_user = 0
die_name = []
playerlist = []

def tellMessage(server, player, msg):
  for line in msg.splitlines():
    server.tell(player, line)

def on_death_message(server, death_message):
  global die_user
  global die_name
  die_user+=1
  try:
    die_name.remove(death_message.split(" ")[0])
  except:
    pass
  die_name.append(death_message.split(" ")[0])
  if death_message.split(" ")[0] != '':
    server.execute('data get entity ' + death_message.split(" ")[0])

def on_info(server, info):
  global die_user
  global die_name
  dimension_convert = {"0":"主世界","-1":"地狱","1":"末地"}
  if("following entity data" in info.content):
    if die_user > 0:
      name = info.content.split(" ")[0]
      if name in die_name:
        try:
          die_name.remove(death_message.split(" ")[0])
        except:
          pass
        dimension = re.search("(?<=Dimension: )-?\d",info.content).group()
        position_str = re.search("(?<=Pos: )\[.*?\]",info.content).group()
        position = re.findall("\[(-?\d*).*?, (-?\d*).*?, (-?\d*).*?\]",position_str)[0]
        position_show = "[x:"+str(position[0])+",y:"+str(position[1])+",z:"+str(position[2])+"]"
        if dimension == '0':
          msg = " " + name + " §r死于 §2" + dimension_convert[dimension] + position_show
        elif dimension == '1':
          msg = " " + name + " §r死于 §5" + dimension_convert[dimension] + position_show
        elif dimension == '-1':
          msg = " " + name + " §r死于 §4" + dimension_convert[dimension] + position_show
        tellMessage(server, name, msg)
        die_user-=1
