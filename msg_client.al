<run msg client where broker=rest and user-agent=anylog and log=false and topic=(
    name=nov and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp=(type=timestamp and value="bring [timestamp]") and
    column.value=(type=float and value="bring [value]" and optional=false)
)>