import yaml, os, re, glob
import importlib.util

yaml.warnings({'YAMLLoadWarning': False})

class World():
	def __init__(self, folder):
		self.rooms = {}
		self.objects = {}
		self.metadata = {}

		for f in glob.glob('{}/**/*.yml'.format(os.path.abspath(folder)), recursive=True):
			self._load_yml_file(f)

	def _load_yml_file(self, f):
		pass