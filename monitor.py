from rpyc.utils.zerodeploy import MultiServerDeployment
from plumbum import SshMachine

def check_process(conn, process):
    proc = conn.modules.subprocess.Popen(["pidof", process], stdout = -1, stderr = -1)
    stdout, stderr = proc.communicate()

    return len(stdout.split()) > 0

servers = [
    SshMachine("192.168.11.26"), # meteormon2 
    SshMachine("192.168.11.32"), # vpn
    SshMachine("192.168.11.35"), # meteormon1
]

deployment = MultiServerDeployment(servers)
conn1, conn2, conn3 = deployment.classic_connect_all()

print("Camera #1 running: ", check_process(conn3, "meteotux_pi"))
print("Camera #2 running: ", check_process(conn1, "meteotux_pi"))
print("VPN running: ", check_process(conn2, "openvpn"))

deployment.close()