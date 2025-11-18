class HistoryStore:
    """
    History store all the commands
    """
    entries: list[str]

    def __init__(self):
        self._entries = []
        self._last_flushed_index: int = 0  # index of entries already written to file

    def add(self, entry: str):
        self._entries.append(entry)

    def entries(self):
        return self._entries

    def get_new_entries(self) -> list[str]:
        return self._entries[self._last_flushed_index:]

    def mark_flushed(self) -> None:
        self._last_flushed_index = len(self._entries)

    def add_entries_from_file(self, filename: str):
        # removed try except, bcz i want it to err out if file is not found
        with open(filename, "r") as f:
            # self._entries += f.readlines() # but adds extra line
            for line in f:
                line = line.rstrip("\n")
                if line.strip():
                    self._entries.append(line)

    def write_entries_to_file(self, filename: str):
        with open(filename, "w") as f:
            for line in self._entries:
                f.write(line + "\n")
        self.mark_flushed()

    def append_entries_to_file(self, filename: str):
        new_entries = self.get_new_entries()
        if not new_entries:
            return

        with open(filename, "a") as f:  # APPEND mode, creates file if missing
            for line in new_entries:
                f.write(line + "\n")

        self.mark_flushed()

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)