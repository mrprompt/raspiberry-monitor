from rpyc.utils.zerodeploy import MultiServerDeployment
from plumbum import SshMachine

m1 = SshMachine("192.168.11.26")
# m2 = SshMachine("192.168.11.32")
m3 = SshMachine("192.168.11.35")

dep = MultiServerDeployment([m1, m2, m3])
conn1, conn2, conn3 = dep.classic_connect_all()

def check_process(conn, process):
    # print(conn.modules.sys.platform)

    proc = conn.modules.subprocess.Popen(["pidof", process], stdout = -1, stderr = -1)
    stdout, stderr = proc.communicate()

    print(stdout.split())

check_process(conn1, 'meteotux_pi')
check_process(conn3, 'meteotux_pi')
# check_process(conn3)

dep.close()