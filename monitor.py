from rpyc.utils.zerodeploy import MultiServerDeployment
from plumbum import SshMachine
from dotenv import load_dotenv
import time
import os
import thingspeak

load_dotenv()

def check_process(conn, process):
    proc = conn.modules.subprocess.Popen(["pidof", process], stdout = -1, stderr = -1)
    stdout, stderr = proc.communicate()

    return len(stdout.split()) > 0

channel = thingspeak.Channel(os.environ['THINGSPEAK_CHANNEL'])

while True:
    servers = [
        SshMachine("192.168.11.26"), # meteormon2 
        SshMachine("192.168.11.32"), # vpn
        SshMachine("192.168.11.35"), # meteormon1
    ]

    deployment = MultiServerDeployment(servers)
    conn1, conn2, conn3 = deployment.classic_connect_all()

    check_1 = check_process(conn3, "meteotux_pi")
    check_2 = check_process(conn1, "meteotux_pi")
    check_3 = check_process(conn2, "openvpn")

    print("Camera #1 running: ", check_1)
    print("Camera #2 running: ", check_2)
    print("VPN running: ", check_3)

    deployment.close()

    params = {
        'api_key': os.environ['THINGSPEAK_KEY'],
        'field1': int(check_1),
        'field2': int(check_2),
        'field3': int(check_3)
    }

    try:
        channel.update(params)
    except (Exception):
        print("Olha a excessao", Exception)
        pass

    time.sleep(3600)
