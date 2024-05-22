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
        self.last_update_time = None # Last update timestamp for the test data

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
            Type of battery test data. Supported types: 'Arbin', 'BioLogic', 'Neware', 'Vdf'

        Returns
        -------
        pd.DataFrame
            Formatted battery test data
        """
        self.clear()
        self.format_metadata(metadata)
        self.format_test_data(data, test_type)

        return self.test_data

    def format_test_data(self, data: pd.DataFrame, test_type: str) -> None:
        """
        Format battery test data.

        Parameters
        ----------
        data : pd.DataFrame
            Raw battery test data

        test_type : str
            Type of battery test data. Supported types: 'Arbin', 'BioLogic', 'Neware', 'Vdf'

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
        if test_type != Const.VDF:
            Utils.add_column(df, Const.TEMPERATURE)
            Utils.add_column(df, Const.STEP_IDX)
        elif test_type == Const.BIOLOGIC:
            if(max(abs(df[Const.CURRENT]))>20): 
                # current data is ma vs A divide by 1000.
                df[Const.CURRENT] = df[Const.CURRENT]/1000
                # TODO: AHT sometime is missing in the data. Assign it to 0 if it is missing
                if Const.AHT not in df.columns:
                    df[Const.AHT] = 0
                else:   
                    df[Const.AHT] = df[Const.AHT]/1000 
            if Const.STEP_IDX not in df.columns:
                df[Const.STEP_IDX] = 0
        elif test_type == Const.NEWARE:
            if df[Const.TEMPERATURE] is not None:
                df[Const.TEMPERATURE] = np.where((df[Const.TEMPERATURE] >= 200) & (df[Const.TEMPERATURE] <250), np.nan, df[Const.TEMPERATURE]) 
            
            # Formate the time column from HH:MM:SS.fff to seconds
            df[Const.TIME] = Utils.time_str_series_to_seconds(df[Const.TIME])

            # For the formation test, calculate AHT from integrating current, 
            # TODO: Check if the timestamp column is uesed correctly when calculating AHT
            # if self.metadata.get('Test Type').lower() == 'f':
            # From integrating current.... some formation files had wrong units
        time_reset = df[Const.TIMESTAMP].reset_index(drop=True)
        print(f"Time reset: {time_reset}")
        current_reset = df[Const.CURRENT].reset_index(drop=True)
        aht_calculated = integrate.cumtrapz(
            abs(current_reset), 
            (time_reset - time_reset[0]).dt.total_seconds(),
        ) / 3600
        aht_calculated = np.append(aht_calculated, aht_calculated[-1])
        df[Const.AHT] = aht_calculated

        # Check the data lengths for cycle data
        if test_type != Const.VDF:
            lengths = [len(df[column].reset_index(drop=True)) for column in [Const.TIME, Const.CURRENT, Const.VOLTAGE]]
            if len(set(lengths)) > 1:
                raise ValueError(f"Inconsistent data lengths in the dataframe")

        if not df.empty and Const.TIMESTAMP in df.columns:
            last_timestamp_value = df[Const.TIMESTAMP].iloc[-1]
            if isinstance(last_timestamp_value, pd.Timestamp):
                self.last_update_time = Utils.timestamp_to_int(last_timestamp_value)
            else:
                self.last_update_time = int(last_timestamp_value)

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