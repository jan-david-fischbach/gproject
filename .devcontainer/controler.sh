#!/bin/bash

mosquitto &

# Start the first process
python /usr/local/bin/klive_translator.py 
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?