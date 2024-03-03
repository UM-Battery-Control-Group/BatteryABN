import pandas as pd

from batteryabn import logger, Constants
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
        self.timezone = timezone if timezone else Constants.DEFAULT_TIME_ZONE_INFO

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
        rename_dict = getattr(Constants, f'{test_type.upper()}_RENAME_DICT')
        df = Utils.rename_columns(df, rename_dict)

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