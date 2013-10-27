from __future__ import print_function

import importlib
import re

import pygit2

class FetchError(Exception):
	pass

class Fetcher(object):
	def __init__(self, name):
		self.name = name

	def fetch(self, version, path):
		pass

class GitFetcher(Fetcher):
	url = ""
	patterns = []

	def __init__(self, name, config=None):
		super(GitFetcher, self).__init__(name)

		self.url = config["url"]
		self.patterns = config["patterns"]

	def fetch(self, path, version):
		try:
			self.repo = pygit2.Repository(path)
			print("  Updating {0} from {1}".format(self.name, self.url))
			self.update(path)
		except KeyError:
			print("  Cloning {0} from {1}".format(self.name, self.url))
			self.clone(path)

		ref = self.map_version_to_ref(version)
		print("  Checking out version {0} from {1}".format(version, ref))
		self.checkout(ref)

	def progress(self, message):
		print("    ", message, end="")

	def determine_wants(self, refs):
		# retrieve all objects
		return refs.values()

	def update(self, path):
		self.repo.remotes[0].fetch()

	def clone(self, path):
		self.repo = pygit2.clone_repository(self.url, path)

	def map_version_to_ref(self, version):
		ref = version
		for pattern, replacement in self.patterns:
			ref = re.sub(pattern, replacement, ref)
		return ref

	def checkout(self, ref):
		try:
			# Check if it's a reference, and if not, assume it's a tag
			if not ref in self.repo.listall_references():
				ref = "refs/tags/{0}".format(ref)

			self.repo.checkout(ref)
		except KeyError as e:
			raise FetchError("Invalid version or reference ({0})".format(ref))

def map(extension, fetchable):
	try:
		config = fetchable[extension]
		try:
			if config["type"] == "git":
				return GitFetcher(extension, config)
		except KeyError:
			config["type"] = "__MISSING__"

		raise FetchError("Invalid fetchable type ({0}) for {1}".format(config["type"], extension))
	except KeyError:
		raise FetchError("Cannot fetch {0}".format(extension))
