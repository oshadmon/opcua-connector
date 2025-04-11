#!/bin/bash

# OPC-UA stops then automatically restarts
if ([[ ! ${STRING_MODE} == int ]] && [[ ! ${STRING_MODE} == short ]] && [[ ! ${STRING_MODE} == long ]]) || [[ ${GET_HELP} == true ]] ; then
  python3 /app/server.py --help
  exit 0
elif [[ ${ADVANCED_CCNFIGS} == true ]] ; then
  while : ; do
    python3 /app/server.py --opcua-conn ${OPCUA_CONN} --string-mode ${STRING_MODE} --advanced-opcua
  done
else
  while : ; do
    python3 /app/server.py --opcua-conn ${OPCUA_CONN} --string-mode ${STRING_MODE}
  done
fi
