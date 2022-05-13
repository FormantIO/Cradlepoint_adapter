#!/usr/bin/env python3

import json

from cp_status import CradlepointStatus


class CradlePointIntegration(object):
    def __init__(self, fclient):
        self._fclient = fclient
        self._cp_status = CradlepointStatus()

    def capture_gps(self, event=None):
        print("Capturing GPS")
        try:
            gps_data = self._cp_status.get_gps()
            json_value = gps_data
            if json_value["fix"] is not None:
                latitude = json_value["fix"]["latitude"]
                longitude = json_value["fix"]["longitude"]
                if latitude["degree"] < 0:
                    lat = (
                        latitude["degree"]
                        - latitude["minute"] / 60.0
                        - latitude["second"] / 3600.0
                    )
                else:
                    lat = (
                        latitude["degree"]
                        + latitude["minute"] / 60.0
                        + latitude["second"] / 3600.0
                    )
                if longitude["degree"] < 0:
                    lon = (
                        longitude["degree"]
                        - longitude["minute"] / 60.0
                        - longitude["second"] / 3600.0
                    )
                else:
                    lon = (
                        longitude["degree"]
                        + longitude["minute"] / 60.0
                        + longitude["second"] / 3600.0
                    )

                speed = json_value["fix"]["ground_speed_knots"]
                altitude = json_value["fix"]["altitude_meters"]

                if json_value["fix"]["lock"]:
                    self._fclient.post_geolocation("gps", lat, lon)
                    if speed is not None:
                        self._fclient.post_numeric("speed_knots", speed)
                    if altitude is not None:
                        self._fclient.post_numeric("altitude_meters", altitude)
                    self._fclient.post_bitset("gps_lock", {"lock": True})
                else:
                    self._fclient.post_bitset("gps_lock", {"lock": False})
            else:
                print("No Fix")
                print(json_value)

        except Exception as e:
            print("Error capturing GPS")
            print(e)

    def capture_cp_stats(self, event=None):
        try:
            print("Capturing stats")
            diagnostics = self._cp_status.get_diagnostics()
            for modem in diagnostics:
                print("Stats for modem: %s" % str(modem))
                carrier = diagnostics[modem]["CARRID"]
                tags = {"carrier": carrier, "modem": modem}
                self._fclient.post_json(
                    ("modem.%s.json" % modem),
                    json.dumps(diagnostics[modem]),
                    tags,
                )
                modempsstate = diagnostics[modem]["MODEMPSSTATE"]
                modemimstate = diagnostics[modem]["MODEMIMSSTATE"]
                modemopmode = diagnostics[modem]["MODEMOPMODE"]
                ss = diagnostics[modem]["SS"]
                srvc_type = diagnostics[modem]["SRVC_TYPE"]
                tac = diagnostics[modem]["TAC"]
                sinr = diagnostics[modem]["SINR"]
                rsrp = diagnostics[modem]["RSRP"]
                ulfrq = diagnostics[modem]["ULFRQ"]
                dlfrq = diagnostics[modem]["DLFRQ"]
                rfchannel = diagnostics[modem]["RFCHANNEL"]
                txchannel = diagnostics[modem]["TXCHANNEL"]
                rfband = diagnostics[modem]["RFBAND"]
                ltebandwidth = diagnostics[modem]["LTEBANDWIDTH"]

                carrier = diagnostics[modem]["CARRID"]
                rsrq = diagnostics[modem]["RSRQ"]
                dbm = diagnostics[modem]["DBM"]
                temp = diagnostics[modem]["MODEMTEMP"]

                self._fclient.post_numeric("modem_rsrq", float(rsrq), tags)
                self._fclient.post_numeric("modem_dbm", float(dbm), tags)
                self._fclient.post_numeric("modem_temp", float(temp), tags)
                self._fclient.post_text(
                    "modem_ps_state",
                    str(modempsstate),
                    tags,
                )
                self._fclient.post_text(
                    "modem_ims_state",
                    str(modemimstate),
                    tags,
                )
                self._fclient.post_text(
                    "modem_op_mode",
                    str(modemopmode),
                    tags,
                )
                self._fclient.post_numeric("SS", int(ss), tags)
                self._fclient.post_text("srvc_type", str(srvc_type), tags)
                self._fclient.post_numeric("tac", int(tac), tags)
                self._fclient.post_numeric("sinr", float(sinr), tags)
                self._fclient.post_numeric("rsrp", float(rsrp), tags)
                self._fclient.post_numeric("ulfrq", float(ulfrq), tags)
                self._fclient.post_numeric("dlfrq", float(dlfrq), tags)
                self._fclient.post_numeric("rfchannel", int(rfchannel), tags)
                self._fclient.post_numeric("txchannel", int(txchannel), tags)
                self._fclient.post_text("rfband", str(rfband), tags)
                self._fclient.post_text(
                    "ltebandwidth",
                    str(ltebandwidth),
                    tags,
                )

        except Exception as e:
            print("Error capturing stats")
            print(e)
