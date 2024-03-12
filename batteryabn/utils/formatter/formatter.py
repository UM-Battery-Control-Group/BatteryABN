import pandas as pd
import numpy as np
from scipy import integrate

from batteryabn import logger, Constants as Const
from batteryabn.utils import Utils

class Formatter:
    def __init__(self, timezone: str = None):
        """
        A class to format battery test data.

        Parameters
        ----------
        timezone : str, optional
            Timezone to use for formatting
        """
        # Default NY timezone
        self.timezone = timezone if timezone else Const.DEFAULT_TIME_ZONE_INFO

        self.test_data = pd.DataFrame(dtype=object)
        self.metadata = {}
        self.cell_name = None # Cell name for the test data

    def format_data(self, data: pd.DataFrame, metadata: pd.DataFrame, test_type: str) -> pd.DataFrame:
        """
        Format battery test data and metadata.

        Parameters
        ----------
        data : pd.DataFrame
            Raw battery test data

        metadata : dict
            Raw battery test metadata

        test_type : str
            Type of battery test data. Supported types: 'Arbin', 'BioLogic', 'Neware', 'Neware_Vdf'

        Returns
        -------
        pd.DataFrame
            Formatted battery test data
        """
        self.clear()
        self.format_test_data(data, test_type)
        self.format_metadata(metadata)

        return self.test_data

    def format_test_data(self, data: pd.DataFrame, test_type: str) -> None:
        """
        Format battery test data.

        Parameters
        ----------
        data : pd.DataFrame
            Raw battery test data

        test_type : str
            Type of battery test data. Supported types: 'Arbin', 'BioLogic', 'Neware', 'Neware_Vdf'

        is_cycle : bool, optional
            Whether the data is cycle data
        """
        logger.info('Format battery test data')

        if data.empty:
            return
        
        df = data.copy()

        df = Utils.drop_unnamed_columns(df)
        df = Utils.drop_empty_rows(df)
        df = Utils.formate_columns(df)

        # Rename columns based on test type
        rename_dict = getattr(Const, f'{test_type.upper()}_RENAME_DICT')
        df = Utils.rename_columns(df, rename_dict)

        # Format the data based on test type
        if test_type.lower() == 'arbin':
            Utils.add_column(df, Const.TEMPERATURE)
        elif test_type.lower() == 'biologic':
            if(max(abs(df[Const.CURRENT]))>20): 
                # current data is ma vs A divide by 1000.
                df[Const.CURRENT] = df[Const.CURRENT]/1000
                df[Const.AHT] = df[Const.AHT]/1000
        elif test_type.lower() == 'neware':
            if df[Const.TEMPERATURE] is not None:
                df[Const.TEMPERATURE] = np.where((df[Const.TEMPERATURE] >= 200) & (df[Const.TEMPERATURE] <250), np.nan, df[Const.TEMPERATURE]) 
            # TODO: Pass in cycle type and use it 
            if test_type == 'Formation':
                # From integrating current.... some formation files had wrong units
                time_reset = df[Const.TIME].reset_index(drop=True)
                aht_calculated = integrate.cumtrapz(
                    abs(time_reset), 
                    (time_reset - time_reset[0]) / 1000
                ) / 3600
                aht_calculated = np.append(aht_calculated, aht_calculated[-1])
                df[Const.AHT] = aht_calculated


        # Check the data lengths for cycle data
        if test_type.lower() != 'neware_vdf':
            lengths = [len(df[column].reset_index(drop=True)) for column in [Const.TIME, Const.CURRENT, Const.VOLTAGE, Const.STEP_IDX]]
            if len(set(lengths)) > 1:
                raise ValueError(f"Inconsistent data lengths in the dataframe")


        #TODO: Check the timestamp column

        self.test_data = df

    def format_metadata(self, metadata: dict) -> None:
        """
        Format battery test metadata.

        Parameters
        ----------
        metadata : dict
            Raw battery test metadata
        """
        logger.info('Format battery test metadata')

        metadata = Utils.format_dict(metadata)
        self.metadata = metadata

        # Get cell name from metadata
        cell_name = metadata.get('Project Name') + '_' + metadata.get('Cell ID')
        self.cell_name = cell_name

    def clear(self) -> None:
        """
        Clear formatted data and metadata
        """
        self.test_data = pd.DataFrame(dtype=object)
        self.metadata = {}
        self.cell_name = None