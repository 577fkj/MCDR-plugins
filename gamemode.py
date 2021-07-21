# -*- coding: utf-8 -*-
import re
import os
from time import sleep

PLUGIN_METADATA = {
	'id': 'Gamemode',
	'version': '1.0.0',
	'name': 'Gamemode',
	'author': [
		'57767598'
   ],
	'link': 'https://github.com/577fkj/MCDR-plugins/'
}

gm_user = 0

def process_coordinate(text):
	data = text[1:-1].replace('d', '').split(', ')
	data = [(x + 'E0').split('E') for x in data]
	return tuple([float(e[0]) * 10 ** int(e[1]) for e in data])


def process_dimension(text):
	return text.replace(re.match(r'[\w ]+: ', text).group(), '', 1)


def display(server, name, position, dimension):
	server.tell(name, '§6将在3秒后切换游戏模式')
	sleep(3)
	if position != ():
		x, y, z = position
	else:
		x, y, z = (0, 0, 0)
	dimension = dimension.replace('"', '').replace('\n', '')
	if os.path.exists('./plugins/gm/' + name + '.gmpos'):
		with open('./plugins/gm/' + name + '.gmpos', 'r') as f:
			pos_data = f.read()
		pos_data = pos_data.split('$')
		print('execute at {0} as {0} in {1} run tp {2} {3} {4}'.format(name, pos_data[0], pos_data[1], pos_data[2], pos_data[3]))
		server.execute('execute at {0} as {0} in {1} run tp {2} {3} {4}'.format(name, pos_data[0], pos_data[1], pos_data[2], pos_data[3]))
		server.execute('gamemode survival {}'.format(name))
		os.remove('./plugins/gm/' + name + '.gmpos')
		server.tell(name, '§6已切换到生存模式!')
	else:
		with open('./plugins/gm/' + name + '.gmpos', 'w') as f:
			f.write('%s$%s$%s$%s' % (dimension, x, y, z))
		server.execute('gamemode spectator {}'.format(name))
		server.tell(name, '§6已切换到旁观者模式!')


def on_info(server, info):
	global gm_user
	position = ()
	dimension = ''
	if info.is_player and info.content == '!!gm':
		if hasattr(server, 'MCDR') and server.is_rcon_running():
			name = info.player
			if not os.path.exists('./plugins/gm/' + name + '.gmpos'):
				position = process_coordinate(re.search(r'\[.*\]', server.rcon_query('data get entity {} Pos'.format(name))).group())
				dimension = process_dimension(server.rcon_query('data get entity {} Dimension'.format(name)))
			display(server, name, position, dimension)
		else:
			gm_user += 1
			if not os.path.exists('./plugins/gm/' + info.player + '.gmpos'):
				server.execute('data get entity ' + info.player)
			else:
				display(server, info.player, position, dimension)
	if not info.is_player and gm_user > 0 and re.match(r'\w+ has the following entity data: ', info.content) is not None:
		name = info.content.split(' ')[0]
		dimension = re.search(r'(?<= Dimension: )(.*?),', info.content).group().replace('"', '').replace(',', '')
		position_str = re.search(r'(?<=Pos: )\[.*?\]', info.content).group()
		position = process_coordinate(position_str)
		display(server, name, position, dimension)
		gm_user -= 1


def on_load(server, old):
	server.register_help_message('!!gm', '切换旁观者/生存')
	if not os.path.exists('./plugins/gm/'):
		os.mkdir('./plugins/gm/')
