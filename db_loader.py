import json
import os

def load_dictionary():
    db_path = os.path.join(os.path.dirname(__file__), "dictionary_db.json")
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading dictionary_db.json: {e}")
        return {"dictionary": {}, "thesaurus": {}}
