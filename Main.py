# Written by Haden Xu @ Cisco Systems, Jan 2019

# list of other .py files
from Log import *
import ACI_Access as ACI
from Generate_Intf_Report import *
from Shut_non_connected_port import *
from Functions import *

# list of other Library
import time

# Output file & path
report_file_name = 'ACI Interface Report.xlsx'
target_intf = 'Target Interface.xlsx'


def main():
    # Initiate the logger
    initiate_logger(logger)
    # Login in APIC
    session = aci_login(ACI.APIC, ACI.USER, ACI.PASS)
    # Generate the interface status report
    # and get the up/down list(DataFrame)
    frame = gen_intf_report(session, report_file_name)
    # Shut the port listed in the interface report.
    # shut_noncon_ports(session, report_file_name, frame)
    # Log out the APIC
    aci_logout(session)
    logger.info("Script run time is : %.03f seconds" % (time.clock()))
    logger.info('Completed!!!')


if __name__ == '__main__':
    main()

