#!/usr/bin/env bash


# Ensure all prints make it to the journal log
export PYTHONUNBUFFERED=true

# Start the cradlepoint adapter
bash -c "python3 -m pip install -r requirements.txt"
bash -c "python3 cradlepoint_main.py"
