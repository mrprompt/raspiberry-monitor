from rpyc.utils.zerodeploy import MultiServerDeployment
from plumbum import SshMachine

def check_process(conn, process):
    proc = conn.modules.subprocess.Popen(["pidof", process], stdout = -1, stderr = -1)
    stdout, stderr = proc.communicate()

    return len(stdout.split()) > 0

servers = [
    SshMachine("192.168.11.26"), 
    SshMachine("192.168.11.35")
]

deployment = MultiServerDeployment(servers)
conn1, conn2 = deployment.classic_connect_all()

print("Meteormon #1 running: ", check_process(conn1, "meteotux_pi"))
print("Meteormon #2 running: ", check_process(conn1, "meteotux_pi"))

deployment.close()