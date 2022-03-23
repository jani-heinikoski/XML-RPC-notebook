# Author: Jani Heinikoski
# Created: 22.03.2022
# Description: RPC functions for the server to register
# Sources: 
# xmlrpc.server — Basic XML-RPC servers — Python 3.9.11 documentation 2022. Available at: https://docs.python.org/3.9/library/xmlrpc.server.html#module-xmlrpc.server (Accessed: 22 March 2022).
from data_access import DAO

class RPCFunctions:
    @staticmethod
    def add_note(topic: str, note_title: str, content: str, timestamp: str) -> None:
        if (topic and note_title and content and timestamp):
            dao = DAO()
            dao.save_note(topic, note_title, content, timestamp)
    @staticmethod
    def add_information_to_topic(search_terms: str, topic: str) -> bool:
        if (search_terms and topic):
            dao = DAO()
            return dao.add_info_to_topic(search_terms, topic)
        return False
    @staticmethod
    def fetch_notes(topic: str = None) -> str:
        return DAO().fetch_notes(topic)