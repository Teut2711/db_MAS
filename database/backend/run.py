from .nsdl import dematad
from database import models


def main(file_obj):
    if not models.Dematad.objects.exists():
        stats_Dematad = dematad.Dematad.clear_and_fill(
            models.Dematad, file_obj)
    else:
        stats_Dematad = dematad.update_or_create(
            models.Dematad, file_obj)
    return {
        "uploadedFileRows": stats_Dematad.uploaded_file_rows,
        "finalRows": stats_Dematad.final_rows,
        "rowsInserted": stats_Dematad.inserts,
        "rowsFailed": stats_Dematad.failures
    }
