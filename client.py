from opcua import Client
import time

# Connect to the OPC UA server
client = Client("opc.tcp://127.0.0.1:4840/freeopcua/server/")
client.connect()

# Get the namespace index for the custom namespace
uri = "http://example.org"
idx = client.get_namespace_index(uri)

# Access the object and variable
objects = client.get_objects_node()
my_obj = objects.get_child(["2:MyObject"])  # Index 2 is the namespace index

# Access the variable by name
my_var = my_obj.get_child(["2:MyStringVariable"])

try:
    # Read and print the value of the string variable
    while True:
        value = my_var.get_value()
        print(f"Received value: {value}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Client stopped.")
finally:
    client.disconnect()
