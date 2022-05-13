import time


from csclient import EventingCSClient


class Boot2Exception(Exception):
    pass


class Timeout(Boot2Exception):
    pass


class SocketLost(Boot2Exception):
    pass


class OneModem(Boot2Exception):
    pass


class RunBefore(Boot2Exception):
    pass


STATUS_DEVS_PATH = "/status/wan/devices"
CFG_RULES2_PATH = "/config/wan/rules2"
CTRL_WAN_DEVS_PATH = "/control/wan/devices"
API_URL = "https://www.cradlepointecm.com/api/v2"
CONNECTION_STATE_TIMEOUT = 7 * 60  # 7 Min
NETPERF_TIMEOUT = 5 * 60  # 5 Min


class CradlepointStatus(object):
    STATUS_DEVS_PATH = "/status/wan/devices"
    CFG_RULES2_PATH = "/config/wan/rules2"
    CTRL_WAN_DEVS_PATH = "/control/wan/devices"
    API_URL = "https://www.cradlepointecm.com/api/v2"
    CONNECTION_STATE_TIMEOUT = 7 * 60  # 7 Min
    NETPERF_TIMEOUT = 5 * 60  # 5 Min

    def __init__(self):
        self.client = EventingCSClient("CradlepointStats")

    def find_sims(self):
        sims = {}
        wan_devs = self.client.get(self.STATUS_DEVS_PATH) or {}
        for uid, status in wan_devs.items():
            if uid.startswith("mdm-"):
                error_text = status.get("status", {}).get("error_text", "")
                if error_text:
                    if "NOSIM" in error_text:
                        continue
                sims[uid] = status
        num_sims = len(sims)
        if not num_sims:
            print("No SIMs found at all yet")
        return sims

    def get_sim_diagnostic(self, device):
        try:
            diagnostics = self.client.get(
                f"{self.STATUS_DEVS_PATH}/{device}/diagnostics"
            )
            diagnostics["DEVICE"] = device
            return diagnostics

        except Exception as e:
            print(e)
            return {}

    def get_diagnostics(self):
        sim_diagnostics = {}
        sims = self.find_sims()
        for sim in sims.keys():
            sim_diagnostics[sim] = self.get_sim_diagnostic(sim)
        return sim_diagnostics

    def get_gps(self):
        return self.client.get("/status/gps")
