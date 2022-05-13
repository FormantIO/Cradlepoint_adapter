#!/usr/bin/env python3

import os
from formant.sdk.agent.v1 import Client as FormantClient
from cradlepoint_integration import CradlePointIntegration
import time


class CradlePointIntegrationNode:
    def __init__(self):
        self._rospy_timers = []
        try:
            while True:
                try:
                    agent_url = os.getenv("FORMANT_AGENT_URL", None)
                    if agent_url is None:
                        self._fclient = FormantClient(
                            ignore_unavailable=True,
                            ignore_throttled=True,
                        )
                    else:
                        self._fclient = FormantClient(
                            agent_url=agent_url,
                            ignore_unavailable=True,
                            ignore_throttled=True,
                        )
                    print("Agent connection established, initializing")
                    self._node = CradlePointIntegration(self._fclient)
                    self._update_config_callback()
                    self._fclient.register_config_update_callback(
                        self._update_config_callback
                    )
                    break
                except Exception as e:
                    print(e)
                    time.sleep(3)
            print("Initialized, starting capture.")
            while True:
                if self.capture_cp_stats:
                    self._node.capture_cp_stats()
                if self.capture_gps:
                    self.node.capture_gps()
                time.sleep(1)
        except Exception as e:
            print(e)
            pass

    def _update_config_callback(self):
        print("test")
        self.capture_cp_stats = (
            self._fclient.get_app_config("capture_cp_stats", "false") == "true"
        )
        if self.capture_cp_stats == "true":
            print("Starting to capture state")
        self.capture_gps = (
            self._fclient.get_app_config("capture_gps", "false") == "true"
        )
        if self.capture_gps == "true":
            print("Starting to capture gps")


if __name__ == "__main__":
    try:
        CradlePointIntegrationNode()
    except Exception:
        pass
