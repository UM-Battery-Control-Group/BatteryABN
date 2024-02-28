import pandas as pd

from batteryabn.Testrecord.Parser import Parser
from batteryabn.Testrecord.Formatter import Formatter

class Testrecord:
    def __init__(self):
        """
        A class for a single battery test record.
        """
        self.test_name = None
        self.test_type = None
        self.test_data = pd.DataFrame(dtype=object)
        self.cycler_data = pd.DataFrame(dtype=object)
        self.test_metadata = {}

    def parse(self, file_path: str):
        """
        Parse battery test data from file.

        Parameters
        ----------
        file_path : str
            Path to battery test data file

        Returns
        -------
        self : Testrecord
            Returns self for method chaining
        """
        self.clear()

        parser = Parser()
        parser.parse(file_path)
        self.test_name = parser.test_name
        self.test_type = parser.test_type
        self.test_data = parser.raw_test_data
        self.cycler_data = parser.raw_cycler_data
        self.test_metadata = parser.raw_metadata

        # Return self for method chaining
        return self
    
    def format(self, timezone: str = None):
        """
        Format battery test data.

        Parameters
        ----------
        timezone : str, optional
            Timezone to use for formatting

        Returns
        -------
        self : Testrecord
            Returns self for method chaining
        """
        formatter = Formatter(timezone)
        formatter.format_test_data(self.test_data, self.test_type)
        formatter.format_test_data(self.cycler_data, self.test_type, is_cycle=True)
        formatter.format_metadata(self.test_metadata)

        self.test_data = formatter.test_data
        self.cycler_data = formatter.cycler_data
        self.test_metadata = formatter.metadata

        return self
    
    def clear(self):
        """
        Clear test data and metadata.
        """
        self.test_name = None
        self.test_type = None
        self.test_data = pd.DataFrame(dtype=object)
        self.cycler_data = pd.DataFrame(dtype=object)
        self.test_metadata = {}