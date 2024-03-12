import os
import logging
import dotenv
import json
import yaml
import pandas as pd
import numpy as np
from batteryabn import logger


class Utils:
    def load_env(env_path: str) -> None:
        """
        Load environment variables from .env file

        Parameters
        ----------
        env_path : str
            Path to .env file
        """
        logger.info(f'Load environment variables from {env_path}')
        dotenv.load_dotenv(env_path, override=True)
        # Set logger level
        if os.getenv('ENV') == 'dev':
            logger.info('Set logger level to DEBUG')
            logger.setLevel(logging.DEBUG)  
        else:
            logger.info('Set logger level to INFO')
            logger.setLevel(logging.INFO)

    def load_config(config_path: str) -> dict:
        """
        Load config file from path

        Parameters
        ----------
        config_path : str
            Path to config file

        Returns
        -------
        dict
            Config file as a dictionary
        """
        logger.info(f'Load config file from {config_path}')
        config = None

        if not os.path.exists(config_path):
            raise FileNotFoundError(f'Config file not found at {config_path}')

        # Try to load config file as yaml
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info('Loaded config file as yaml')
                return config
        except yaml.YAMLError:
            logger.debug('Config file is not yaml')

        # Try to load config file as json
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                logger.info('Loaded config file as json')
                return config
        except json.decoder.JSONDecodeError:
            logger.debug('Config file is not json')

        # If config file is not yaml or json, raise an error
        raise ValueError('Config file is not yaml or json')
    
    def formate_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Format column names of a DataFrame

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to format column names

        Returns
        -------
        pd.DataFrame
            DataFrame with formatted column names
        """
        logger.info(f'Format column names of DataFrame')
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.strip()
        return df

    def rename_columns(df: pd.DataFrame, rename_dict: dict) -> pd.DataFrame:
        """
        Rename columns of a DataFrame

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to rename columns
        rename_dict : dict
            Dictionary with old column names as keys and new column names as values

        Returns
        -------
        pd.DataFrame
            DataFrame with renamed columns
        """
        logger.info(f'Rename columns of DataFrame')
        logger.debug(f"Columns name before renaming: {df.columns.tolist()}")

        # Normalize rename_dict keys to lower case and strip
        rename_dict = {k.lower().strip(): v for k, v in rename_dict.items()}

        df = df.rename(columns=rename_dict)
        logger.debug(f"Columns name after renaming: {df.columns.tolist()}")
        return df

    def drop_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """
        Drop columns from a DataFrame

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to drop columns
        columns : list
            List of columns to drop

        Returns
        -------
        pd.DataFrame
            DataFrame with dropped columns
        """
        logger.info(f'Drop {len(columns)} columns from DataFrame')
        df = df.drop(columns=columns)
        return df

    def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
        """
        The function drops empty rows from DataFrame

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to drop empty rows from

        Returns
        -------
        df : pandas.DataFrame
            Pandas DataFrame with the empty rows dropped
        """
        all_na_count = (df.isna().all(axis=1)).sum()
        if all_na_count > 0:
            logger.info(f'Drop {all_na_count} empty rows')
            df = df.dropna(how='all')

        return df
    
    def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        The function drops unnamed columns from DataFrame

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to drop unnamed columns from.

        Returns
        -------
        df : pandas.DataFrame
            Pandas DataFrame with the unnamed columns dropped.
        """
        logger.info('Drop unnamed columns')
        unnamed_column_list = df.filter(like='Unnamed', axis=1).columns
        df = Utils.drop_columns(df, unnamed_column_list)

        return df
    
    def add_column(df: pd.DataFrame, column_name: str, value: any = np.nan) -> pd.DataFrame:
        """
        Add a column to a DataFrame

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to add column
        column_name : str
            Name of the column to add
        value : any, optional
            Value to add to the column

        Returns
        -------
        pd.DataFrame
            DataFrame with added column
        """
        logger.info(f'Add column {column_name} to DataFrame')
        df[column_name] = value * len(df)
        return df

    def set_value(df: pd.DataFrame, column_name: str, indexs: list[int], value: any) -> pd.DataFrame:
        """
        Set a value in a DataFrame

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to set value
        column_name : str
            Name of the column to set value
        index : list of int
            Indexs to set value
        value : any
            Value to set

        Returns
        -------
        pd.DataFrame
            DataFrame with set value
        """
        logger.info(f'Set value in DataFrame')
        for index in indexs:
            df.at[index, column_name] = value
        return df

    def format_dict(data: dict) -> dict:
        """
        Format dictionary keys to lower case and strip

        Parameters
        ----------
        data : dict
            Dictionary to format

        Returns
        -------
        dict
            Formatted dictionary
        """
        logger.info('Format dictionary keys to lower case and strip')
        return {k.strip(): v.strip() for k, v in data.items() if v is not None}