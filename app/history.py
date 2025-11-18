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

    def add_entries_from_file(self, filename: str):
        try:
            with open(filename, "r") as f:
                # self._entries += f.readlines() # but adds extra line
                for line in f:
                    line = line.rstrip("\n")
                    if line.strip():
                        self._entries.append(line)

        except FileNotFoundError:
            ...

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)