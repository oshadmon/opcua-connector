import datetime
import json
import os
import aiohttp
import asyncio
import requests
import random

TAG_HIERARCHY = {
    "VFD_CNTRL_TAGS": {
        "D1001VFDStop": 0,
        "D1001VFDStopSpeedSetpoint": 1
    },
    "PE_Lube_Tags": {
        "D2001PELubePumpMtr1Stop": 2,
        "D2003PELubeCoolerManualSpeedValue": 95,
        "D2002PELubePumpMtr2ManualSpeedValue": 96
    },
    "Outputs": {
        "D1001DriveRunCommandDO": 3,
        "D1001DriveSpeedReferenceAO_ENG": 4,
        "D1002ChargePumpDriveSpeedReferenceAO_ENG": 5,
        "D2001PELubePumpDriveSpeedReferenceAO_ENG": 6,
        "D1002ChargePumpVFDRunCommandDO": 7,
        "D2001PELubePumpVFDRunCommandDO": 8,
        "D2002PELubePumpVFDRunCommandDO": 86
    },
    "Inputs": {
        "CV1001PositionFeedbackAI_ENG": 9,
        "CV1002PositionFeedbackAI_ENG": 10,
        "D1001MotorSpeedAI_ENG": 11,
        "D1001MotorTorqueAI_ENG": 12,
        "D1002ChargePumpSpeedAI_ENG": 13,
        "D1002ChargePumpTorqueAI_ENG": 14,
        "D2001PELubePumpDriveSpeedAI_ENG": 15,
        "FT1001MainLoopFlowrateAI_ENG": 16,
        "FT2001PELubeSupplyFlowAI_ENG": {"idx": 17, "name": "Oil FlowRate, "file": """},
        "FT2001PELubeSupplyFlowSetpoint_ENG": 18,
        "LT1001MainWaterTankLevelAI_ENG": 19,
        "PT1001MaingPumpChargePressAI_ENG": 20,
        "PT1002MainPumpDischargePressAI_ENG": 21,
        "PT1003MainPumpDischargePressAI_ENG": 22,
        "PT1004ChokeCV1002PressAI_ENG": 23,
        "PT2001PELubeSupplyPressAI_ENG": 24,
        "PT2001PELubeSupplyPressSetpoint_ENG": 25,
        "PT2002PELubeSupplyPressAI_ENG": 26,
        "PT2002PELubeSupplyPressSetpoint_ENG": 27,
        "TC1001PumpTempSensorAI_ENG": 28,
        "TC1002PumpTempSensorAI_ENG": 29,
        "TC1003PumpTempSensorAI_ENG": 30,
        "TC1004PumpTempSensorAI_ENG": 31,
        "TC1005PumpTempSensorAI_ENG": 32,
        "TC1006PumpTempSensorAI_ENG": 33,
        "TC1007PumpTempSensorAI_ENG": 34,
        "TC1008PumpTempSensorAI_ENG": 35,
        "TC1009PumpTempSensorAI_ENG": 36,
        "TC1010PumpTempSensorAI_ENG": 37,
        "TC1011PumpTempSensorAI_ENG": 38,
        "TC1012PumpTempSensorAI_ENG": 39,
        "TT1001MainWaterTemperatureAI_ENG": 40,
        "TT2001PELubeTankTempAI_ENG": 41,
        "TT2002PELubeSupplyTempAI_ENG": 42,
        "D2002PELubePumpDriveSpeedAI_ENG": 87,
        "PT2006PELubeSupplyPressSetpointAI_ENG": 88,
        "PT2006PELubeSupplyPressAI_ENG": 89,
        "PT2005PELubeSupplyPressAI_ENG": 90,
        "PT2005PELubeSupplyPressSetpointAI_ENG": 91,
        "PT2004PELubeSupplyPressAI_ENG": 92,
        "PT2003PELubeSupplyPressAI_ENG": 93,
        "FT2002PELubeSupplyFlowAI_ENG": 94,
        "D1001MotorEff": 97,
        "D2001PELubePumpDriveEff": 98,
        "D2002PELubePumpDriveEff": 99,
        "FT2001PELubeDriveCalculatedFlowrate_ENG": 100,
        "FT1001MainLoopCalculatedFlowrateAI_ENG": 101,
        "FT2002PELubeDriveCalculatedFlowrate_ENG": 102
    },
    "CHOKE_TAGS": {
        "CV1002ChokeValvePositionSetpoint": 43,
        "CV1002ChokeValveStop": 44,
        "CV1001ChokeValveStop": 45,
        "CV1001ChokeValvePositionSetpoint": 46
    },
    "CHARGE_PUMP_TAGS": {
        "D1002ChargePumpMotorStop": 47
    },
    "ALARM_TAGS": {
        "FT2001LL_AlarmSetpoint": 48,
        "LS1001H_AlarmSetpoint": 49,
        "LS1002H_AlarmSetpoint": 50,
        "LS1003H_AlarmSetpoint": 51,
        "LS1004HH_AlarmSetpoint": 52,
        "LS2001L_AlarmSetpoint": 53,
        "LT1001L_AlarmSetpoint": 54,
        "LT1001LL_AlarmSetpoint": 55,
        "PT1001L_AlarmSetpoint": 56,
        "PT1001LL_AlarmSetpoint": 57,
        "PT1002HH_AlarmSetpoint": 58,
        "PT1003HH_AlarmSetpoint": 59,
        "PT2001HH_AlarmSetpoint": 60,
        "PT2002L_AlarmSetpoint": 61,
        "PT2002LL_AlarmSetpoint": 62,
        "TT1001H_AlarmSetpoint": 63,
        "TT1001HH_AlarmSetpoint": 64,
        "TT2001H_AlarmSetpoint": 65,
        "TT2001HH_AlarmSetpoint": 66,
        "FT2001LL_Alarm": 67,
        "LS1001H_Alarm": 68,
        "LS1002H_Alarm": 69,
        "LS1003H_Alarm": 70,
        "LS1004HH_Alarm": 71,
        "LS2001L_Alarm": 72,
        "LT1001L_Alarm": 73,
        "LT1001LL_Alarm": 74,
        "PT1001L_Alarm": 75,
        "PT1001LL_Alarm": 76,
        "PT1002HH_Alarm": 77,
        "PT1003HH_Alarm": 78,
        "PT2001HH_Alarm": 79,
        "PT2002L_Alarm": 80,
        "PT2002LL_Alarm": 81,
        "TT1001H_Alarm": 82,
        "TT1001HH_Alarm": 83,
        "TT2001H_Alarm": 84,
        "TT2001HH_Alarm": 85
    }
}




async def post_data(conn: str, data, session: aiohttp.ClientSession, chunk_size: int = 1000, max_parallel: int = 5):
    headers = {
        "command": "data",
        "topic": "nov",
        "User-Agent": "AnyLog/1.23",
        "Content-Type": "application/json"
    }

    sem = asyncio.Semaphore(max_parallel)

    async def send_chunk(chunk):
        async with sem:
            try:
                async with session.post(f"http://{conn}", headers=headers, data=json.dumps(chunk)) as resp:
                    if resp.status >= 300:
                        text = await resp.text()
                        raise Exception(f"Failed posting data: {resp.status} - {text}")
            except Exception as e:
                print(f"⚠️ Chunk failed: {e}")

    tasks = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        tasks.append(asyncio.create_task(send_chunk(chunk)))

    await asyncio.gather(*tasks)


def get_data(dir_name):
    full_data = []
    full_dir = os.path.join("data", dir_name)
    if os.path.isdir(full_dir):
        for fname in os.listdir(full_dir):
            full_path = os.path.join(full_dir, fname)
            with open(full_path, "r") as f:
                for line in f.read().split("\n"):
                    if line.strip():
                        full_data.append(json.loads(line))
    return full_data


def shift_timestamps(data, new_start):
    if not data:
        return []

    if isinstance(new_start, str):
        new_start = datetime.datetime.fromisoformat(new_start)

    updated = []
    prev_new_ts = new_start
    updated.append({**data[0], "timestamp": prev_new_ts.isoformat()})

    for i in range(1, len(data)):
        prev_old_ts = datetime.datetime.fromisoformat(data[i - 1]["timestamp"])
        curr_old_ts = datetime.datetime.fromisoformat(data[i]["timestamp"])
        delta = curr_old_ts - prev_old_ts
        new_ts = prev_new_ts + delta
        updated.append({**data[i], "timestamp": new_ts.isoformat()})
        prev_new_ts = new_ts

    return updated


async def prepare_data(idx: int):
    full_data = get_data(f"t{idx}")
    data = shift_timestamps(
        data=full_data,
        new_start=datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    )
    for i in range(len(data)):
        data[i]["timestamp"] = data[i].pop("timestamp").split("+")[0]
        data[i]["table"] = f"t{idx+1}"
        data[i]["dbms"] = "new_nov"
    return data


async def grep_json_data():
    """
    Fetch data in parallel, then push in async-parallel batches.
    """
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            for category, tags in TAG_HIERARCHY.items():
                for tag_name, idx in tags.items():
                    tasks.append(prepare_data(idx))

            results = await asyncio.gather(*tasks)
            all_data = [row for dataset in results for row in dataset]

            if all_data:
                await post_data("10.0.0.220:32149", all_data, session)

            await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(grep_json_data())
