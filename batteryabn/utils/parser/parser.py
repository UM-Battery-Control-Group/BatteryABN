import os
import re
import pandas as pd
from galvani import BioLogic

from batteryabn import logger, Constants as Const

class Parser:
    def __init__(self):
        """
        A class to parse data from battery test data files.
        """
        self.test_name = None
        self.test_type = None
        self.raw_test_data = pd.DataFrame(dtype=object)
        self.raw_metadata = {}
        # Define parse functions
        self.parse_functions = {
            Const.ARBIN: self.parse_arbin,
            Const.BIOLOGIC: self.parse_biologic,
            Const.NEWARE: self.parse_neware,
            Const.VDF: self.parse_vdf,
        }

    def parse(self, file_path: str) -> None:
        """
        Parse data from battery test data files.
        Supported test types: 'BioLogic', 'Neware', 'Vdf'
        The data will be stored in the attributes of the class.

        Parameters
        ----------
        file_path : str
            Path to battery test data file
        """
        logger.debug(f'Load file path: {file_path}')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Unable to load file {file_path}')
        
        # Clear previous data before parsing new data
        self.clear()
        
        # Get measurement name
        self.test_name = self.__get_test_name(file_path)

        # Determine test type
        self.test_type = self.__determine_test_type(file_path)
        
        # Parse metadata from test name
        self.parse_metadata(self.test_name, self.test_type)

        # Parse data based on test type
        self.parse_functions[self.test_type](file_path)

    def parse_arbin(self, file_path: str) -> None:
        """
        Parse Arbin test data.

        Parameters
        ----------
        file_path : str
            Path to Arbin test data file
        """
        # TODO: Implement Arbin test data parsing
        pass

    def parse_biologic(self, file_path: str) -> None:
        """
        Parse BioLogic test data.

        Parameters
        ----------
        file_path : str
            Path to BioLogic test data file
        """
 
        biologic_raw_df, start_time = self.__load_mpr(file_path)
        
        # Add the timestamp column
        total_time = pd.to_timedelta(biologic_raw_df['time/s'])
        biologic_raw_df[Const.TIMESTAMP] = start_time + total_time

        self.raw_test_data = biologic_raw_df
        

    def parse_neware(self, file_path: str) -> None:
        """
        Parse Neware test data.

        Parameters
        ----------
        file_path : str
            Path to Neware test data file
        """
        neware_raw_df = self.__load_xlsx(file_path)

        # Add the timestamp for the neware data
        start_time = pd.to_datetime(neware_raw_df['Date'][0])
        total_time = pd.to_timedelta(neware_raw_df['Total Time'])
        neware_raw_df[Const.TIMESTAMP] = start_time + total_time
        neware_raw_df.drop(columns=['t1(℃)'], inplace=True)
        
        # Store raw test data
        self.raw_test_data = neware_raw_df

    def parse_vdf(self, file_path: str) -> None:
        """
        Parse Neware Vdf test data.

        Parameters
        ----------
        file_path : str
            Path to Neware Vdf test data file
        """
        vdf_df, vdf_meta = self.__load_vdf_csv(file_path)

        # Store raw test data
        self.raw_test_data = vdf_df
        # Store raw metadata
        self.raw_metadata.update(vdf_meta)

    def parse_metadata(self, test_name: str, test_type: str) -> None:
        """
        Parse metadata from battery test name and type.
        Supported test types: 'Arbin', 'BioLogic', 'Neware', 'Vdf'
        The name of the test should follow the name rules of the test type.

        Parameters
        ----------
        test_name : str
            Name of the battery test
        test_type : str
            Type of battery test. Supported types: 'Arbin', 'BioLogic', 'Neware', 'Vdf'

        Raises
        ------
        ValueError
            If the test name does not match the name rules of the test type
        """
        keys = getattr(Const, f'{test_type.upper()}_NAME_KEYS')
        # Split the test name by '_' and match the keys
        try:
            values = test_name.split('_')
            self.raw_metadata.update(dict(zip(keys, values)))
        except:
            raise ValueError(f'Test name {test_name} does not match the name rules of {test_type}')
        
    def __get_test_name(self, file_path: str) -> str:
        """
        Get measurement name from file path.

        Parameters
        ----------
        file_path : str
            Path to battery test data file

        Returns
        -------
        str
            Measurement name
        """
        logger.debug(f'Get measurement name from file path: {file_path}')
        measurement_name = None

        # Get measurement name from file path
        file_name = os.path.basename(file_path)
        measurement_name = re.sub(r'\..*$', '', file_name)
        logger.debug(f'Measurement name: {measurement_name}')

        return measurement_name

    def __determine_test_type(self, file_path: str) -> str:
        """
        Determine test type from file path.

        Parameters
        ----------
        file_path : str
            Path to battery test data file

        Returns
        -------
        str
            Test type
        """
        logger.debug(f'Determine test type from file path: {file_path}')
        test_type = None

        # Determine test type from file path
        file_type = file_path.split(".")[-1]

        if file_type in Const.FILE_TYPE_2_TEST_TYPE:
            test_type = Const.FILE_TYPE_2_TEST_TYPE[file_type]
            logger.debug(f'Test type: {test_type}')
        else:
            raise ValueError(f'Unsupported file type: {file_type}')
        
        return test_type
    
    def __load_xlsx(self, file_path: str, sheet: str = 'record') -> pd.DataFrame:
        """
        Read the xlsx file, get the sheet and return the raw data

        Parameters
        ----------
        file_path : str
            The path to the xlsx file

        sheet : str (default: 'record')
            The sheet name to read 
            
        Returns
        -------
        raw_data : pandas.DataFrame
            The raw data
        """
        try:
            # Read the xlsx file
            xlsx = pd.ExcelFile(file_path)
            # Get the 'record' sheet
            raw_data = pd.read_excel(xlsx, sheet_name=sheet)
            logger.info(f"Loaded xlsx file from {file_path} successfully")
            
            return raw_data

        except:
            raise ValueError(f"Failed to load xlsx file from {file_path}")
        
    def __load_vdf_csv(self, file_path: str) -> pd.DataFrame:
        """
        Read the vdf csv file and return the raw data

        Parameters
        ----------
        file_path : str
            The path to the vdf csv file
            
        Returns
        -------
        vdf_df : pandas.DataFrame
            The raw data of the vdf csv file

        metadata : dict
            The metadata inside the vdf csv file
        """
        vdf_meta = {}
        start_line = None

        try:
            # Open the file once and parse it line by line
            with open(file_path, 'r') as file:
                for i, line in enumerate(file):
                    if "[DATA START]" in line:
                        start_line = i + 1  # Adjust for 0-based index
                        break  # Exit loop once the data start marker is found
                    elif ':' in line:
                        key, value = line.split(':', 1)  # Split on the first colon only
                        vdf_meta[key.strip()] = value.strip()
        except:
            raise ValueError(f"Failed to read vdf meta data from {file_path}")

        # Check if the data start marker was not found
        if start_line is None:
            raise ValueError(f"Failed to find data start marker in vdf csv file {file_path}")

        try:
        # Read the DataFrame, assuming the first row of data contains units
            df_units = pd.read_csv(file_path, delimiter='\t', skiprows=start_line, nrows=1)
            header = df_units.columns
            units = df_units.iloc[0].values

            # New header with units if available
            new_header = [f"{header[i]} ({units[i]})" if units[i] != 'none' else header[i] for i in range(len(header))]

            # Read the actual data, skipping the units row
            vdf_df = pd.read_csv(file_path, delimiter='\t', skiprows=start_line + 2, header=None, names=new_header)

            logger.info(f"Loaded vdf csv file from {file_path} successfully")
        except:
            raise ValueError(f"Failed to read vdf data from {file_path}")
        
        return vdf_df, vdf_meta

    def __load_mpr(self, file_path: str) -> pd.DataFrame:
        """
        Read the mpr file of Biologic, get the data and return the dataframe

        Parameters
        ----------
        file_path : str
            The path to the mpr file

        Returns
        -------
        df : pandas.DataFrame
            The dataframe
        start_timestamp : datetime.datetime
            The start timestamp
        """
        try:
            # Read the mpr file
            mpr_file = BioLogic.MPRfile(file_path)
            # Get the start time
            start_time = mpr_file.timestamp
            df = pd.DataFrame(mpr_file.data)
            logger.info(f"Loaded mpr file from {file_path} successfully")

            return df, start_time
        
        except Exception:
            raise ValueError(f"Failed to load mpr file from {file_path}")
        

    def clear(self) -> None:
        """
        Clear the previous data.
        """
        self.test_name = None
        self.test_type = None
        self.raw_test_data = pd.DataFrame(dtype=object)
        self.raw_metadata = {}