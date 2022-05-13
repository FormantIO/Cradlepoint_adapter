# Cradlepoint Integration

## Captured Data

Data from the Cradlepoint is ingested under two main categories, modem diagnostics and GPS.
Ingestion for modem diagnostics and GPS is controlled by setting the Application Configurations (found in Device Configuration) for 'capture_cp_stats' and 'capture_gps' to 'true'.


### Modem Diagnostics

The following is ingested if 'capture_cp_stats' is set to 'true'.
All ingested data is tagged with '{"carrier":carrier}' and '{"modem":modem}'


-   modem_rsrq (float)
-   modem_dbm (float)
-   modem_temp (float)
-   modem_ps_state (string)
-   modem_ims_state (string)
-   modem_op_mode (string)
-   SS (int)
-   srvc_type (string)
-   tac (int)
-   sinr (float)
-   rsrp (float)
-   ulfrq (float)
-   dlfrq (float)
-   rfchannel (int)
-   txchannel (int)
-   rfband (string)
-   ltebandwidth (string)

Additionally, the entire diagnostics cluster is ingested as 'modem._modem_name_.json' 

### GPS

The following is ingested if 'capture_gps' is set to 'true'

-   gps (geolocation)
-   speed_knots (float)
-   altitude_meters (float)

## Setup

After cloning the repository, populate the 'sdk_settings.ini' file with the appropriate information, including the username, ip and password for the Cradlepoint modem. 

## Running the adapter

### As an Adapter or with the `start.sh` Script
The repo can either be zipped and configured as an adapter in Formant with "Exec command" `./start.sh`, or can be run manually.

