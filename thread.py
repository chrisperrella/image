import threading, subprocess

class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout=100, **kwargs):
		def target(**kwargs):
			self.process = subprocess.Popen(self.cmd, **kwargs)
			self.process.communicate()

		thread = threading.Thread(target=target, kwargs=kwargs)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			thread.join()

		return self.process.returncode