import argparse
import os
import time
from opcua import Server, ua
import multiprocessing
import threading
from server_working import OPCUAServer
import pandas as pd


METADATAS = {
    "oil system": {
        "file": os.path.join('base_examples', 'hpu_mud_system_oil_data.v6.csv'),
        "oil_flowrate_lpm": 20,
        "oil_temp_supply_c": 45,
        "oil_pressure_kpa": 27,
        "oil_temp_cooled_c": 42
    },
    "main loop": {
        "file": os.path.join('base_examples', 'hpu_mud_system_main_loop_data.v6.csv'),
        "main_loop_flowrate_lpm": 19,
        "discharge_pressure_1_kpa": 24,
        "discharge_pressure_2_kpa": 25
    },
    "thermocouples": {
        "file": os.path.join('base_examples', 'hpu_mud_system_thermocouple_data.v6.csv'),
        'TC1001': 31, 'TC1002': 32, 'TC1003': 33, 'TC1004': 34,
        'TC1005': 35, 'TC1006': 36, 'TC1007': 37, 'TC1008': 38,
        'TC1009': 39, 'TC1010': 40, 'TC1011': 41, 'TC1012': 42
    }
}


# Static NodeIds for Objects (folders/nodes)
IDX_OBJECTS = [
    "DeviceSet",
    "WAGO 750-8210 PFC200 G2 4ETH XTR",
    "Resources",
    "Application",
    "GlobalVars",
    "VFD_CNTRL_TAGS",
    # "PE_Lube_Tags",
    # "Outputs",
    "Inputs", # <-
    "CHOKE_TAGS", # <-
    # "CHARGE_PUMP_TAGS",
    # "ALARM_TAGS"
]


# Static NodeIds for Variables (leaf tags)
IDX_VARIABLES = {
    'LT1001MainWaterTankLevelAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 19, 'file': 'base_examples\\hpu_mud_system_main_loop_data.v6.csv', 'file_column': 'main_loop_flowrate_lpm'},
    'PT1001MaingPumpChargePressAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 20, 'file': 'base_examples\\hpu_mud_system_oil_data.v6.csv', 'file_column': 'oil_flowrate_lpm'},
    'PT2001PELubeSupplyPressAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 24, 'file': 'base_examples\\hpu_mud_system_main_loop_data.v6.csv', 'file_column': 'discharge_pressure_1_kpa'},
    'PT2001PELubeSupplyPressSetpoint_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 25, 'file': 'base_examples\\hpu_mud_system_main_loop_data.v6.csv', 'file_column': 'discharge_pressure_2_kpa'},
    'PT2002PELubeSupplyPressSetpoint_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 27, 'file': 'base_examples\\hpu_mud_system_oil_data.v6.csv', 'file_column': 'oil_pressure_kpa'},
    'TC1004PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 31, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1001'},
    'TC1005PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 32, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1002'},
    'TC1006PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 33, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1003'},
    'TC1007PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 34, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1004'},
    'TC1008PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 35, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1005'},
    'TC1009PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 36, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1006'},
    'TC1010PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 37, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1007'},
    'TC1011PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 38, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1008'},
    'TC1012PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 39, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1009'},
    'TT1001MainWaterTemperatureAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 40, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1010'},
    'TT2001PELubeTankTempAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 41, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1011'},
    'TT2002PELubeSupplyTempAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 42, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1012'},
    'CV1001ChokeValveStop': {'alter_datatype':ua.VariantType.Float, 'idx': 45, 'file': 'base_examples\\hpu_mud_system_oil_data.v6.csv', 'file_column': 'oil_temp_supply_c'}
}

# Tag HIERARCHY
TAG_HIERARCHY = {
    'Inputs': {
        'LT1001MainWaterTankLevelAI_ENG': ua.VariantType.Float,
        'PT1001MaingPumpChargePressAI_ENG': ua.VariantType.Float,
        'PT2001PELubeSupplyPressAI_ENG': ua.VariantType.Float,
        'PT2001PELubeSupplyPressSetpoint_ENG': ua.VariantType.Float,
        'PT2002PELubeSupplyPressSetpoint_ENG': ua.VariantType.Float, 'TC1004PumpTempSensorAI_ENG': ua.VariantType.Float,
        'TC1005PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1006PumpTempSensorAI_ENG': ua.VariantType.Float,
        'TC1007PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1008PumpTempSensorAI_ENG': ua.VariantType.Float,
        'TC1009PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1010PumpTempSensorAI_ENG': ua.VariantType.Float,
        'TC1011PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1012PumpTempSensorAI_ENG': ua.VariantType.Float,
        'TT1001MainWaterTemperatureAI_ENG': ua.VariantType.Float, 'TT2001PELubeTankTempAI_ENG': ua.VariantType.Float,
        'TT2002PELubeSupplyTempAI_ENG': ua.VariantType.Float
    },
    'CHOKE_TAGS': {
        'CV1001ChokeValveStop': ua.VariantType.Float
    }
}


def run_variable_updater(server:OPCUAServer, tag_groups, change_rate, value_change, update_base):
    server.update_variable_values(tag_groups, change_rate, value_change, update_base)


class DataGenerator:
    def __init__(self):
        self.csv_cache = {}

    def load_csv(self, file_path: str):
        if file_path not in self.csv_cache:
            df = pd.read_csv(file_path)
            self.csv_cache[file_path] = df
        return self.csv_cache[file_path]

    def get_column_values(self, file_path: str, column_name: str):
        df = self.load_csv(file_path)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in {file_path}")
        return df[column_name].tolist()

class OPCUAServer:
    def __init__(self, endpoint="127.0.0.1:4840", is_advanced: bool = False):
        self.data_generator = DataGenerator()
        self.server = Server()
        self.endpoint = f"opc.tcp://{endpoint}/freeopcua/server/"
        self.is_advanced = is_advanced

    def setup_server(self, enable_auth: bool = False, string_mode: str = 'short'):
        self.server.set_endpoint(self.endpoint)
        self.server.set_server_name("OPC-UA Server")
        self.idx = self.server.register_namespace("http://example.org")

        # if enable_auth:
        #     self.server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
        #     self.setup_authentication()

        objects = self.server.get_objects_node()
        device_set = objects.add_object(
            self.build_nodeid("DeviceSet", string_mode=string_mode),
            "DeviceSet"
        )

        wago = device_set.add_object(
            self.build_nodeid("WAGO 750-8210 PFC200 G2 4ETH XTR", parent_path="DeviceSet", string_mode=string_mode),
            "WAGO 750-8210 PFC200 G2 4ETH XTR"
        )

        resources = wago.add_object(
            self.build_nodeid("Resources", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR", string_mode=string_mode),
            "Resources"
        )

        application = resources.add_object(
            self.build_nodeid("Application", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources", string_mode=string_mode),
            "Application"
        )

        global_vars = application.add_object(
            self.build_nodeid("GlobalVars", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application", string_mode=string_mode),
            "GlobalVars"
        )

        return global_vars


    def build_nodeid(self, name, parent_path="", string_mode='short'):
        # string_mode can be 'int', 'short', or 'long'
        if string_mode == 'int':
            if name in IDX_OBJECTS:
                node_id_value = IDX_OBJECTS.index(name) + 1000
            elif name in IDX_VARIABLES:
                node_id_value = IDX_VARIABLES[name]['idx'] + 2001
                if len(IDX_OBJECTS) >= 2000:
                    node_id_value += len(IDX_OBJECTS)
            else:
                raise ValueError(f"Missing {name} from both objects and variables list(s)")
            return ua.NodeId(node_id_value, self.idx)
        elif string_mode == 'short':
            # Use string name as is
            return ua.NodeId(name, self.idx)
        elif string_mode == 'long':
            full_name = f"{parent_path}.{name}" if parent_path else name
            return ua.NodeId(full_name, self.idx)
        else:
            raise ValueError(f"Unknown string_mode '{string_mode}'")

    def add_variables(self, parent_obj, tag_dict, parent_path="", string_mode='short'):
        tag_var_dict = {}
        for tag, vtype in tag_dict.items():
            default_value = {
                ua.VariantType.Int32: 0,
                ua.VariantType.Float: 0.0,
                ua.VariantType.Double: 0.0,
                ua.VariantType.Boolean: False,
                ua.VariantType.String: "",
            }.get(vtype, None)
            nodeid = self.build_nodeid(tag, parent_path=parent_path, string_mode=string_mode)
            var = parent_obj.add_variable(nodeid, tag, default_value, varianttype=vtype)
            tag_var_dict[tag] = (var, vtype)
        return tag_var_dict

    def create_tag_group_objects(self, global_vars, string_mode='short'):
        tag_group_var_dicts = {}
        base_path = "DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application.GlobalVars"

        for tag_group, tags_with_types in TAG_HIERARCHY.items():
            parent_path = f"{base_path}.{tag_group}" if string_mode == 'long' else base_path
            tag_group_nodeid = self.build_nodeid(tag_group, parent_path=base_path if string_mode == 'long' else "", string_mode=string_mode)
            tag_group_obj = global_vars.add_object(tag_group_nodeid, tag_group)
            tag_group_var_dicts[tag_group] = self.add_variables(tag_group_obj, tags_with_types, parent_path=parent_path, string_mode=string_mode)

        return tag_group_var_dicts

    def set_variables_writable(self, tag_group_var_dicts):
        for tag_vars in tag_group_var_dicts.values():
            for var, _ in tag_vars.values():
                var.set_writable()

    def start_server(self):
        self.server.start()
        print(f"Server is running at {self.endpoint}")

    def get_sensor_data(self, idx:int):
        for metadata in METADATAS:
            if idx in METADATAS[metadata].values():
                file_name =  METADATAS[metadata]['file']
                for column_name, value in METADATAS[metadata].items():
                    if value == idx:
                        return self.data_generator.get_column_values(file_path=file_name, column_name=column_name)


    def update_variable_values(self, tag_group_var_dicts, change_rate, value_change, update_base):
        last_update_time = time.time()
        while True:
            current_time = time.time()
            if current_time - last_update_time >= change_rate:
                last_update_time = current_time
                for tag_group, tag_vars in tag_group_var_dicts.items():
                    for tag, (var, vtype) in tag_vars.items():
                        # Random fluctuation around base value
                        values = self.get_sensor_data(idx=IDX_VARIABLES.get(tag)['idx'])
                        # Clamp if numeric
                        for val in values:
                            var.set_value(val)
                            time.sleep(5)

    # ✅ ADD THIS to your OPCUAServer class
    def run_multiprocess(self, num_workers=4, **kwargs):
        # Setup server and create tag group objects in parent process
        global_vars = self.setup_server(
            enable_auth=kwargs.get("enable_auth", False),
            string_mode=kwargs.get("string_mode", 'short')
        )
        tag_group_var_dicts = self.create_tag_group_objects(
            global_vars, string_mode=kwargs.get("string_mode", 'short')
        )
        self.set_variables_writable(tag_group_var_dicts)
        self.start_server()

        tag_group_items = list(tag_group_var_dicts.items())
        chunk_size = (len(tag_group_items) + num_workers - 1) // num_workers
        processes = []

        # Define a wrapper function that runs inside each process
        def worker(chunk, change_rate, value_change, update_base):
            # The server object or tag groups are NOT passed; just data values
            self.update_variable_values(chunk, change_rate, value_change, update_base)

        for i in range(num_workers):
            chunk_dict = dict(tag_group_items[i * chunk_size:(i + 1) * chunk_size])
            if not chunk_dict:
                continue
            p = multiprocessing.Process(
                target=worker,
                args=(
                    chunk_dict,
                    kwargs.get("change_rate", 1),
                    kwargs.get("value_change", None),
                    kwargs.get("update_base", False)
                )
            )
            p.start()
            processes.append(p)

        try:
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            print("Stopping server and worker processes...")
            for p in processes:
                p.terminate()
            self.server.stop()

    def run_threaded(self, num_workers=4, **kwargs):
        # Setup server and create tag group objects
        global_vars = self.setup_server(
            enable_auth=kwargs.get("enable_auth", False),
            string_mode=kwargs.get("string_mode", 'short')
        )
        tag_group_var_dicts = self.create_tag_group_objects(
            global_vars, string_mode=kwargs.get("string_mode", 'short')
        )
        self.set_variables_writable(tag_group_var_dicts)
        self.start_server()

        tag_group_items = list(tag_group_var_dicts.items())
        chunk_size = (len(tag_group_items) + num_workers - 1) // num_workers
        threads = []

        # Define worker function for each thread
        def worker(chunk, change_rate, value_change, update_base):
            self.update_variable_values(chunk, change_rate, value_change, update_base)

        for i in range(num_workers):
            chunk_dict = dict(tag_group_items[i * chunk_size:(i + 1) * chunk_size])
            if not chunk_dict:
                continue
            t = threading.Thread(
                target=worker,
                args=(
                    chunk_dict,
                    kwargs.get("change_rate", 1),
                    kwargs.get("value_change", None),
                    kwargs.get("update_base", False)
                ),
                daemon=True  # allows program to exit even if threads are running
            )
            t.start()
            threads.append(t)

        try:
            # Keep main thread alive while workers run
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping server and threads...")
            self.server.stop()



# ✅ UPDATED MAIN ENTRY POINT
if __name__ == "__main__":
    """
    Sample server for OPC-UA

    Optional arguments:
        -h, --help              Show this help message and exit
        --opcua-conn            OPC-UA connection IP + Port
        --string-mode           NodeId mode: int / short / long
        --change-rate           Frequency (Hz) to change values
        --value-change          Change rate percentage (e.g. 5 for ±5%)
        --update-base           Whether to update base value
        --enable-auth           Enable authentication
        --advanced-opcua        Use multiple data types
        --num-workers           Number of parallel variable updater processes
    """
    multiprocessing.freeze_support()  # safe for Windows
    parser = argparse.ArgumentParser()
    parser.add_argument('--opcua-conn', type=str, default='127.0.0.1:4840', help="OPC-UA connection IP + Port")
    parser.add_argument('--string-mode', choices=['int', 'short', 'long'], default='short', help='String NodeId mode')
    parser.add_argument('--change-rate', type=float, default=1, help='Frequency in Hz to change values')
    parser.add_argument('--value-change', type=float, default=None, help='Change rate percentage (e.g. 5 for ±5%)')
    parser.add_argument('--update-base', type=bool, nargs='?', const=True, default=False, help='Update base value on each change')
    parser.add_argument('--enable-auth', type=bool, nargs='?', const=True, default=False, help='Enable OPC-UA authentication')
    parser.add_argument('--advanced-opcua', type=bool, nargs='?', const=True, default=False, help='Use advanced data types')
    parser.add_argument('--num-workers', type=int, default=4, help='Number of parallel update processes')

    args = parser.parse_args()

    args.change_rate = round(1 / abs(args.change_rate), 5) if args.change_rate > 0 else 1.0
    if args.value_change is not None:
        args.value_change = abs(args.value_change / 100) if args.value_change > 1 else abs(args.value_change)

    server = OPCUAServer(endpoint=args.opcua_conn, is_advanced=args.advanced_opcua)
    server.run_threaded(
        num_workers=args.num_workers,
        enable_auth=args.enable_auth,
        string_mode=args.string_mode,
        change_rate=args.change_rate,
        value_change=args.value_change,
        update_base=args.update_base
    )