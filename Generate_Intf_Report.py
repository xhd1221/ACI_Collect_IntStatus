# This module is to generate the interface status report.
# which is a .xlsx file and generated in the same path with this script

# list of other .py files
from Functions import *
from Output import *
from Log import *

# list of packages that should be imported for this code to work
import pandas as pd


# Generate status report for all interfaces.
#                   ACI login session, report file name
def gen_intf_report(session, report_file_name):
	# Create a empty DataFrame to contain the result
	frame = pd.DataFrame(columns=['No', 'POD', 'Leaf', 'Interface', 'Admin_St', 'Status', 'MTU', 'Port Type'])
	# Manually manipulate the index of DataFrame
	frame.set_index('No')
	index_n = [1]
	# Get POD list of the Fabric
	pods = get_pods(session)
	for pod in pods:
		# get nodes and non-APIC & active nodes
		nodes = get_nodes(session, pod)
		non_apic_nodes = get_non_apic_nodes(nodes)
		for node in non_apic_nodes:
			# print('Proceeding ' + str(node.rn))
			logger.debug('Proceeding ' + str(node.rn))
			# get interface list
			intf_list = get_intf_list(session, node)
			# get ethernet PM list
			pminf_list = get_node_intf_pminfs(session, node)
			for intf, pminf in zip(intf_list, pminf_list):
				# get interface result
				data = {
					'No': index_n,
					'POD': str(pod.rn),
					'Leaf': str(node.rn),
					'Interface': str(intf.id),
					'Admin_St': str(intf.adminSt),
					'Status': str(pminf.operSt),
					'MTU': str(intf.mtu),
					'Port Type': str(intf.portT)
				}
				# print(data)
				frame = frame.append(pd.DataFrame(data), sort=False)
				index_n[0] += 1
			#break
	frame.name = 'Intf_Info'
	frame = if_free_swtich(frame)
	# Save the result of all interface status
	to_excel_file(frame, report_file_name, False)
	logger.info('ACI Interface Report Generated...')
	# print("Script run time is : %.03f seconds" % (time.clock()))
	# Generate leaf interfaces in up/down status report
	# meanwhile return the up/down port list
	return gen_updown_report(frame, report_file_name)


# Generate report for interfaces in up/down status.
#                   DataFrame, report file name
def gen_updown_report(frame, report_file_name):
	# Get leaf interfaces in up/down status
	leafintf_up_down = get_leafintf_up_down(frame)
	# Add a attribute name for the result DataFrame
	leafintf_up_down.name = 'Intf_UP_Down'
	# Re-indexing the filtering result
	leafintf_up_down = df_reindex(leafintf_up_down, 'No')
	# Save the filtering result
	to_excel_file(leafintf_up_down, report_file_name, False)
	# print("Script run time is : %.03f seconds" % (time.clock()))
	# Return up/down port list
	return leafintf_up_down

