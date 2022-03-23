# Author: Jani Heinikoski
# Created: 23.03.2022
from typing import Any, Union, Callable
from xmlrpc.client import ServerProxy
def on_error(e: Exception) -> None:
    print("Something went wrong at the server side.", end="\n\n")
# Function for calling XML-RPC functions and handling their exceptions
def handle_exceptions(f: Callable[..., Any], p: tuple[Any]) -> Any:
    try:
        return f(*p)
    except Exception as e:
        on_error(e)
        return e
# Ask the server to append articles related to topic from Wikipedia's API using search_terms
def send_wikipedia_query_to_server(search_terms: str, topic: str, proxy: ServerProxy) -> Union[bool, Exception]:
    return handle_exceptions(proxy.add_information_to_topic, (search_terms, topic))
# Send a note to be saved to the remote XML-RPC server
def send_note_to_server(note: tuple[str], proxy: ServerProxy) -> Exception:
    return handle_exceptions(proxy.add_note, note)
def fetch_notes_from_server(topic: str, proxy: ServerProxy) -> Union[str, Exception]:
    return handle_exceptions(proxy.fetch_notes, (topic,))