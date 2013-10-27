import subprocess
import pipes
import shlex

import sys

class BuildError(Exception):
	pass

class RunError(BuildError):
	pass

def run(command, path):
	args = shlex.split(command)
	result = subprocess.Popen(args, cwd=path, stdout=sys.stdout,
		stderr=subprocess.STDOUT)
	result.wait()

	# print(result.stdout.read())
	# if result.stderr:
		# print(result.stderr.read())
	if result.returncode > 1:
		raise RunError("{0} exited with code {1}".format(args[0], result.returncode))

def configure(config, path, buildpath):
	try:
		commands = config["configure"]

		# Horribly un-Pythonicly, check if we have a string
		if isinstance(commands, str) or isinstance(commands, unicode):
			commands = [ commands ]

		for command in commands:
			print("      Running {0}".format(command))

			config_command = command.format(pipes.quote(buildpath))
			run(config_command, path)

	except RunError:
		raise BuildError("Configure failed")

def build(config, path, buildpath):
	try:
		configure(config, path, buildpath)
		print("      Done configure")
	except KeyError:
		# Ignore a missing configure command
		print("      Skipping configure")
		return

	commands = config["build"]
	if isinstance(commands, str) or isinstance(commands, unicode):
		commands = [ commands ]

	for command in commands:
		print("      Running {0}".format(command))
		run(command, path)

