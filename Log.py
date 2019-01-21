# This module is to generate the log information to both Console and
# the log file.

# list of packages that should be imported for this code to work
import logging

logger_name = 'scriptlogger'


# Define/Create a logger
def define_logger(name):
	return logging.getLogger(name)


def initiate_logger(logger):
	# set logger level to DEBUG
	logger.setLevel(logging.DEBUG)
	# create a handler to write the log
	fh = logging.FileHandler('Running_Log.log')
	# set log file logging level
	fh.setLevel(logging.DEBUG)
	# create another handler for Console output
	ch = logging.StreamHandler()
	# set Console log logging level
	ch.setLevel(logging.DEBUG)
	# define handler output format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add handler to logger
	logger.addHandler(fh)
	logger.addHandler(ch)
	logger.debug('logger has been initiated...')


if __name__ == 'Log':
	logger = define_logger(logger_name)


