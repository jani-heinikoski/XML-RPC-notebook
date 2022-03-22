# Author: Jani Heinikoski
# Created: 22.03.2022
# Sources: xmlrpc.client — XML-RPC client access — Python 3.9.11 documentation (2022). Available at: https://docs.python.org/3.9/library/xmlrpc.client.html#module-xmlrpc.client (Accessed: 22 March 2022).
from xmlrpc.client import ServerProxy
from datetime import datetime
# Construct the note as user input from stdin using input
def get_note_from_user() -> tuple[str]:
    topic = input("Give a topic for the note: ")
    note_title = input("Give a title for the note: ")
    content = input("Give the content of the note: ")
    timestamp = datetime.now().strftime(r"%d/%m/%Y - %H:%M:%S")
    return topic, note_title, content, timestamp

def send_note_to_server(note: tuple[str], proxy: ServerProxy) -> Exception:
    try:
        proxy.add_note(*note)
    except Exception as e:
        print("Something went wrong at the server side.")
        print("Contact the server administrator")
        return e
    return None

# CLI-loop for interacting with the user
def cli(proxy: ServerProxy) -> None:
    MENU = ("1) Create a new note", "0) Exit")
    option = None
    e = None
    while (True):
        print(*MENU, sep="\n", end="\n\n")
        option = input("Choose an option: ")
        if (option == "0"):
            print("Exiting client...")
            exit(0)
        elif (option == "1"):            
            note = get_note_from_user()
            print("Sending the note to the server...", end="\n\n")
            e = send_note_to_server(note, proxy)
            print(e, end="\n\n")

# Establish connection with the XML-RPC-server and begin the CLI-loop
def start_client(uri: str) -> None:
    try:
        with ServerProxy(uri) as p:
            cli(p)
    except KeyboardInterrupt:
        print("Exiting client due to keyboard interrupt...")
        exit(0)
    
if __name__ == "__main__":
    start_client("http://localhost:3000/")
 

