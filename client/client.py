# Author: Jani Heinikoski
# Created: 22.03.2022
# Sources: xmlrpc.client — XML-RPC client access — Python 3.9.11 documentation (2022). Available at: https://docs.python.org/3.9/library/xmlrpc.client.html#module-xmlrpc.client (Accessed: 22 March 2022).
from comms import *
import xml.etree.ElementTree as ET
from xmlrpc.client import ServerProxy
from datetime import datetime
from typing import NoReturn
SERVER_ADDRESS = "http://localhost:3000/"
# Construct the note as user input from stdin using input
def get_note_from_user() -> tuple[str]:
    topic = input("Give a topic for the note: ")
    note_title = input("Give a title for the note: ")
    content = input("Give the content of the note: ")
    timestamp = datetime.now().strftime(r"%d/%m/%Y - %H:%M:%S")
    return topic, note_title, content, timestamp
# Get the topic and search terms from stdin for querying the Wikipedia API
def get_topic_search_terms() -> str:
    topic = input("Give a topic: ")
    st = input("Give search terms for Wikipedia: ")
    return st, topic
# Print the notes received from the server as an XML-string
def print_notes(xml: str) -> None:
    def handle_topic(topic: ET.Element):
        print("Topic : ", topic.get("name"))
        extra_element = None
        for child in topic:
            if (child.tag == "note"):
                print("Note : ", child.get("name"))
                print("\t- ", child.find("text").text)
                print("\t- Created - ", child.find("timestamp").text)
            elif (child.tag == "extra"):
                extra_element = child
        if (extra_element):
            print("Articles related to topic:",)
            for article in extra_element:
                print(article.get("URL"))
    try:
        root = ET.fromstring(xml)
        if (len(list(root)) == 0):
            print("No notes in the database")
            return None
        if (root.tag == "data"):
            for topic in root:
                handle_topic(topic)
                print("\n----------------------------------------------")
        elif (root.tag == "topic"):
            handle_topic(root)
    except:
        pass
# CLI-loop for interacting with the user
def cli(proxy: ServerProxy) -> NoReturn:
    MENU = ("1) Create a new note", "2) Add articles to topic from Wikipedia", "3) Find notes", "0) Exit")
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
            print("New note created" if not send_note_to_server(note, proxy) else "", end="\n\n")
        elif (option == "2"):
            ts = get_topic_search_terms()
            print("Sending the request to the server...", end="\n\n")
            res = send_wikipedia_query_to_server(*ts, proxy)
            if (res == True):
                print("Articles added successfully!", end="\n\n")
            else:
                print("No articles found based on the search terms", end="\n\n")
        elif (option == "3"):
            topic = input("Enter a topic (empty to get all topics): ")
            print("Sending the request to the server...", end="\n\n")
            res = fetch_notes_from_server(topic, proxy)
            if (isinstance(res, str)):
                print_notes(res)
                print(end="\n\n")
# Establish connection with the XML-RPC-server and begin the CLI-loop
def start_client(uri: str) -> None:
    try:
        with ServerProxy(uri, allow_none=True) as p:
            cli(p)
    except KeyboardInterrupt:
        print("Exiting client due to keyboard interrupt...")
        exit(0)
    
if __name__ == "__main__":
    start_client(SERVER_ADDRESS)

