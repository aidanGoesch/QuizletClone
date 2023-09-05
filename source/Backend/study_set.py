from source.Backend.flashcard import FlashCard

class StudySet:
    def __init__(self, title: str, flashcards: list[FlashCard], description: str = ""):
        self.title = title
        self.description = description
        self.flashcards = flashcards

    def __repr__(self):
        return f"StudySet('{self.title}', '{self.description}', '{self.flashcards}')"

    def __eq__(self, other):
        return self.description.split() == other.description.split() and self.title == other.title

    def is_empty(self):
        return self.title == '' and self.description == '' and self.flashcards == []


if __name__ == '__main__':
    set1 = StudySet(title = "animals", flashcards=[], description='  ')
    set2 = StudySet(title = "animals", flashcards=[], description='')

    print(set1 == set2)

