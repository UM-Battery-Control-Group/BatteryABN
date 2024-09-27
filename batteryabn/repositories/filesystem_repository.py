import os
import pickle
import gzip
import pandas as pd
import matplotlib.pyplot as plt
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

    def save_df_to_csv(self, project: str, cell_name: str, data_name: str, data: pd.DataFrame):
        """
        Save data to a local csv file.

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

        # Save data to a local csv file
        file_path = os.path.join(cell_dir, f'{cell_name}_{data_name}.csv')
        data.to_csv(file_path, index=False)

        logger.info(f'Saved data to local file: {file_path}')

    def save_plt_to_png(self, project: str, cell_name: str, image_name: str, img: plt.Figure):
        """
        Save an image to a local png file.

        Parameters
        ----------
        project : str
            The name of the project
        cell_name : str
            The name of the cell
        image_name : str
            The name of the image
        img : matplotlib.figure.Figure
            The image to save
        """

        project_dir = os.path.join(self.root_directory, project)
        cell_dir = os.path.join(project_dir, cell_name)
        if not os.path.exists(cell_dir):
            os.makedirs(cell_dir)

        # Save image to a local png file
        file_path = os.path.join(cell_dir, f'{cell_name}_{image_name}.png')
        img.savefig(file_path)

        logger.info(f'Saved image to local file: {file_path}')

    def load_from_local_pklgz(self, project: str, cell_name: str, data_name: str) -> pd.DataFrame:
        """
        Load data from a local pickle file that is compressed with gzip.

        Parameters
        ----------
        project : str
            The name of the project
        cell_name : str
            The name of the cell
        data_name : str
            The name of the data

        Returns
        -------
        pd.DataFrame
            The loaded data
        """

        file_path = os.path.join(self.root_directory, project, cell_name, f'{data_name}.pkl.gz')
        with gzip.open(file_path, 'rb') as f:
            data = pickle.load(f)

        logger.info(f'Loaded data from local file: {file_path}')
        return data