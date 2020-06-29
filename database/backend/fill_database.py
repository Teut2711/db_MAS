from database import models
import pickle
import pandas as pd
import os
import pathlib
from more_itertools.more import split_before
from time import time



def main(file_obj):

    

    cols_df = get_cols(PATH, 'cols', 'cols.pk') + ["ISIN", "Date"]
   
#  //  cols_DEMATHOL = get_cols(PATH, 'cols', 'Demathol.pk')

    for dataset in read_file_obj(file_obj):
        data_list = map(lambda x: dict(zip(cols_df, x)),  dataset)
        objects = list(
            map(lambda x: get_dematad_objects(cols_dematad, x), data_list))
        models.Dematad.bulk_create(objects, ignore_conficts=True)

# //    update_DEMATHOL(cols_DEMATHOL, data_list)
