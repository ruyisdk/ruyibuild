import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from log import logger
from constant import version, help_info
from command.init import Init
from command.update import Update
from command.generate import Generate


class RuyiBuildApp:
  def __init__(self):
    self.cmdlist = ['help', 'version', 'init', 'update', 'generate', 'destory']
   
  def run_command(self, commandlist):
    if commandlist[0] not in self.cmdlist:
        logger.error('Invalid command, please run "ruyibuild help" for help')
    else:
        if commandlist[0] == 'help':
            if len(commandlist) == 1:
                print (help_info)
            else:
                logger.error('Invalid command, please run "ruyibuild help" for help')
        if commandlist[0] == 'version':
            if len(commandlist) == 1:
                print (version)
            else:
                logger.error('Invalid command, please run "ruyibuild help" for help')
        if commandlist[0] == 'init':
            if len(commandlist) == 3 and commandlist[1] == '-d' and commandlist[2] != '-f':
                init = Init()
                init.run(commandlist[2])
            elif len(commandlist) == 5 and commandlist[1] == '-d' and commandlist[3] == '-f':
                init = Init()
                init.run(commandlist[2], commandlist[4])
            else:
                logger.error('Invalid command, please run "ruyibuild help" for help')
        if commandlist[0] == 'update':
            if len(commandlist) == 1:
                update = Update()
                update.run()
            else:
                logger.error('Invalid command, please run "ruyibuild help" for help')
        if commandlist[0] == 'generate':
            if len(commandlist) == 2:
                generate = Generate()
                generate.run(commandlist[1])
            elif len(commandlist) == 1:
                generate = Generate()
                generate.run()
            else:
                logger.error('Invalid command, please run "ruyibuild help" for help')
        if commandlist[0] == 'destory':
            if len(commandlist) == 1:
                generate = Generate()
                generate.debug_finish()
            else:
                logger.error('Invalid command, please run "ruyibuild help" for help')



def main():
    if (len(sys.argv) < 2 or len(sys.argv) > 6):
        logger.error('Invalid command, please run "ruyibuild help" for help')
    else:
        app = RuyiBuildApp()
        app.run_command(sys.argv[1:])


if __name__ == "__main__":
    main()     