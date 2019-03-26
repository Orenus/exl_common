
import paramiko
from exl_base.exl_conf import ExlConf
from exl_base.exl_logger import ExlLogger

logger = ExlLogger.instance()

class ExlSshUtils:
  def __init__(self, host, username, password, port = 22):
    self.client = None
    self.host = host
    self.username = username
    self.password = password
    self.port = port
    self.timeout = ExlConf.instance().get_int("ssh", "connection_timeout", 10*1000)

  def connect(self):
    connection_result = False
    logger.debug("Estsblishing ssh connection to {}:{}".format(self.host, self.port))

    self.client = paramiko.SSHClient()
    #Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
      self.client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password,timeout=self.timeout, allow_agent=False,look_for_keys=False)    
      logger.debug("Connected to ssh server @{}:{}".format(self.host, self.port))
    except paramiko.AuthenticationException:
      logger.error("Authentication failed, please verify your credentials")
    except paramiko.SSHException as sshException:
      logger.error("Could not establish SSH connection: {}".format(sshException))
    except socket.timeout as e:
      logger.error("Connection timed out @{}:{}".format(self.host, self.port))
      self.client.close()
    except Exception as ex:
       logger.error("Failed connecting to ssh server @{}:{} ERROR: {}".format(self.host, self.port, ex))
    else:
        connection_result = True

    return connection_result

  def execute_command(self, commands):
    """Execute a command on the remote host.Return a tuple containing
    an integer status and a two strings, the first containing stdout
    and the second containing stderr from the command."""
    exec_result = False
    try:
      if self.connect():
        for command in commands:
          logger.debug("Executing command >> {}".format(command))
          stdin, stdout, stderr = self.client.exec_command(command, timeout = 10)
          ssh_output = stdout.read()
          ssh_error = stderr.read()
          if ssh_error:
            logger.error("Problem occurred while running command: {} The error is {}".format(command, ssh_error))
            exec_result = False
          else:    
            logger.debug("Command result: {}".format(ssh_output))
            
            exec_result = False
       
    except Exception as ex:
        logger.error("Command execution failure: {}".format(ex))
        self.client.close()
        exec_result = False                
    except paramiko.SSHException as sshException:
      logger.error("Failed executing command! {}".format(sshException))
      self.client.close()
      exec_result = False    

    return exec_result