import pandas as pd 
import numpy as np

from scipy import integrate, interpolate
from scipy.signal import find_peaks, medfilt, savgol_filter
from scipy.optimize import Bounds, NonlinearConstraint, minimizev
from itertools import compress

from batteryabn import logger, Utils 
from batteryabn import Constants as Const
from batteryabn.models import TestRecord


class Processor:

    def __init__(self) -> None:
        """
        A class to process battery test data.
        """
        self.cell_data = pd.DataFrame(dtype=object)
        self.cell_cycle_metrics = pd.DataFrame(dtype=object)
        self.cell_data_vdf = pd.DataFrame(dtype=object)
        self.update = False

    def set_processed_data(self, data: pd.DataFrame = None, 
                           cycle_metrics: pd.DataFrame = None, data_vdf: pd.DataFrame =None) -> None:
        """
        Set processed battery test data.

        Parameters
        ----------
        data : pd.DataFrame, optional
            Processed battery test data

        cycle_metrics : pd.DataFrame, optional
            Processed battery test cycle metrics
        
        data_vdf : pd.DataFrame, optional
            Processed battery test voltage data
        """
        self.cell_data = data
        self.cell_cycle_metrics = cycle_metrics
        self.cell_data_vdf = data_vdf

    def process(self, cycler_trs: list[TestRecord], vdf_trs: list[TestRecord] = None, project: str = None):
        """
        Process battery test data.

        Parameters
        ----------
        cycler_trs : list[TestRecord]
            List of TestRecord objects for cycler data

        vdf_trs : list[TestRecord], optional
            List of TestRecord objects for voltage data
        """

        # Process cycler data
        cell_data, cell_cycle_metrics = self.process_cycler_data(cycler_trs, project)

        cell_data_vdf, cell_cycle_metrics = self.process_cycler_expansion(vdf_trs, cell_cycle_metrics, project)    

        # Rearrange columns of cell_cycle_metrics for easy reading with data on left and others on right
        cols = cell_cycle_metrics.columns.to_list()
        move_idx = [c for c in cols if '[' in c] + [c for c in cols if '[' not in c] 
        cell_cycle_metrics = cell_cycle_metrics[move_idx]

        self.set_processed_data(cell_data, cell_cycle_metrics, cell_data_vdf)

#-----------------Cycler Expansion Processing-----------------#

    def process_cycler_expansion(self, trs: list[TestRecord], cell_cycle_metrics: pd.DataFrame, project: str):
        """
        Process cycler expansion data.

        Parameters
        ----------
        trs : list[TestRecord]
            List of TestRecord objects
        cell_cycle_metrics : pd.DataFrame
            Cycler cycle metrics
        project : str
            Project name

        Returns
        -------
        pd.DataFrame
            Processed cycler expansion data
        pd.DataFrame
            Processed cycler cycle metrics
        """
        cell_data_vdf = self.combine_cycler_expansion_data(trs, project)

        # Find matching cycle timestamps from cycler data
        t_vdf, exp_vdf, exp_vdf_um = (cell_data_vdf[key] for key in [Const.TIME, Const.EXPANSION, Const.EXPANSION_UM])
        cycle_timestamps = cell_cycle_metrics[Const.TIME][cell_cycle_metrics[Const.CYCLE_IDC]]
        t_cycle_vdf, cycle_idx_vdf, matched_timestamp_idx = self.find_matching_timestamp(cycle_timestamps, t_vdf)  

        # Add cycle indicator, align with cycles timestamps previously defined by cycler data
        Utils.add_column(cell_data_vdf, Const.CYCLE_IDC, False)
        Utils.set_value(cell_data_vdf, Const.CYCLE_IDC, cycle_idx_vdf, True)

        # Add additional columns to cell_cycle_metrics
        for column in Const.CCM_COLUMNS_ADDITIONAL_VDF:
            Utils.add_column(cell_cycle_metrics, column, np.nan) 

        # Find min/max expansion and reversible expansion
        cycle_idx_vdf_minmax = [i for i in cycle_idx_vdf if i is not np.nan]
        cycle_idx_vdf_minmax.append(len(t_vdf) - 1) #append end
        exp_max, exp_min = self.max_min_cycle_data(exp_vdf, cycle_idx_vdf_minmax)
        exp_rev = np.subtract(exp_max, exp_min)
        exp_max_um, exp_min_um = self.max_min_cycle_data(exp_vdf_um, cycle_idx_vdf_minmax)
        exp_rev_um = np.subtract(exp_max_um, exp_min_um)
        discharge_cycle_idx = list(np.where(cell_cycle_metrics[Const.CYCLE_IDC])[0])

        # Put the calculated values into the cell_cycle_metrics dataframe
        for i, j in enumerate(matched_timestamp_idx):
            index = discharge_cycle_idx[j]
            cell_cycle_metrics.loc[index, Const.TIME_VDF] = t_cycle_vdf[i]
            cell_cycle_metrics.loc[index, Const.MIN_CYCLE_EXPANSION] = exp_min[i]
            cell_cycle_metrics.loc[index, Const.MAX_CYCLE_EXPANSION] = exp_max[i]
            cell_cycle_metrics.loc[index, Const.REV_CYCLE_EXPANSION] = exp_rev[i]
            cell_cycle_metrics.loc[index, Const.MIN_CYCLE_EXPANSION_UM] = exp_min_um[i]
            cell_cycle_metrics.loc[index, Const.MAX_CYCLE_EXPANSION_UM] = exp_max_um[i]
            cell_cycle_metrics.loc[index, Const.REV_CYCLE_EXPANSION_UM] = exp_rev_um[i]
            cell_cycle_metrics.loc[index, Const.DRIVE_CURRENT] = cell_data_vdf.get(Const.DRIVE_CURRENT, [0])[i] if Const.DRIVE_CURRENT in cell_data_vdf else 0
            cell_cycle_metrics.loc[index, Const.EXPANSION_STDDEV] = cell_data_vdf.get(Const.EXPANSION_STDDEV, [0])[i] if Const.EXPANSION_STDDEV in cell_data_vdf else 0
            cell_cycle_metrics.loc[index, Const.REF_STDDEV] = cell_data_vdf.get(Const.REF_STDDEV, [0])[i] if Const.REF_STDDEV in cell_data_vdf else 0

        # Add timestamps for charge cycles
        charge_cycle_idx = list(np.where(cell_cycle_metrics[Const.CHARGE_CYCLE_IDC])[0])
        charge_cycle_timestamps = cell_cycle_metrics[Const.TIME][cell_cycle_metrics[Const.CHARGE_CYCLE_IDC]]
        t_charge_cycle_vdf, _, matched_charge_timestamp_idx = self.find_matching_timestamp(charge_cycle_timestamps, t_vdf)
        for i, j in enumerate(matched_charge_timestamp_idx):
            cell_cycle_metrics.loc[charge_cycle_idx[j], Const.TIME_VDF] = t_charge_cycle_vdf[i]

        return cell_data_vdf, cell_cycle_metrics        

    def combine_cycler_expansion_data(self, trs: list[TestRecord], project: str):
        """
        Combine cycler expansion data from multiple files into a single dataframe.
        It will calculate the min, max, and reversible expansion for each cycle. 

        Parameters
        ----------
        trs : list[TestRecord]
            List of TestRecord objects
        project : str
            Project name

        Returns
        -------
        pd.DataFrame
            Combined cycler expansion data
        """
        dfs = []
        for tr in trs:
            dfs.append(self.process_cycler_expansion_tr(tr))
        logger.info(f"Combining {len(dfs)} dataframes")

        if len(dfs) == 0:
            logger.debug("No cycler expansion data found")
            return self.create_default_cell_data_vdf()
        
        cell_data_vdf = pd.concat(dfs, ignore_index=True).sort_values(by=Const.TIME)

        return cell_data_vdf
    
    def process_cycler_expansion_tr(self, tr: TestRecord):
        """
        Process and format cycler expansion data for a single test record.

        Parameters
        ----------
        tr : TestRecord
            TestRecord object

        Returns
        -------
        pd.DataFrame
            Processed cycler expansion data
        """
        logger.debug(f"Processing cycler expansion data for {tr.test_name}")
        df = tr.get_test_data()
        df = df[(df[Const.EXPANSION] >1e1) & (df[Const.EXPANSION] <1e7)] #keep good signals 

        x1, x2, c = self.get_calibration_parameters(tr)
        df[Const.EXPANSION_UM] = 1000 * (30.6 - (x2 * (df[Const.EXPANSION] / 10**6)**2 + x1 * (df[Const.EXPANSION] / 10**6) + c))
        df[Const.TEMPERATURE] = np.where((df[Const.TEMPERATURE] >= 200) & (df[Const.TEMPERATURE] <250), np.nan, df[Const.TEMPERATURE]) 

        return df

    def get_calibration_parameters(self, tr: TestRecord):
        # TODO: This method should be placed in the other file
        # It should load the calibration parameters from the database or yaml file
        # 
        pass

    def find_matching_timestamp(self, desired_timestamps, t, t_match_threshold = 10000):
        pass

    def create_default_cell_data_vdf(self):
        pass



#-----------------Cycler Data Processing-----------------#

    def process_cycler_data(self, trs: list[TestRecord], project: str):
        """
        Process cycler data.

        Parameters
        ----------
        trs : list[TestRecord]
            List of TestRecord objects
        project : str
            Project name

        Returns
        -------
        pd.DataFrame
            Processed cycler data
        pd.DataFrame
            Processed cycler cycle metrics
        """
        cell_data, cell_cycle_metrics = self.combine_cycler_data(trs)

        #TODO: Put project settings in json file and change this load method
        if project is None or project not in Const.PROJECTS_SETTING.keys():
            project = 'DEFAULT'
        qmax = Const.PROJECTS_SETTING[project]['Qmax']

        charge_t_idx = list(cell_data[cell_data[Const.CHARGE_CYCLE_IDC]].index)
        discharge_t_idx = list(cell_data[cell_data[Const.DISCHARGE_CYCLE_IDC]].index)
        q_c, q_d = self.calc_capacities(cell_data[Const.TIME], cell_data[Const.CURRENT], cell_data[Const.AHT], charge_t_idx, discharge_t_idx, qmax)
        i_avg_c, i_avg_d = self.avg_cycle_data_x(cell_data[Const.TIME], cell_data[Const.CURRENT], charge_t_idx, discharge_t_idx)
        
        # Find min/max metrics
        cycle_idx_minmax = list(cell_data[cell_data[Const.CYCLE_IDC]].index)
        cycle_idx_minmax.append(len(cell_data)-1)
        v_max, v_min = self.max_min_cycle_data(cell_data[Const.VOLTAGE], cycle_idx_minmax)
        temp_max, temp_min = self.max_min_cycle_data(cell_data[Const.TEMPERATURE], cycle_idx_minmax)

        # Add additional columns to cell_cycle_metrics
        for column in Const.CCM_COLUMNS_ADDITIONAL:
            Utils.add_column(cell_cycle_metrics, column, np.nan)

        # Put the calculated values into the cell_cycle_metrics dataframe
        charge_cycle_idx = list(cell_cycle_metrics[cell_cycle_metrics[Const.CHARGE_CYCLE_IDC]].index)
        discharge_cycle_idx = list(cell_cycle_metrics[cell_cycle_metrics[Const.DISCHARGE_CYCLE_IDC]].index) 
        cycle_idx = list(cell_cycle_metrics[cell_cycle_metrics[Const.CYCLE_IDC]].index) # align with charge start
        for i,j in enumerate(charge_cycle_idx): 
            cell_cycle_metrics.loc[j, Const.CHARGE_CAPACITY] = q_c[i]
            cell_cycle_metrics.loc[j, Const.AVG_CYCLE_CHARGE_CURRENT] = i_avg_c[i]  
        for i,j in enumerate(discharge_cycle_idx): 
            cell_cycle_metrics.loc[j, Const.DISCHARGE_CAPACITY] = q_d[i]
            cell_cycle_metrics.loc[j, Const.AVG_CYCLE_DISCHARGE_CURRENT] = i_avg_d[i]  
        for i,j in enumerate(cycle_idx): 
            cell_cycle_metrics.loc[j, Const.MIN_CYCLE_VOLTAGE] = v_min[i] 
            cell_cycle_metrics.loc[j, Const.MAX_CYCLE_VOLTAGE] = v_max[i] 
            cell_cycle_metrics.loc[j, Const.MIN_CYCLE_TEMP] = temp_min[i] 
            cell_cycle_metrics.loc[j, Const.MAX_CYCLE_TEMP] = temp_max[i] 

        return cell_data, cell_cycle_metrics

    def combine_cycler_data(self, trs: list[TestRecord]):
        """
        Combine cycler data from multiple files into a single dataframe.
        Concatenate data frames, identify cycles based on rests (I=0), then calculate min and max voltage and temperature for each cycle.

        Parameters
        ----------
        trs : list[TestRecord]
            List of TestRecord objects

        Returns
        -------
        pd.DataFrame
            Combined cycler data
        pd.DataFrame
            Cycler cycle metrics
        """
        dfs =[]
        for tr in trs:
            dfs.append(self.process_cycle_tr(tr))
        logger.info(f"Combining {len(dfs)} dataframes")
        cell_data = pd.concat(dfs, ignore_index=True)

        discharge_start_idx_0 = np.where(cell_data[Const.DISCHARGE_CYCLE_IDC])[0]
        charge_start_idx_0 = np.where(cell_data[Const.CHARGE_CYCLE_IDC])[0]
        capacity_check_idx_0 = np.where(cell_data[Const.CAPACITY_CHECK_IDC])[0]
        if len(discharge_start_idx_0) > 1 and len(charge_start_idx_0) > 1:
            charge_start_idx, discharge_start_idx = self.match_charge_discharge(charge_start_idx_0, discharge_start_idx_0)
            removed_charge_cycle_idx = list(set(charge_start_idx_0).symmetric_difference(set(charge_start_idx)))
            cell_data.loc[removed_charge_cycle_idx, Const.CAPACITY_CHECK_IDC] = False
            removed_discharge_cycle_idx = list(set(discharge_start_idx_0).symmetric_difference(set(discharge_start_idx)))
            cell_data.loc[removed_discharge_cycle_idx, Const.DISCHARGE_CYCLE_IDC] = False
            removed_capacity_check_idx = list(set(capacity_check_idx_0).symmetric_difference(set(charge_start_idx)))
            cell_data.loc[removed_capacity_check_idx, Const.CAPACITY_CHECK_IDC] = False

        cell_data[Const.CYCLE_IDC] = cell_data[Const.CHARGE_CYCLE_IDC] #default cycle indicator on charge

        # Save cycle metrics to separate dataframe and sort. Only keep columns where charge and discharge cycles start. Label the type of protocol
        cell_cycle_metrics = cell_data[Const.CCM_COLUMNS][(cell_data[Const.CHARGE_CYCLE_IDC]) | (cell_data[Const.DISCHARGE_CYCLE_IDC])].copy()
        cell_cycle_metrics.reset_index(drop=True, inplace=True)
        logger.info(f"Found {len(cell_data)} cell data, {len(cell_cycle_metrics)} cycles")

        return cell_data, cell_cycle_metrics
            
    def process_cycle_tr(self, tr: TestRecord):
        """
        Process and format cycle data for a single test record.

        Parameters
        ----------
        tr : TestRecord
            TestRecord object

        Returns
        -------
        pd.DataFrame
            Formatted cycle data
        """
        logger.debug(f"Processing cycle data for {tr.test_name}")
        df = tr.get_test_data()
    
        # Get the data
        t = df[Const.TIME].reset_index(drop=True)
        i = df[Const.CURRENT].reset_index(drop=True)
        protocal = tr.get_cycle_type()
        lims = Const.CYCLE_ID_LIMS[protocal]

        # These parameters could be used to filter cycle index in the future
        v = df[Const.VOLTAGE].reset_index(drop=True)
        step_idx = df[Const.STEP_IDX].reset_index(drop=True)
        cycle_idx = df[Const.CYCLE_IDX].reset_index(drop=True)
        v_max_cycle, v_min_cycle, dah_min, dt_min = (
            lims[key] for key in (
                Const.V_MAX_CYCLE, 
                Const.V_MIN_CYCLE, 
                Const.DAH_MIN, 
                Const.DT_MIN
            )
        )

        charge_start_idx, discharge_start_idx = self.find_cycle_idx(t, i)
        try: # won't work for half cycles (files with only charge or only discharge)
            charge_start_idx, discharge_start_idx = self.match_charge_discharge(charge_start_idx, discharge_start_idx)
        except:
            logger.error(f"Error processing {tr.test_name}: failed to match charge discharge")
            pass

        # Add aux cycle indicators to df. Column of True if start of a cycle, otherwise False. 
        # Set default cycle indicator = charge start 
        for indicator in Const.INDICATORS:
            Utils.add_column(df, indicator, False)
        Utils.set_value(df, Const.CHARGE_CYCLE_IDC, charge_start_idx, True)
        Utils.set_value(df, Const.DISCHARGE_CYCLE_IDC, discharge_start_idx, True)
        #TODO: test_data['cycle_indicator'] = test_data['charge_cycle_indicator']
        #TODO: is_rpt() and is_format() are not implemented
        is_cap_check = tr.is_rpt() or tr.is_format()
        if is_cap_check:
            Utils.set_value(df, Const.CAPACITY_CHECK_IDC, charge_start_idx, True)

        # Add cycle type and test name to df
        Utils.add_column(df, Const.CYCLE_TYPE, ' ')
        Utils.add_column(df, Const.TEST_NAME, ' ')
        
        Utils.set_value(df, Const.CYCLE_TYPE, np.concatenate((discharge_start_idx,charge_start_idx)), protocal)
        Utils.set_value(df, Const.TEST_NAME, np.concatenate((discharge_start_idx,charge_start_idx)), tr.test_name)

        # Identify subcycle type. For extracting HPPC and C/20 dis/charge data later. 
        Utils.add_column(df, Const.PROTOCOL, np.nan)

        # Get the cycle metrics
        cycle_metrics = df[(df[Const.CHARGE_CYCLE_IDC]) | (df[Const.DISCHARGE_CYCLE_IDC])]

        for i in range(0, len(cycle_metrics)):
            t_start = cycle_metrics[Const.TIME].iloc[i]
            if i == len(cycle_metrics) - 1: # if last subcycle, end of subcycle = end of file 
                t_end = df[Const.TIME].iloc[-1]
            else: # end of subcycle = start of next subcycle
                t_end = cycle_metrics[Const.TIME].iloc[i+1]
            i_subcycle = df[Const.CURRENT][(t > t_start) & (t < t_end)]
            data_idx = cycle_metrics.index.tolist()[i]
            if is_cap_check:
                # hppc: ID by # of types of current sign changes (threshold is arbitrary)
                if len(np.where(np.diff(np.sign(i_subcycle)))[0]) > 10:
                    df.loc[data_idx, Const.PROTOCOL] = 'HPPC'
                # C/20 charge: longer than 8 hrs and mean(I)>0. Will ID C/10 during formation as C/20...
                elif (t_end - t_start) / 3600.0 > 8 and np.mean(i_subcycle) > 0 and np.mean(i_subcycle) < Const.QMAX / 18:
                    df.loc[data_idx, Const.PROTOCOL] = 'C/20 charge'
                # C/20 discharge: longer than 8 hrs and mean(I)<0. Will ID C/10 during formation as C/20...
                elif (t_end - t_start) / 3600.0 > 8 and np.mean(i_subcycle) < 0 and np.mean(i_subcycle) > - Const.QMAX / 18:
                    df.loc[data_idx, Const.PROTOCOL] = 'C/20 discharge'
            
        return df


    def find_cycle_idx(self, t: pd.Series, i: pd.Series):
        """
        Find the cycle charge and discharge indices

        Parameters
        ----------
        t: pd.Series
            Time data
        i: pd.Series
            Current data
        """
        pass

    def match_charge_discharge(self, charge_start_idx: np.array, discharge_start_idx: np.array):
        pass

    def calc_capacities(self, t, i, aht, charge_idx, discharge_idx, qmax):
        pass

    def avg_cycle_data_x(self, t, data, charge_idx, discharge_idx):
        pass

    def max_min_cycle_data(self, data, cycle_idx_minmax):
        pass