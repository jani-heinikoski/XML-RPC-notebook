# Author: Jani Heinikoski
# Created: 22.03.2022
# Description: Data access functionality for saving data to the mock xml-database
# Sources: xml.etree.ElementTree — The ElementTree XML API — Python 3.9.11 documentation (2022). Available at: https://docs.python.org/3.9/library/xml.etree.elementtree.html (Accessed: 22 March 2022).
import xml.etree.ElementTree as ET
from os.path import exists

class DAO:
    def __init__(self, db_path: str) -> None:
        if (exists(db_path)):
            self.tree = ET.parse(db_path)
            self.root = self.tree.getroot()
        else:
            raise FileNotFoundError(db_path)
    # Find and return the topic element under root
    def _find_topic(self, topic: str) -> ET.Element:
        for t in self.root.findall('topic'):
            print(t.get("name"))
            if (t.get("name") == topic):
                return t
        return None
    # Construct a new note element to be saved in the "database"
    def _construct_note_element(self, note_title: str, content: str, timestamp: str) -> ET.Element:
        note_element = ET.Element("note")
        note_element.set("name", note_title)
        text_element = ET.SubElement(note_element, "text")
        text_element.text = content
        ts_element = ET.SubElement(note_element, "timestamp")
        ts_element.text = timestamp
        return note_element
    # Try to save a note to the database, create a new topic if it does not exist already
    def save_note(self, topic: str, note_title: str, content: str, timestamp: str) -> None:
        if (topic and note_title and content and timestamp):
            new_topic = self._find_topic(topic)
            if (not new_topic):
                new_topic = ET.SubElement(self.root, "topic")
                new_topic.set("name", topic)
            new_topic.append(self._construct_note_element(note_title, content, timestamp))
            self.tree.write("db_example.xml")
        else:
            raise ValueError()


