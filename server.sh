#!/bin/bash

# Show help if STRING_MODE is invalid or GET_HELP is true
if ([[ ! ${STRING_MODE} == int ]] && [[ ! ${STRING_MODE} == short ]] && [[ ! ${STRING_MODE} == long ]]) || [[ ${GET_HELP} == true ]]; then
  python3 /app/server.py --help
  exit 0
fi

# Construct base command
CMD="python3 /app/server.py --opcua-conn ${OPCUA_CONN} --string-mode ${STRING_MODE}"

# Append optional arguments if set
[[ -n "${CHANGE_RATE}" ]] && CMD+=" --change-rate ${CHANGE_RATE}"
[[ -n "${VALUE_CHANGE}" ]] && CMD+=" --value-change ${VALUE_CHANGE}"
[[ ${UPDATE_BASE} == true ]] && CMD+=" --update-base"
[[ ${ENABLE_AUTH} == true ]] && CMD+=" --enable-auth"
[[ ${ADVANCED_OPCUA} == true ]] && CMD+=" --advanced-opcua"

# Run server in an infinite loop
while : ; do
  eval $CMD
done
