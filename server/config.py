import imp
from os import environ
from os.path import isfile
from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader


__all__ = ['CONFIG', 'get_param']


def get_param(key, default=False):
	key = key.upper()
	return environ.get(key, default)


CONFIG_FILE = get_param('config_file', 'config.yml')

CONFIG = {}
if isfile(CONFIG_FILE):
	with open(CONFIG_FILE, 'r') as file:
		CONFIG = load(file, Loader=Loader)
else:
	print('config file required')
	exit(1)
