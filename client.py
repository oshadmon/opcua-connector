from opcua import Client
from opcua import ua
import time

# Define the server endpoint (this should match the server endpoint defined in the server code)
server_url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"

# Create a client instance
client = Client(server_url)

# Connect to the server
client.connect()
print(f"Connected to the server at {server_url}")

try:
    # Get the root object of the server (Objects Node)
    objects_node = client.get_objects_node()

    # Print all objects in the address space to check the structure
    print("Listing all objects in the address space:")
    for obj in objects_node.get_children():
        print(f"Object: {obj}, Address: {obj.nodeid}")

    # Access the GlobalVars object (Check path)
    global_vars = objects_node.get_child(["2", "Objects", "DeviceSet", "WAGO 750-8210 PFC200 G2 4ETH XTR", "Resources", "Application", "GlobalVars"])
    print("GlobalVars")
