from __future__ import print_function

import yaml
import os.path
import shlex
import pipes
import subprocess

import buildtool.fetcher
import buildtool.builder

class InstallError(Exception):
	pass

class Installer(object):
	def __init__(self, config, fetchable):
		self.config = config
		self.fetchable = fetchable
		self.extensions = {}

	def install(self, basedir, release):
		# Prepare directories
		self.base = os.path.join(basedir, release)
		if not os.path.exists(self.base):
			os.makedirs(self.base)

		self.builddir = os.path.join(self.base, "build")
		if not os.path.exists(self.builddir):
			os.makedirs(self.builddir)

		print("  Downloading PHP source")
		self.fetch("php", self.config["php"])

		print("  Downloading extension source")
		self.fetch_extensions()

		print("  Building extensions")
		self.build_extensions()

		print("  Building PHP")
		self.install_php()

		print("  Configuring")
		self.configure()

		print("Completed")
		print("----")

	def fetch(self, extension, version):
		# Prepare a space
		if extension == "php":
			path = os.path.join(self.base, "php-src")
		else:
			path = os.path.join(self.base, "ext-src", extension)
		if not os.path.exists(path):
			os.makedirs(path)

		# Work out how to fetch it
		try:
			fetcher = buildtool.fetcher.map(extension, self.fetchable)
		except ImportError:
			# Report this
			print("Fetcher not found for {0}".format(extension))
			return False

		# Then, actually try to fetch it
		try:
			print("    Downloading source for {0}".format(extension))
			fetcher.fetch(path, version)
		except buildtool.fetcher.FetchError as e:
			# Report this too
			print("Error fetching {0}: {1}".format(extension, e.message))
			return False

		self.extensions[extension] = path
		print("    Downloaded")
		print("    ----")

		return True

	def fetch_extensions(self):
		success = True
		for extension, version in self.config.iteritems():
			# Ignore explictly-ignored extensions
			if not version:
				continue

			# Handle PHP separately
			if extension == "php":
				continue

			success = success and self.fetch(extension, version)

		if not success:
			raise InstallError("Could not fetch all extensions")

	def build_extensions(self):
		extensions = self.extensions.copy()
		completed = ["php"]
		del extensions["php"]

		while len(extensions) > 0:
			for extension, path in extensions.iteritems():
				if extension in completed:
					continue

				config = self.fetchable[extension]

				# Check dependencies
				try:
					deps = config["requires"]
				except KeyError:
					deps = []

				try:
					prereqs = deps + config["after"]
				except KeyError:
					prereqs = deps

				# Check hard dependencies first
				for dep in deps:
					if dep not in self.extensions.keys():
						raise InstallError("{0} requires {1}".format(extension, dep))

				# Check prereqs
				missing = False
				for prerequisite in prereqs:
					if prerequisite not in completed:
						missing = True
						break
				if missing:
					continue

				print("    Starting {0}".format(extension))
				buildtool.builder.build(config, path, self.builddir)

				# Mark as complete
				completed.append(extension)
				print("    Completed build")
				print("    ----")

			for extension in completed:
				try:
					del extensions[extension]
				except KeyError:
					pass


	def install_php(self):
		import sys
		path = os.path.join(self.base, "php-src")

		print("    Running buildconf")
		print(subprocess.call(["./buildconf", "--force"], cwd=path, stdout=sys.stdout, stderr=subprocess.STDOUT))

		args = ["./configure"]
		print(self.extensions)
		for extension, srcpath in self.extensions.iteritems():
			if extension == "php":
				continue

			args.append("--with-{0}={1}".format(extension, pipes.quote(srcpath)))

		args.append("--prefix={0}".format(pipes.quote(self.builddir)))

		print("    Running configure")
		subprocess.call(args, cwd=path, stdout=sys.stdout, stderr=subprocess.STDOUT)

		print("    Running make")
		subprocess.call(["make"], cwd=path, stdout=sys.stdout, stderr=subprocess.STDOUT)

	def configure(self):
		pass


def install_all(config, fetchable):
	basedir	= os.path.expandvars(config['basedir'])
	basedir	= os.path.expanduser(config['basedir'])
	basedir = os.path.abspath(basedir)

	for release, extensions in config['builds'].iteritems():
		print("Starting build {0}".format(release))
		try:
			installer = Installer(extensions, fetchable)
			installer.install(basedir, release)
		except InstallError as err:
			print(err)

def run():
	with open("config.yaml", "r") as f:
		data = yaml.load(f)

	with open("fetchable.yaml", "r") as f:
		fetchable = yaml.load(f)

	install_all(data, fetchable)
