from . import BaseAssertion
import subprocess
import logging

class ExecuteCommand(BaseAssertion):
  def __init__(self, command, expected_exit_code=0, expected_stdout=None, expected_stderr=None, strip_output=True):
    self.command = command
    self.expected_exit_code = expected_exit_code
    self.stdout = expected_stdout
    self.stderr = expected_stderr
    self.strip_output = strip_output
    self.logger = logging.getLogger('monitor')
    super(ExecuteCommand, self).__init__()

  def get_process(self):
    return subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  def test(self):
    self.logger.debug("Executing command: {}".format(self.command))
    proc = self.get_process()
    stdout, stderr = proc.communicate()
    exit_code = proc.returncode

    if self.strip_output:
      stdout, stderr = stdout.strip(), stderr.strip()

    # Check expected_stdout and expected_stderr are bytes
    if (self.stdout and not isinstance(self.stdout, (bytes, bytearray))) or (self.stderr and not isinstance(self.stderr, (bytes, bytearray))):
      self.logger.error("expected_stderr and expected_stdout arguments must be a bytes object.")

    # Check stdout
    if self.stdout:
      self.logger.debug("Checking output for command is: {}".format(self.stdout))

      if stdout != self.stdout:
        self.logger.debug("Checking failed.\n\nstdout: {}\nexpected_stdout: {}".format(stdout, self.stdout))
        self.raise_failure()

    # Check stderr
    if self.stderr:
      self.logger.debug("Checking output for command is: {}".format(self.stderr))

      if stderr != self.stderr:
        self.logger.debug("Checking failed.\n\nstderr: {}\nexpected_stderr: {}".format(stderr, self.stderr))
        self.raise_failure()

    # Check status code
    self.logger.debug("Checking exit code for command is: {}".format(self.expected_exit_code))
    if self.expected_exit_code != exit_code:
      self.logger.debug("Checking failed.\n\exit_code: {}\nexpected_exit_code: {}".format(exit_code, self.expected_exit_code))
      self.raise_failure()


class ExecuteRemoteCommand(ExecuteCommand):
  def __init__(self, remote, *args, **kwargs):
    self.remote = remote
    super(ExecuteRemoteCommand, self).__init__(*args, **kwargs)

  def get_process(self):
    return subprocess.Popen("ssh {} \"{}\"".format(self.remote, self.command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
