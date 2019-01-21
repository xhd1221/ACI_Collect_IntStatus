# This module is to shut the port listed in the interface report.

# list of other .py files
from Functions import *
from Log import *


# Shutdown interfaces in up/down status.
#                   ACI login session, DataFrame, report file name
def shut_noncon_ports(session, file_name=None, frame=None):
	# if frame == None:
	# 	load_df(file_name)
	for i in frame['No']:
		tDN = get_tDN(frame[(frame['No'] == i)])
		shut_intf(session, tDN, True)
		logger.info('Shutting down ' + tDN)
		# break











