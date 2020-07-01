from abc import ABC, abstractmethod
from dataclasses import dataclass
from database import models
from more_itertools.more import split_before
import pickle
from psqlextra.util import postgres_manager
import os
import pathlib

# Error if I used Pathlib, confirm if it works before recommending :
#     PATH_COLS = os.path.join(str(pathlib.Path(__file__).parent[1]), 'cols')
# TypeError: 'WindowsPath' object is not subscriptable

PATH_COLS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cols")
ALL_COLS = os.path.join(PATH_COLS, 'cols.pk')


class Interface(ABC):

    @classmethod
    def clear_and_fill(cls, model, file_obj):
        model.objects.all().delete()
        instance_ = cls(model, file_obj)
        instance_.uploaded_file_rows = 0
        instance_.inserts = 0
        instance_.create_database()
        instance_.final_rows = model.objects.count()
        instance_.failures = instance_.uploaded_file_rows - instance_.inserts

        return instance_

    @classmethod
    def update_or_create(cls, model, file_obj):
        instance_ = cls(model, file_obj)
        instance_.uploaded_file_rows = 0
        instance_.update_database()
        instance_.final_rows = model.objects.count()
        instance_.inserts = instance_.final_rows - instance_.initial_rows
        instance_.failures = instance_.uploaded_file_rows - instance_.inserts
        return instance_

    def __init__(self, model, file_obj):
        self.model = model
        self.file_obj = file_obj

        self.all_cols = self.get_cols(
            ALL_COLS) + ["ISIN", "DATE"]

        self.model_cols = self.get_cols(
            PATH_COLS, f'{self.model.__name__}.pk')

        self.initial_rows = model.objects.count()

    @staticmethod
    def get_cols(*args):
        
        with open(os.path.join(*args), "rb") as p:
            cols = pickle.load(p)
        return cols

    def create_database(self):
        for chunk in self.get_data(self.file_obj):

            self.inserts += len(chunk)
            self.model.objects.bulk_create(

                [
                    {
                        key: val
                        for key, val in dict(
                            zip(self.all_cols, i)
                        ).items() if key in self.model_cols
                    }
                    for i in chunk
                ], ignore_conflicts=True)

    @staticmethod
    def get_data(file_obj):
        # return iterator (type annotations are conflicting with the comments in vscode)

        # these are the value of the dict only the keys are `cols` in the `main`

        def chunk_to_dict_values(chunk):
            # get value at index 1 and 2
            isin, date = chunk[0].split("##")[1:3]

            chunk = chunk[1:]

            return [(i.split("##")[2:] + [isin, date])
                    for i in chunk]   # this is a list of lists
            
        # from nodeirc by @_habnabit
        for chunk in split_before(
            (l.decode().strip() for l in file_obj),
                lambda l: l.startswith('01')):
            if len(chunk) <= 1:
                continue
            yield chunk_to_dict_values(chunk)
        # from nodeirc by @_habnabit

    @abstractmethod
    def update_database(self):
        pass
