from collections import defaultdict
import re


class EntityRegistry:
    def __init__(self, entities):
        self.entities = entities
        self.canonical = {}
        self.alias_map = {}
        self.type_index = defaultdict(list)
        self._build()

    def _normalise(self, text):
        if not text:
            return ""
        text = text.strip().lower()
        text = re.sub(r"[^a-z0-9 ]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _make_id(self, entity):
        base = self._normalise(entity.title)
        return f"{entity.type.upper()}::{base}"

    def _build(self):
        for e in self.entities:
            canonical_id = self._make_id(e)
            self.canonical[canonical_id] = e
            self.type_index[e.type].append(canonical_id)
            self.alias_map[self._normalise(e.title)] = canonical_id
            if hasattr(e, "id"):
                self.alias_map[self._normalise(e.id)] = canonical_id

    def resolve(self, name):
        key = self._normalise(name)
        return self.alias_map.get(key)

    def get(self, canonical_id):
        return self.canonical.get(canonical_id)

    def all(self):
        return self.canonical

    def merge_view(self, graph):
        return graph

