import os
import pickle
import gzip
import pandas as pd
from batteryabn import logger, Constants as Const


class FileSystemRepository:
    def __init__(self):
        self.root_directory = Const.ROOT_DIRECTORY

    def save_to_local_pklgz(self, project: str, cell_name: str, data_name: str, data: pd.DataFrame):
        """
        Save data to a local pickle file and use gzip to compress it.

        Parameters
        ----------
        project : str
            The name of the project
        cell_name : str
            The name of the cell
        data_name : str
            The name of the data
        data : pd.DataFrame
            The data to save
        """

        project_dir = os.path.join(self.root_directory, project)
        cell_dir = os.path.join(project_dir, cell_name)
        if not os.path.exists(cell_dir):
            os.makedirs(cell_dir)

        # Save data to a local pkl.gz file
        file_path = os.path.join(cell_dir, f'{data_name}.pkl.gz')
        with gzip.open(file_path, 'wb') as f:
            pickle.dump(data, f)

        logger.info(f'Saved data to local file: {file_path}')

