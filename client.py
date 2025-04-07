from opcua import Client, ua
import sys

if len(sys.argv) < 2:
    print("Usage: python3 client.py <NodeId> [--secure]")
    print("Example: python3 client.py ns=2;s=CV1002PositionFeedbackAI_ENG --secure")
    sys.exit(1)

node_id = sys.argv[1]
use_secure = "--secure" in sys.argv

# Endpoint
endpoint = "opc.tcp://127.0.0.1:4840/freeopcua/server/"

# Set up client with or without security
client = Client(endpoint)
client.set_user("useer1")
client.set_password("pass123")
if use_secure:
    client.set_security([ua.SecurityPolicyType.NoSecurity])
    # client.set_security(
    #     mode=ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
    #     certificate_path="certs/client_cert.pem",
    #     private_key_path="certs/client_key.pem",
    #     server_certificate_path="certs/server_cert.pem"
    # )

    print("Using secure connection with Basic256Sha256_SignAndEncrypt")
else:
    print("Using insecure connection")
client = Client(endpoint)


try:
    client.connect()
    print(f"Connected to OPC-UA server")

    # Get node and value
    node = client.get_node(node_id)
    value = node.get_value()
    print(f"Value of {node_id}: {value}")

finally:
    client.disconnect()
    print("Disconnected from OPC-UA server")
