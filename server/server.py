# Author: Jani Heinikoski
# Created: 22.03.2022
# Sources: 
# xmlrpc.server — Basic XML-RPC servers — Python 3.9.11 documentation 2022. Available at: https://docs.python.org/3.9/library/xmlrpc.server.html#module-xmlrpc.server (Accessed: 22 March 2022).
from xmlrpc.server import SimpleXMLRPCServer
from rpc_functions import RPCFunctions

def start_xml_rpc_server(host: str, port: int):
    try:
        with SimpleXMLRPCServer((host, port)) as server:
            server.register_instance(RPCFunctions)
            server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting server")
        exit(0)

if __name__ == "__main__":
    start_xml_rpc_server("localhost", 3000)

