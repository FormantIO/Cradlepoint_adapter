#!/usr/bin/env bash


# Ensure all prints make it to the journal log
export PYTHONUNBUFFERED=true

#!/usr/bin/env bash

# Check for the setup lock
FILENAME="setup.lock"
 
if [ ! -f "$FILENAME" ]
then
  echo "$FILENAME not found - running setup..."
  ./setup.sh
fi 

# Start the cradlepoint adapter
bash -c "python3 cradlepoint_main.py"
