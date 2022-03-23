# Author: Jani Heinikoski
# Created: 22.03.2022
# Description: Data access functionality for saving data to the mock xml-database
# Sources: xml.etree.ElementTree — The ElementTree XML API — Python 3.9.11 documentation (2022). Available at: https://docs.python.org/3.9/library/xml.etree.elementtree.html (Accessed: 22 March 2022).
import xml.etree.ElementTree as ET
from os.path import exists
import requests

DB_PATH = "db.xml"

class DAO:
    def __init__(self) -> None:
        if (exists(DB_PATH)):
            self.tree = ET.parse(DB_PATH)
            self.root = self.tree.getroot()
        else:
            raise FileNotFoundError(DB_PATH)
    # Find and return the topic element under root, create a new one if it does not exist
    def _find_topic(self, topic: str) -> ET.Element:
        topic_to_find = None
        for t in self.root.findall('topic'):
            if (t.get("name") == topic):
                topic_to_find = t
                break
        if (not topic_to_find):
            topic_to_find = ET.SubElement(self.root, "topic")
            topic_to_find.set("name", topic)
        return topic_to_find
    # Find a topic's extra -element which contains related Wikipedia articles
    def _find_topic_extra(self, topic: ET.Element) -> ET.Element:
        extra_to_find = topic.find("extra")
        if (not extra_to_find):
            extra_to_find = ET.Element("extra")
            topic.append(extra_to_find)
        return extra_to_find
    # Add an article element to the extra section
    def _append_article_to_extra(self, extra: ET.Element, article: str) -> None:
        ET.dump(self.root)
        a = ET.Element("article")
        a.set("URL", article)
        extra.append(a)
    # Find articles based on search_terms from the Wikipedia's API
    def _find_articles(self, search_terms: str) -> list[str]:
        session = requests.Session()
        URL = "https://en.wikipedia.org/w/api.php"
        PARAMS = {
            "action": "opensearch",
            "namespace": "0",
            "search": search_terms,
            "limit": "1",
            "format": "json"
        }
        try:
            response = session.get(url=URL, params=PARAMS)
            return response.json()[3]
        except:
            return []
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
            t = self._find_topic(topic)
            t.append(self._construct_note_element(note_title, content, timestamp))
            self.tree.write(DB_PATH)
        else:
            raise ValueError()
    # Query the Wikipedia API and add links of articles to a topic
    def add_info_to_topic(self, search_terms: str, topic: str) -> bool:
        if (search_terms and topic):
            extra = self._find_topic_extra(self._find_topic(topic))
            articles = self._find_articles(search_terms)
            if (articles):
                for article in articles:
                    self._append_article_to_extra(extra, article)
                    self.tree.write(DB_PATH)
                return True
        else:
            raise ValueError()
        return False
    # Fetch notes from the database. Sends everything if no topic given
    def fetch_notes(self, topic: str = None) -> str:
        if (not topic):
            return ET.tostring(self.root, encoding="unicode")
        topic_to_find = None
        for t in self.root.findall('topic'):
            if (t.get("name") == topic):
                topic_to_find = t
                break
        return ET.tostring(topic_to_find, encoding="unicode") if topic_to_find else ""
        
