from abc import ABCMeta
from dataclasses import dataclass
from database import models
from more_itertools.more import split_before
import pickle
import os
import pathlib

PATH = os.path.join(pathlib.Path(__file__).parent, 'cols')


class GeneralModel(ABCMeta):

    @classmethod
    def clear_and_fill(cls, model, file_obj):
        model.objects.flush()
        instance_ = cls(model, file_obj)
        instance_.uploaded_file_rows = 0
        instance_.create_database()
        instance_.final_rows = model.objects.count()
        instance_.inserts = instance_.final_rows - instance_.initial_rows
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

        self.all_cols = self.get_cols(
            PATH, 'cols.pk') + ["isin", "Date"]

        self.model_cols = self.get_cols(
            PATH, f'{self.model.__class__.__name__}.pk')

        self.initial_rows = model.objects.count()
    
    
    def create_database(self):
        for chunk in self.get_data(self.file_obj):
            self.inserts += len(chunk)
            self.model.bulk_create(
                self.get_objects(
                    self.model_cols, [dict(zip(self.all_cols, i))
                                      for i in chunk]
                ), ignore_conficts=True)

    def update_database(self):
        for chunk in self.get_data(self.file_obj):
            self.model.bulk_update(
                self.get_objects(
                    self.model_cols, [dict(zip(self.all_cols, i))
                                      for i in chunk]
                ), ignore_conficts=True)

    def empty_model(self):
        self.model.flush()

    @staticmethod
    def get_objects(cols: list, data: dict):
        # This is my `unique_together`(aka composite key if I' m right)
        data = {i: data[i] for i in cols}
        composite_key = data['DPID'] + data['CLID']
        return models.Dematad(**data, defaults=("DEMATAD_DPID_CLID", composite_key))

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
            # //df = pd.DataFrame(data=data, columns=cols)      Unnecessary pandas usage(was using earlier but no longer feel to use it)
            # //df["ISEN"] = isin
            # //df["DATE"] = date
        # from nodeirc by @_habnabit
        for chunk in split_before(
            (l.decode().strip() for l in file_obj),
                lambda l: l.startswith('01')):
            if len(chunk) <= 1:
                continue
            yield chunk_to_dict_values(chunk)
        # from nodeirc by @_habnabit

    @staticmethod
    def get_cols(*args):

        with open(os.path.join(*args), "rb") as p:
            cols = pickle.load(p)
        # //return list(map(lambda x: x.lower(), cols))
        return cols 

    def create_database(self):
            for chunk in self.get_data(self.file_obj):
            self.inserts += len(chunk)
            self.model.bulk_update(
                self.get_objects(
                    self.model_cols, [dict(zip(self.all_cols, i))
                                      for i in chunk]
                ), ignore_conficts=True)
    
    @abstractmethod
    def update_database():
        pass
    






class Dematad(GeneralModel):
    
    def update_database(self):
        for chunk in self.get_data(self.file_obj):
            self.model.bulk_update(
                self.get_objects(
                    self.model_cols, [dict(zip(self.all_cols, i))
                                      for i in chunk]
                ), ignore_conficts=True)
