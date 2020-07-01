from .nsdl import dematad
from database import models
from configparser import RawConfigParser

config = RawConfigParser()
config.read('config.cfg')


def main(file_obj):
    if config["RUN"]["TASK"] == "CREATE":
        stats_Dematad = dematad.Dematad.clear_and_fill(
            models.Dematad, file_obj)
    elif config["RUN"]["TASK"] == "UPDATE":
        stats_Dematad = dematad.update_or_create(
            models.Dematad, file_obj)
        
    return {
        "uploadedFileRows": stats_Dematad.uploaded_file_rows,
        "finalRows": stats_Dematad.final_rows,
        "rowsInserted": stats_Dematad.inserts,
        "rowsFailed": stats_Dematad.failures
    }
