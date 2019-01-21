# This module contains basic functions

# list of other .py files
from Log import *

# list of packages that should be imported for this code to work
import numpy as np
import urllib3
import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.fabric
from cobra.internal.codec.xmlcodec import toXMLStr


# Login
def aci_login(APIC, USER, PASS):
    urllib3.disable_warnings()
    login = cobra.mit.session.LoginSession(APIC, USER, PASS, secure=False, timeout=180)
    session = cobra.mit.access.MoDirectory(login)
    session.login()
    logger.info('Connected to APIC successfully...')
    return session


# Logout
def aci_logout(session):
    session.logout()
    logger.info('Logged out from APIC successfully!!!')


# Get the list of pods of a ACI fabric
def get_pods(session):
    # ClassQuery
    pods = session.lookupByClass("fabricPod", parentDn='topology')
    return pods


# Get the list of nodes under one pod
def get_nodes(session, pod):
    dn = pod.dn
    nodes = session.lookupByClass("fabricNode", parentDn=dn)
    # for node in nodes:
    #     print "Node: {:10s} Name: {:10s} Role: {:10s}".format(node.rn, node.name, node.role)
    return nodes


# Get the list of non-apic and active spine and leaf
# Skip APICs and unsupported switches
def get_non_apic_nodes(nodes):
    n_apic_nodes = []
    for node in nodes:
        if node.role != 'controller' and node.fabricSt == 'active':
            n_apic_nodes.append(node)
        # print "Pod: {:10s} Node Name: {:10s}".format(pod.rn, node.name)
    return n_apic_nodes


# Get the interface list of a node (a non-apic node, like a spine or a leaf)
# l1PhysIf has the name of interface and admin status
def get_intf_list(session, node):
    dn = str(node.dn) + '/sys'
    intfs = session.lookupByClass("l1PhysIf", parentDn=dn)
    return intfs


# Get the operation status of the a single interface
# ethpmPhysIf has the operation status
# please note !!!
# the pmifs is a list who has its own attributes and contains only one member.
# if you would like to access the attribute like operSt or operSpeed, please access member '0' first via for or pmifs[0]
def get_single_intf_OperSt(session, intf):
    dn = str(intf.dn) + '/phys'
    pmifs = session.lookupByClass("ethpmPhysIf", parentDn=dn)
    return pmifs


# Get the Physical interface information of all interfaces on a node
# ethpm:PhysIf Physical interface information holder
# ethpm:PhysIf is not directly contained by node.dn/sys, so if we use so, we can get a object which_
# contains the Physical interface information of all interfaces of a node.
def get_node_intf_pminfs(session, node):
    dn = str(node.dn) + '/sys'
    pmifs = session.lookupByClass("ethpmPhysIf", parentDn=dn)
    return pmifs


# Get interfaces in up/down status
def get_leafintf_up_down(frame):
    return frame[(frame['Admin_St'] == 'up') & (frame['Status'] == 'down') & (frame['Port Type'] == 'leaf')].copy()


# DateFrame re-index (start from 1)
#              DataFrame, DataFrame index column name
def df_reindex(dataframe, index_name):
    dataframe.loc[:, index_name] = np.arange(1, len(dataframe) + 1)
    return dataframe


# Administratively shutdown the interface
# intf_tDn is the target DN of the interface
def shut_intf(session, intf_tDn, if_commit=True):
    topMo = session.lookupByDn('uni/fabric/outofsvc')
    # topMo is from doc APIC Management Information Model Reference
    action = 'blacklist'
    # lc = 'blacklist' is to shutdown the interface
    # 'in-service' is to enable the interface
    # must explicitly point out which argument, tDn and lc
    fabricRsOosPath = cobra.model.fabric.RsOosPath(topMo, tDn=intf_tDn, lc=action)
    change = cobra.mit.request.ConfigRequest()
    change.addMo(fabricRsOosPath)
    if if_commit:
        commit_change(session, change)


# Commit the change to ACI
def commit_change(session, change):
    session.commit(change)
    logger.info('Change Committed...')


# Print Cobra DN to XML code
def show_xml(cobra_dn):
    print toXMLStr(cobra_dn)


# Get the tDN to shutdown the interface
# the input is a DataFrame which only include info for one intf
def get_tDN(data):
    # tDN example 'topology/pod-1/paths-201/pathep-[eth1/47]'
    return 'topology/' + str(data.POD.values[0]) \
          + get_leafno_tDN(str(data.Leaf.values[0])) + '/pathep-[' \
          + str(data.Interface.values[0]) + ']'


# Get the tDN of a Leaf
# fromat from 'node-201' to '/paths-201'
def get_leafno_tDN(node_id):
    return '/paths-' + node_id.split('-')[1]

