import os
import pickle
import gzip
import pandas as pd
import matplotlib.pyplot as plt
from batteryabn import logger, Constants as Const

def create_filesystem_repository():
    return FileSystemRepository()

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

        cell_dir = self.get_cell_dir(project, cell_name)
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

        cell_dir = self.get_cell_dir(project, cell_name)
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
        cell_dir = self.get_cell_dir(project, cell_name)
        if not os.path.exists(cell_dir):
            os.makedirs(cell_dir)

        # Save image to a local png file
        file_path = os.path.join(cell_dir, f'{cell_name}_{image_name}.png')
        img.savefig(file_path)

        logger.info(f'Saved image to local file: {file_path}')

    def save_html(self, project: str, cell_name: str, html_name: str, html: str):
        """
        Save an html string to a local html file.

        Parameters
        ----------
        project : str
            The name of the project
        cell_name : str
            The name of the cell
        html_name : str
            The name of the html
        html : str
            The html to save
        """
        cell_dir = self.get_cell_dir(project, cell_name)
        if not os.path.exists(cell_dir):
            os.makedirs(cell_dir)

        # Save html to a local html file
        file_path = os.path.join(cell_dir, f'{cell_name}_{html_name}.html')
        with open(file_path, 'w') as f:
            f.write(html)

        logger.info(f'Saved html to local file: {file_path}')

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
    
    def get_cell_dir(self, project: str, cell_name: str):
        """
        Get the directory for a cell.

        Parameters
        ----------
        project : str
            The name of the project
        cell_name : str
            The name of the cell

        Returns
        -------
        str
            The directory for the cell
        """
        return os.path.join(self.root_directory, project, cell_name)
    
    def get_cell_imgs_paths(self, project: str, cell_name: str):
        """
        Get the paths for the images of a cell.

        Parameters
        ----------
        project : str
            The name of the project
        cell_name : str
            The name of the cell

        Returns
        -------
        tuple
            The paths for the images of the cell
        """
        cell_dir = self.get_cell_dir(project, cell_name)
        return os.path.join(cell_dir, f'{cell_name}_cell.png'), os.path.join(cell_dir, f'{cell_name}_ccm.png'), os.path.join(cell_dir, f'{cell_name}_ccm_aht.png')
    
    def get_cell_htmls_paths(self, project: str, cell_name: str):
        """
        Get the path for the html of a cell.

        Parameters
        ----------
        project : str
            The name of the project
        cell_name : str
            The name of the cell

        Returns
        -------
        str
            The path for the html of the cell
        """
        cell_dir = self.get_cell_dir(project, cell_name)
        return os.path.join(cell_dir, f'{cell_name}_cell.html'), os.path.join(cell_dir, f'{cell_name}_ccm.html'), os.path.join(cell_dir, f'{cell_name}_ccm_aht.html')