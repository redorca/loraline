'''
    Fundamentally a wrapper around the python logging module to both simplify default handling, which would never touch on syslog or systemd, so that logging is as simple as print.
    In fact replacing print with a logg call would be a nice touch.
'''
import logging
import logging.handlers as lhaul

class DasLog():
    '''
        Framework for establishing a logging componnent
    '''
    def __init__(self, handler="syslog"):
        '''
            Setup a logger with the syslog handler and useful formatting so upon
            return the class instance is a fully functional logger
        '''
        self.handlers = dict()
        self.map_to_level = dict()

        self.handlers['syslog'] = lhaul.SysLogHandler
        sysHandle = self.handlers['syslog'](address='/dev/log')

        '''
            This order of mapping to levels is the priority/order within the logging module too.
        '''
        self.map_to_level['debug'] =    logging.DEBUG
        self.map_to_level['info'] =     logging.INFO
        self.map_to_level['warn'] =     logging.WARNING
        self.map_to_level['error'] =    logging.ERROR
        self.map_to_level['critical'] = logging.CRITICAL

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(sysHandle)

        return

    def error(self, msg):
        self.log.error(msg)

    def info(self, msg):
        self.log.info(msg)

    def warn(self, msg):
        self.warning(msg)

    def warning(self, msg):
        self.log.warning(msg)

    def debug(self, msg):
        self.log.debug(msg)

    def critical(self, msg):
        self.log.critical(msg)

    def get_level(self):
        return logging.getLevelName(self.log.getEffectiveLevel())

    def msg(self, level, msg):
        self.map_to_level[level](msg)

#-_- search for -_- to find the first line of those remaining to the end of the file, to be removed
#
if __name__ == "__main__":
    def main():
        print("Running from main.")

    main()
