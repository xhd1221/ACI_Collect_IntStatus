# This module is to shut the port listed in the interface report.

# list of other .py files
from Functions import *


# Generate status report for all interfaces.
#                   ACI login session, DataFrame, report file name
def shut_noncon_ports(session, file_name, frame=None):
	# if frame == None:
	# 	load_df(file_name)
	for i in frame['No']:
		tDN = get_tDN(frame[(frame['No'] == i)])
		shut_intf(session, tDN, True)
		print tDN
		# break











