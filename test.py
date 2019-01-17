import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.fabric
from cobra.internal.codec.xmlcodec import toXMLStr
import urllib3

APIC = "https://apic.ashk.io"  # type: str
USER = "admin"
PASS = "C1sc0123"

urllib3.disable_warnings()
login = cobra.mit.session.LoginSession(APIC, USER, PASS, secure=False, timeout=180)
session = cobra.mit.access.MoDirectory(login)
session.login()

# tDn = "topology/pod-1/paths-201/pathep-[eth1/47]"
topMo = session.lookupByDn('uni/fabric/outofsvc')
action = 'blacklist'
dnname = 'topology/pod-1/paths-201/pathep-[eth1/47]'

fabricRsOosPath = cobra.model.fabric.RsOosPath(topMo, tDn=dnname, lc=action)
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
session.commit(c)


