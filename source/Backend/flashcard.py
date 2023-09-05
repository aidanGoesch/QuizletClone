# file that will hold the flashcard class
# Class will inherit from a button - clickable - will change what text is displayed when clicked

class FlashCard:
    def __init__(self, term: str, definition: str, familiarity: int = 0) -> None:
        self.familiarity = familiarity  # -1 = Flashcards only, 1 = MCQ, 2 = Write

        self._term = self.make_multi_line(term)
        self._definition = self.make_multi_line(definition)

    @property
    def term(self):
        return self._term

    @property
    def definition(self):
        return self._definition

    def __repr__(self):
        return f"FlashCard('{self._term}', '{self._definition}')"

    def __eq__(self, other):
        return self.term == other.term and self.definition == other.definition

    def __hash__(self):
        return hash((self._term, self._definition))

    def make_multi_line(self, text: str):
        """max chars per line is 40 -- Add functionality to check
        if the definition exceeds a max character length - truncate with ..."""
        word_list = text.split()

        chars = 0
        for i in range(len(word_list)):
            temp = chars + len(word_list[i]) + 1
            if temp > 40:
                word_list[i - 1] += '\n'  # Insert newline character to the previous word
                chars = len(word_list[i])
            else:
                chars = temp

        return ' '.join(word_list)


if __name__ == '__main__':
    f = FlashCard('Apple', 'A fruit')
    print(f.term)