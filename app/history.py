class HistoryStore:
    """
    History store all the commands
    """
    entries: list[str]

    def __init__(self):
        self._entries = []

    def add(self, entry: str):
        self._entries.append(entry)

    def list(self):
        return self._entries

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)