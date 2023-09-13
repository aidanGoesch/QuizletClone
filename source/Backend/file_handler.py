import pathlib
import csv

from source.Backend.study_set import StudySet
from source.Backend.flashcard import FlashCard
from source.Backend.Log.logging import log


class Loader:
    def __init__(self):
        self.file_path = pathlib.Path("source/Backend/Sets")

        if not self.file_path.exists(): # changes filepath to work from repo
            self.file_path = pathlib.Path("./Backend/Sets")

    def get_set_names(self):
        names = []
        for file in self.file_path.iterdir():
            names.append(file.name[:-4])

        return names

    def get_data_from_file(self, file_name: str):
        data = []
        with open(f'{self.file_path}/{file_name}.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                row = [x for x in row if x != '']
                data.append(row)

        study_set = convert_data_to_study_set(data)
        # print(study_set)
        return study_set

class Writer:
    def __init__(self, study_set: StudySet):
        self.file_path = pathlib.Path("source/Backend/Sets")

        if not self.file_path.exists(): # changes filepath to work from repo
            self.file_path = pathlib.Path("./Backend/Sets")

        self.study_set = study_set

    def get_set_names(self):
        names = []
        for file in self.file_path.iterdir():
            names.append(file.name)

        return names

    def write_data_to_file(self):
        if not self.overriding():  # if the file has the same description as the one that is trying to be saved then it is considered saving - otherwise it is considered overriding
            file_path = f'{self.file_path}/{self.study_set.title}.csv'
        else:
            for i in range(1, 11):
                if not pathlib.Path(f'{self.file_path}/{self.study_set.title}-{i}.csv').exists():
                    break
            else:
                log('override limit exceeded')
            file_path = f'{self.file_path}/{self.study_set.title}-{i}.csv'
            self.study_set.title = f'{self.study_set.title}-{i}'

        data = convert_study_set_to_data(self.study_set)
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def overriding(self):
        if pathlib.Path(f'{self.file_path}/{self.study_set.title}.csv').exists():
            temp_set = Loader().get_data_from_file(self.study_set.title)
            return temp_set != self.study_set
        return False




def delete_set(file_name: str):
    try:
        file_path = pathlib.Path(f"source/Backend/Sets/{file_name}.csv")

        if not file_path.exists():  # changes filepath to work from repo
            file_path = pathlib.Path(f"./Backend/Sets/{file_name}.csv")

        if file_path.exists():
            file_path.unlink()
            return True
        else:
            return False
    except Exception as e:
        # Log the error or handle it in an appropriate way, e.g., show an error message to the user.
        log(f"Error deleting set {file_name}: {str(e)}")
        return False





def convert_data_to_study_set(data: list[list]) -> StudySet:
    temp = StudySet("", [])
    temp.title = data[0][0]
    temp.description = data[1][0]

    for i in range(2, len(data)):
        try:
            temp.flashcards.append(FlashCard(term = data[i][0], definition = data[i][1]))
        except IndexError:
            log(f"ERROR: Missing term value")

    return temp

def convert_study_set_to_data(study_set: StudySet) -> list[list]:
    temp = [[study_set.title], [study_set.description]]

    for card in study_set.flashcards:
        temp.append([card.term, card.definition])

    return temp




if __name__ == '__main__':
    # w = Writer(StudySet("Fruits", [FlashCard("Apple", "A Fruit"),
    #                                FlashCard("Orange", "Another Fruit")],
    #                     description="something else hopefully this works"))
    # w.write_data_to_file()

    print(Loader().get_set_names())
    Loader().get_data_from_file("Fruits")