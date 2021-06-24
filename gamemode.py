# -*- coding: utf-8 -*-

import re
import time
import os

def on_player_joined(server, player):
  if os.path.exists('./plugins/gm/' + player):
    server.execute("gamemode spectator " + player)

def on_load(server, old):
    server.add_help_message('!!gm', '切换玩家模式')
    server.add_help_message('!!gm [ID]', '管理员强制切换切换玩家模式(限制权限admin)')
    if not os.path.exists('./plugins/gm/'):
      os.makedirs('./plugins/gm/')

def on_info(server, info):
  PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
  dimension_convert = {"0":"overworld","-1":"the_nether","1":"the_end","minecraft:overworld":"overworld","minecraft:the_nether":"the_nether","minecraft:the_end":"the_end"}
  per = server.get_permission_level(info)
  if info.content.startswith('!!gm') and info.is_player == 1:
    if per >= 1:
      gm = info.content.split(" ")
      if len(gm) == 2 and per == 3:
          server.tell(info.player, '即将更改玩家 §6{0} §r的 §a游戏模式!'.format(gm[1]))
          if os.path.exists('./plugins/gm/' + gm[1]):
            server.tell(gm[1], '§6正在更改模式，请不要走动!')
            time.sleep(1)
            f = open('plugins/gm/' + gm[1], 'r')
            zub = f.read()
            zub = zub.replace('\n', '').replace('\r', '')
            f.close()
            os.remove('plugins/gm/' + gm[1])
            xyz = zub.split("|")
            server.execute("execute at " + gm[1] + " in minecraft:" + xyz[3] + " run tp " + gm[1] + " " + xyz[0] + " " + xyz[1] + " " + xyz[2])
            server.execute("gamemode survival " + gm[1])
          else:
            server.tell(gm[1], '§6正在更改模式，请不要走动!')
            time.sleep(1)
            os.system('cd plugins/gm && echo " " > ' + gm[1])
            pos = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Pos')
            dim = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Dimension')
            f = open('./plugins/gm/' + gm[1], 'w')
            f.write(str(pos[0])+'|'+str(pos[1])+'|'+str(pos[2])+'|'+dimension_convert[str(dim)])
            f.close()
            server.execute("gamemode spectator " + gm[1])
            server.tell(gm[1], '§6已切换到观察者模式,要切换回来请!!gm')
      elif len(info.content) != 4:
        server.tell(info.player, '§6装你妈的B')
      elif os.path.exists('./plugins/gm/' + info.player):
        server.tell(info.player, '§6正在更改模式，请不要走动!')
        time.sleep(1)
        f = open('plugins/gm/' + info.player, 'r')
        zub = f.read()
        zub = zub.replace('\n', '').replace('\r', '')
        f.close()
        os.remove('plugins/gm/' + info.player)
        xyz = zub.split("|")
        server.execute("execute at " + info.player + " in minecraft:" + xyz[3] + " run tp " + info.player + " " + xyz[0] + " " + xyz[1] + " " + xyz[2])
        server.execute("gamemode survival " + info.player)
      else:
        server.tell(info.player, '§6正在更改模式，请不要走动!')
        time.sleep(1)
        os.system('cd plugins/gm && echo " " > ' + info.player)
        pos = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Pos')
        dim = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Dimension')
        f = open('./plugins/gm/' + info.player, 'w')
        f.write(str(pos[0])+'|'+str(pos[1])+'|'+str(pos[2])+'|'+dimension_convert[str(dim)])
        f.close()
        server.execute("gamemode spectator " + info.player)
        server.tell(info.player, '§6已切换到观察者模式,要切换回来请!!gm')
    else:
      server.tell(info.player, '你没有权限')
