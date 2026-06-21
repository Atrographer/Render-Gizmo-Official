import re

class DictionaryDocument:
    def __init__(self, word, part_of_speech, definition, synonyms=None, antonyms=None):
        self.word = word.lower().strip()
        self.part_of_speech = part_of_speech.strip()
        self.definition = definition.strip()
        self.synonyms = [s.lower().strip() for s in (synonyms or [])]
        self.antonyms = [a.lower().strip() for a in (antonyms or [])]

class HomeGrownIndex:
    def __init__(self):
        self.database = []

    def add_documents(self, documents: list):
        for doc in documents:
            self.database.append(doc)

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _extract_keywords(self, sentence: str) -> list[str]:
        cleaned = re.sub(r'[^\w\s]', '', sentence.lower())
        stop_words = {"what", "is", "the", "meaning", "of", "definition", "for", "give", "me", "synonyms", "antonyms", "opposite"}
        return [word for word in cleaned.split() if word not in stop_words]

    def query(self, user_query: str) -> str:
        # Clean the input sentence for uniformity
        cleaned_query = user_query.lower().strip()
        
        # 1. FAST-PATH SHORT CIRCUIT: Check for immediate exact term containment
        for doc in self.database:
            # If the user asks exactly for the word, bypass all fuzzy math loops instantly
            if doc.word == cleaned_query or f" {doc.word} " in f" {cleaned_query} ":
                intent_synonym = any(w in cleaned_query for w in ["synonym", "similar", "means the same"])
                intent_antonym = any(w in cleaned_query for w in ["antonym", "opposite", "contrary"])
                
                word_title = f"**{doc.word.capitalize()}** ({doc.part_of_speech})"
                if intent_synonym:
                    syns = ", ".join(doc.synonyms) if doc.synonyms else "None registered."
                    return f"{word_title}\n* **Synonyms:** {syns}"
                if intent_antonym:
                    ants = ", ".join(doc.antonyms) if doc.antonyms else "None registered."
                    return f"{word_title}\n* **Antonyms:** {ants}"
                return (
                    f"{word_title}\n"
                    f"* **Definition:** {doc.definition}\n"
                    f"* **Synonyms:** {', '.join(doc.synonyms) if doc.synonyms else 'None'}\n"
                    f"* **Antonyms:** {', '.join(doc.antonyms) if doc.antonyms else 'None'}"
                )

        # 2. SLOW-PATH FALLBACK: Fallback to Levenshtein text scoring for typos and natural phrasing
        keywords = self._extract_keywords(user_query)
        if not keywords:
            return "Please type a specific word to look up."

        best_match = None
        best_score = 999
        intent_synonym = any(w in user_query.lower() for w in ["synonym", "similar", "means the same"])
        intent_antonym = any(w in user_query.lower() for w in ["antonym", "opposite", "contrary"])

        for keyword in keywords:
            for doc in self.database:
                distance = self._levenshtein_distance(keyword, doc.word)
                if distance < best_score and distance <= 2:
                    best_match = doc
                    best_score = distance

        if best_match and best_score <= 2:
            word_title = f"**{best_match.word.capitalize()}** ({best_match.part_of_speech})"
            if intent_synonym:
                syns = ", ".join(best_match.synonyms) if best_match.synonyms else "None registered."
                return f"{word_title}\n* **Synonyms:** {syns}"
            if intent_antonym:
                ants = ", ".join(best_match.antonyms) if best_match.antonyms else "None registered."
                return f"{word_title}\n* **Antonyms:** {ants}"
            return (
                f"{word_title}\n"
                f"* **Definition:** {best_match.definition}\n"
                f"* **Synonyms:** {', '.join(best_match.synonyms) if best_match.synonyms else 'None'}\n"
                f"* **Antonyms:** {', '.join(best_match.antonyms) if best_match.antonyms else 'None'}"
            )
            
        return "Word not found in your database dictionary index."


class GizmoEngine:
    def __init__(self, db_data):
        self.index = HomeGrownIndex()
        self.load_from_db(db_data)

    def load_from_db(self, db_data):
        docs = []
        for word, info in db_data.get("dictionary", {}).items():
            doc = DictionaryDocument(
                word=word,
                part_of_speech=info.get("pos", "noun"),
                definition=info.get("definition", ""),
                synonyms=info.get("synonyms", [])
            )
            docs.append(doc)
        self.index.add_documents(docs)

    def lookup(self, user_query: str):
        return self.index.query(user_query)
