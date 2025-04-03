import random

from opcua import Server
from opcua import ua
import time

# Initialize the OPC UA server
server = Server()

# Set server endpoint (you can customize the URL here)
server.set_endpoint("opc.tcp://127.0.0.1:4840/freeopcua/server/")

# Setup server namespace (URI for the namespace)
uri = "http://example.org"
idx = server.register_namespace(uri)

# Create a new object in the server address space
objects = server.get_objects_node()
my_obj = objects.add_object(idx, "MyObject")

# Add a string variable to the object
my_var = my_obj.add_variable(idx, "MyStringVariable", "Hello OPC UA!")

# Set the variable to be writable by the client
my_var.set_writable()

# Start the server
server.start()

print("Server is running at {}".format(server.endpoint))

try:
    # Keep the server running and update variable data
    while True:
        time.sleep(1)
        # You can update the variable value dynamically
        my_var.set_value(random.random())
except KeyboardInterrupt:
    print("Server stopped.")
finally:
    server.stop()
