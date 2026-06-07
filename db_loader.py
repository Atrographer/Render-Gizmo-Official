import json
import os
from my_engine import HomeGrownIndex, DictionaryDocument

def load_local_dictionary(json_filename: str, engine_instance: HomeGrownIndex) -> int:
    if not os.path.exists(json_filename):
        return 0
    try:
        with open(json_filename, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
        documents_to_add = []
        for item in raw_data:
            word = item.get("word")
            definition = item.get("definition")
            if not word or not definition:
                continue
            doc = DictionaryDocument(
                word=word,
                part_of_speech=item.get("part_of_speech", "unknown"),
                definition=definition,
                synonyms=item.get("synonyms", []),
                antonyms=item.get("antonyms", [])
            )
            documents_to_add.append(doc)
        engine_instance.add_documents(documents_to_add)
        return len(documents_to_add)
    except:
        return 0
