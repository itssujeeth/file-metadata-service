from datetime import datetime


class Metadata:
    def __init__(self, file_name, hex_digest, file_size, word_count, unique_words, date=None):
        self.file_name = file_name
        self.hex_digest = hex_digest
        self.file_size = file_size
        self.word_count = word_count
        self.unique_words = unique_words
        self.date = date if date else datetime.now().strftime("%Y%m%d-%H%M")

    def to_dict(self):
        return {
            "file_name": self.file_name,
            "hex_digest": self.hex_digest,
            "file_size": self.file_size,
            "word_count": self.word_count,
            "unique_words": self.unique_words,
            "date": self.date
        }