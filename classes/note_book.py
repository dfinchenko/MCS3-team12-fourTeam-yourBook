from classes import Note
from collections import UserDict
import json
import os


class NotesBook(UserDict):
    def add_note(self, note):
        if isinstance(note, Note):
            self.data[note.title.value] = note

    def find(self, title):
        return self.data.get(title)
    
    def search(self, term):
        matches = []
        for note in self.data.values():
            if term.lower() in note.title.value.lower() or term.lower() in note.description.value.lower():
                matches.append(note)
        return matches

    def delete(self, title):
        if title in self.data:
            del self.data[title]


    def load_notes(self, filename):
        if not os.path.isfile(filename):
            self.data = {}
            return

        with open(filename, 'r', encoding='utf-8') as file:
            notes_list = json.load(file)

            for note_dict in notes_list:
                title = note_dict['title']
                description = note_dict.get('description')

                note = Note(title, description)

                self.add_note(note)


    def save_notes(self, filename):
        with open(filename, 'w') as file:
            notes_list = []
            for note in self.data.values():
                note_dict = {
                    'title': note.title.value if note.title else None,
                    'description': note.description.value if note.description else None,
                }
                notes_list.append(note_dict)

            
            json.dump(notes_list, file, ensure_ascii=False)
