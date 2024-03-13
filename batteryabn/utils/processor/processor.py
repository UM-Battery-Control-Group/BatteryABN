import pandas as pd 
import numpy as np
import rfcnt

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
        move_idxs = [c for c in cols if '[' in c] + [c for c in cols if '[' not in c] 
        cell_cycle_metrics = cell_cycle_metrics[move_idxs]

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
        t_cycle_vdf, cycle_vdf_idxs, matched_timestamp_idxs = self.find_matching_timestamp(cycle_timestamps, t_vdf)  

        # Add cycle indicator, align with cycles timestamps previously defined by cycler data
        Utils.add_column(cell_data_vdf, Const.CYCLE_IDC, False)
        Utils.set_value(cell_data_vdf, Const.CYCLE_IDC, cycle_vdf_idxs, True)

        # Add additional columns to cell_cycle_metrics
        for column in Const.CCM_COLUMNS_ADDITIONAL_VDF:
            Utils.add_column(cell_cycle_metrics, column, np.nan) 

        # Find min/max expansion and reversible expansion
        cycle_vdf_minmax_idxs = [i for i in cycle_vdf_idxs if i is not np.nan]
        cycle_vdf_minmax_idxs.append(len(t_vdf) - 1) #append end
        exp_max, exp_min = self.max_min_cycle_data(exp_vdf, cycle_vdf_minmax_idxs)
        exp_rev = np.subtract(exp_max, exp_min)
        exp_max_um, exp_min_um = self.max_min_cycle_data(exp_vdf_um, cycle_vdf_minmax_idxs)
        exp_rev_um = np.subtract(exp_max_um, exp_min_um)
        discharge_cycle_idxs = list(np.where(cell_cycle_metrics[Const.CYCLE_IDC])[0])

        # Put the calculated values into the cell_cycle_metrics dataframe
        for i, j in enumerate(matched_timestamp_idxs):
            index = discharge_cycle_idxs[j]
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
        charge_cycle_idxs = list(np.where(cell_cycle_metrics[Const.CHARGE_CYCLE_IDC])[0])
        charge_cycle_timestamps = cell_cycle_metrics[Const.TIME][cell_cycle_metrics[Const.CHARGE_CYCLE_IDC]]
        t_charge_cycle_vdf, _, matched_charge_timestamp_idx = self.find_matching_timestamp(charge_cycle_timestamps, t_vdf)
        for i, j in enumerate(matched_charge_timestamp_idx):
            cell_cycle_metrics.loc[charge_cycle_idxs[j], Const.TIME_VDF] = t_charge_cycle_vdf[i]

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
            return pd.DataFrame(columns = Const.VDF_COLUMNS)
        
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

        x1, x2, c = tr.get_calibration_parameters()
        df[Const.EXPANSION_UM] = 1000 * (30.6 - (x2 * (df[Const.EXPANSION] / 10**6)**2 + x1 * (df[Const.EXPANSION] / 10**6) + c))
        df[Const.TEMPERATURE] = np.where((df[Const.TEMPERATURE] >= 200) & (df[Const.TEMPERATURE] <250), np.nan, df[Const.TEMPERATURE]) 

        return df


    def find_matching_timestamp(self, desired_timestamps, time_series: pd.Series, t_threshold: int = 10000):
        """
        Find the matching timestamps 

        Parameters
        ----------
        desired_timestamps : pd.Series
            Desired timestamps
        time_series : pd.Series
            Time series
        t_threshold : int, optional
            Timestamp threshold

        Returns
        -------
        pd.Series   
            Matched timestamps
        np.ndarray
            Matched indices
        np.ndarray
            Desired timestamp indices
        """
        # Remove duplicates from time_data and create a new series with unique timestamps as index
        unique_time_data = time_series.drop_duplicates().reset_index(drop=True)
        unique_time_data.index = unique_time_data.values

        # Find the indices of the closest match in unique_time_data for each desired timestamp
        desired_timestamp_idxs = np.argwhere(unique_time_data.index.get_indexer(
            desired_timestamps, method="nearest", tolerance=t_threshold * 1000) != -1)[:, 0]
        matched_indices_in_unique = unique_time_data.index.get_indexer(
            desired_timestamps, method="nearest", tolerance=t_threshold * 1000)
        matched_indices_in_unique = matched_indices_in_unique[matched_indices_in_unique != -1]

        # Get the actual matched timestamps and their indices in the original time_data
        matched_timestamps = unique_time_data.iloc[matched_indices_in_unique].index
        matched_idxs = time_series.index.get_indexer_for(matched_timestamps)

        return matched_timestamps, matched_idxs, desired_timestamp_idxs


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

        charge_t_idxs = list(cell_data[cell_data[Const.CHARGE_CYCLE_IDC]].index)
        discharge_t_idxs = list(cell_data[cell_data[Const.DISCHARGE_CYCLE_IDC]].index)
        q_c, q_d = self.calc_capacities(cell_data[Const.TIME], cell_data[Const.AHT], charge_t_idxs, discharge_t_idxs, qmax)
        i_avg_c, i_avg_d = self.calc_avg_cycle_data(cell_data[Const.TIME], cell_data[Const.CURRENT], charge_t_idxs, discharge_t_idxs)
        
        # Find min/max metrics
        cycle_minmax_idxs = list(cell_data[cell_data[Const.CYCLE_IDC]].index)
        cycle_minmax_idxs.append(len(cell_data)-1)
        v_max, v_min = self.max_min_cycle_data(cell_data[Const.VOLTAGE], cycle_minmax_idxs)
        temp_max, temp_min = self.max_min_cycle_data(cell_data[Const.TEMPERATURE], cycle_minmax_idxs)

        # Add additional columns to cell_cycle_metrics
        for column in Const.CCM_COLUMNS_ADDITIONAL:
            Utils.add_column(cell_cycle_metrics, column, np.nan)

        # Put the calculated values into the cell_cycle_metrics dataframe
        charge_cycle_idxs = list(cell_cycle_metrics[cell_cycle_metrics[Const.CHARGE_CYCLE_IDC]].index)
        discharge_cycle_idxs = list(cell_cycle_metrics[cell_cycle_metrics[Const.DISCHARGE_CYCLE_IDC]].index) 
        cycle_idxs = list(cell_cycle_metrics[cell_cycle_metrics[Const.CYCLE_IDC]].index) # align with charge start
        for i,j in enumerate(charge_cycle_idxs): 
            cell_cycle_metrics.loc[j, Const.CHARGE_CAPACITY] = q_c[i]
            cell_cycle_metrics.loc[j, Const.AVG_CYCLE_CHARGE_CURRENT] = i_avg_c[i]  
        for i,j in enumerate(discharge_cycle_idxs): 
            cell_cycle_metrics.loc[j, Const.DISCHARGE_CAPACITY] = q_d[i]
            cell_cycle_metrics.loc[j, Const.AVG_CYCLE_DISCHARGE_CURRENT] = i_avg_d[i]  
        for i,j in enumerate(cycle_idxs): 
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

        discharge_start_idxs_0 = np.where(cell_data[Const.DISCHARGE_CYCLE_IDC])[0]
        charge_start_idxs_0 = np.where(cell_data[Const.CHARGE_CYCLE_IDC])[0]
        capacity_check_idxs_0 = np.where(cell_data[Const.CAPACITY_CHECK_IDC])[0]
        if len(discharge_start_idxs_0) > 1 and len(charge_start_idxs_0) > 1:
            charge_start_idx, discharge_start_idx = self.match_charge_discharge(charge_start_idxs_0, discharge_start_idxs_0)
            removed_charge_cycle_idx = list(set(charge_start_idxs_0).symmetric_difference(set(charge_start_idx)))
            cell_data.loc[removed_charge_cycle_idx, Const.CAPACITY_CHECK_IDC] = False
            removed_discharge_cycle_idx = list(set(discharge_start_idxs_0).symmetric_difference(set(discharge_start_idx)))
            cell_data.loc[removed_discharge_cycle_idx, Const.DISCHARGE_CYCLE_IDC] = False
            removed_capacity_check_idx = list(set(capacity_check_idxs_0).symmetric_difference(set(charge_start_idx)))
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
        step_idxs = df[Const.STEP_IDX].reset_index(drop=True)
        cycle_idxs = df[Const.CYCLE_IDX].reset_index(drop=True)
        v_max_cycle, v_min_cycle, dah_min, dt_min = (
            lims[key] for key in (
                Const.V_MAX_CYCLE, 
                Const.V_MIN_CYCLE, 
                Const.DAH_MIN, 
                Const.DT_MIN
            )
        )

        charge_start_idxs, discharge_start_idxs = self.find_cycle_idxs(t, i)
        try: # won't work for half cycles (files with only charge or only discharge)
            charge_start_idxs, discharge_start_idxs = self.match_charge_discharge(charge_start_idxs, discharge_start_idxs)
        except:
            logger.error(f"Error processing {tr.test_name}: failed to match charge discharge")
            pass

        # Add aux cycle indicators to df. Column of True if start of a cycle, otherwise False. 
        # Set default cycle indicator = charge start 
        for indicator in Const.INDICATORS:
            Utils.add_column(df, indicator, False)
        Utils.set_value(df, Const.CHARGE_CYCLE_IDC, charge_start_idxs, True)
        Utils.set_value(df, Const.DISCHARGE_CYCLE_IDC, discharge_start_idxs, True)
        #TODO: test_data['cycle_indicator'] = test_data['charge_cycle_indicator']
        #TODO: is_rpt() and is_format() are not implemented
        is_cap_check = tr.is_rpt() or tr.is_format()
        if is_cap_check:
            Utils.set_value(df, Const.CAPACITY_CHECK_IDC, charge_start_idxs, True)

        # Add cycle type and test name to df
        Utils.add_column(df, Const.CYCLE_TYPE, ' ')
        Utils.add_column(df, Const.TEST_NAME, ' ')
        
        Utils.set_value(df, Const.CYCLE_TYPE, np.concatenate((discharge_start_idxs,charge_start_idxs)), protocal)
        Utils.set_value(df, Const.TEST_NAME, np.concatenate((discharge_start_idxs,charge_start_idxs)), tr.test_name)

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


    def find_cycle_idxs(self, t: pd.Series, i: pd.Series):
        """
        Find the cycle charge and discharge indices

        Parameters
        ----------
        t: pd.Series
            Time data
        i: pd.Series
            Current data

        Returns
        -------
        charge_start_idx: np.ndarray
            Array of indices where charging cycles start
        discharge_start_idx: np.ndarray
            Array of indices where discharging cycles start
        """

        ic = (i.values > 1e-5).astype(int)
        Id = (i.values < -1e-5).astype(int)
        potential_charge_start_idxs = np.where(np.diff(ic) > 0.5)[0]
        potential_discharge_start_idxs = np.where(np.diff(Id) > 0.5)[0]
        dt = np.diff(t)

        # Cumah = Ah_Charge - Ah_Discharge
        cumah = integrate.cumtrapz(i, t, initial=0) / 3600 / 1000  # ms to hours
        # Calculate the average discharge current and average time until the next charge step
        cumah = cumah - cumah.min()
        # Check for large gaps in the data, and reset the cumah counter.
        gap_index = np.argwhere(dt > 1e6)  # Look for gaps greater than 1000 seconds

        if gap_index.size > 0:
            if gap_index[0][0] > 0:
                for gap in gap_index[0]:
                    cumah[(gap + 1):] = cumah[gap] + cumah[(gap + 1):] - cumah[gap + 1]

        class_count = 10  # Basically needs to change by more than 10% of the full range.
        class_range = cumah.ptp()
        class_width = class_range / (class_count - 1)
        class_offset = cumah.min() - class_width / 2

        try:
            res = rfcnt.rfc(
                cumah,
                class_count=class_count,
                class_offset=class_offset,
                class_width=class_width,
                hysteresis=class_width,
                spread_damage=rfcnt.SDMethod.FULL_P2,  # Assign damage for closed cycles to 2nd turning point
                residual_method=rfcnt.ResidualMethod._NO_FINALIZE,  # Don't consider residues and leave internal sequence open
                wl={"sd": 1e3, "nd": 1e7, "k": 5}
            )

            turning_points = res["tp"][:, 0].astype(int) - 1
            cum_ah_at_turn = res["tp"][:, 1]
            last_tp = 0

            if len(turning_points) > 2:
                if cum_ah_at_turn[1] > cum_ah_at_turn[0]:
                    # 2nd turning point is the start of discharge.
                    charge_start_idx = np.array([min(potential_charge_start_idxs, key=lambda x: abs(x - turning_points[0]))])
                    discharge_start_idx = np.array([min(potential_discharge_start_idxs, key=lambda x: abs(x - turning_points[1]))])
                    last_tp = 1

                elif cum_ah_at_turn[0] - class_offset > class_range / 2:
                    # The first turning point is likely the start of discharge.
                    charge_start_idx = np.array([0])  # Case of a partial cycle, so set the charge start to the start of the file.
                    if turning_points[0] > charge_start_idx[0] - 10:  # Check that it comes after the first charge
                        discharge_start_idx = np.array([min(potential_discharge_start_idxs, key=lambda x: abs(x - turning_points[0]))])
                        last_tp = 0
                    else:
                        discharge_start_idx = np.array([min(potential_discharge_start_idxs, key=lambda x: abs(x - turning_points[1]))])
                        last_tp = 1
                        logger.debug("Choosing next turning point caveat emptor.")

                else:
                    charge_start_idx = np.array([potential_charge_start_idxs[0]])
                    if turning_points[1] > charge_start_idx[0] - 100:
                        discharge_start_idx = np.array([min(potential_discharge_start_idxs, key=lambda x: abs(x - turning_points[1]))])
                        last_tp = 1

                # Need to add the else case here in case we don't start with a charge cycle.

                for i in range(last_tp + 1, len(turning_points) - 1, 2):
                    charge_start_idx = np.append(charge_start_idx, min(potential_charge_start_idxs, key=lambda x: abs(x - turning_points[i])))
                    discharge_start_idx = np.append(discharge_start_idx, min(potential_discharge_start_idxs, key=lambda x: abs(x - turning_points[i + 1])))

            else:
                # No turning points in the data, just take the extents? This will probably break something else...
                charge_start_idx = []
                discharge_start_idx = []

        except Exception:
            logger.warning("No cycles detected (using the whole test).")
            charge_start_idx = []
            discharge_start_idx = []

        return charge_start_idx, discharge_start_idx

    def match_charge_discharge(self, charge_start_idxs: np.array, discharge_start_idxs: np.array):
        """
        Match charge and discharge start idxs for cycles starting with charge 
        and followed by discharge, considering inputs are numpy arrays.

        Parameters
        ----------
        charge_start_idxs : numpy.array
            Array of charge start idxs.
        discharge_start_idxs : numpy.array
            Array of discharge start idxs.

        Returns
        -------
        numpy.array
            Array of matched charge start idxs.
        numpy.array
            Array of matched discharge start idxs.
        """
        # Ensure cycling starts with a charge by adjusting the discharge idxs if necessary
        if discharge_start_idxs[0] < charge_start_idxs[0]:
            discharge_start_idxs = discharge_start_idxs[1:]
        
        # Match cycles based on the shortest sequence
        min_length = min(len(charge_start_idxs), len(discharge_start_idxs))
        matched_charge_idxs = charge_start_idxs[:min_length]
        matched_discharge_idxs = discharge_start_idxs[:min_length]

        return matched_charge_idxs, matched_discharge_idxs
    

    def calc_capacities(self, time_series: pd.Series, aht: pd.Series, charge_idxs: list, discharge_idxs: list, qmax: int):
        """
        Calculate the charge and discharge capacities based on Ah throughput data.

        Parameters
        ----------
        time_series : pd.Series
            Time data
        aht : pd.Series
            Ah throughput data
        charge_idxs : list
            Indices of charge cycles
        discharge_idxs : list    
            Indices of discharge cycles
        qmax : int
            Maximum capacity

        Returns
        -------
        tuple of np.ndarray
            The charge and discharge capacities.
        """
        cycle_idxs = sorted(charge_idxs + discharge_idxs + [len(time_series) - 1])
        
        charge_capacities = []
        discharge_capacities = []

        for i in range(len(cycle_idxs) - 1):
            capacity = aht[cycle_idxs[i + 1]] - aht[cycle_idxs[i]]
            
            if capacity > qmax:
                capacity = np.nan
                logger.warning(f"Invalid Capacity for cycle {i}")
            
            if cycle_idxs[i] in charge_idxs:
                charge_capacities.append(capacity)
            else:
                discharge_capacities.append(capacity)
        
        return np.array(charge_capacities), np.array(discharge_capacities)

    def calc_avg_cycle_data(self, time_series: np.array, data: np.array, charge_idxs: list, discharge_idxs: list):
        """
        Calculate average data (e.g., voltage, temperature, or expansion) for each cycle.

        Parameters:
        time_series : numpy array
            Time data
        data : numpy array
            Data to calculate average
        charge_idxs : list
            Indices of charge cycles
        discharge_idxs : list
            Indices of discharge cycles

        Returns:
        numpy array
            Averages of charge cycles
        numpy array
            Averages of discharge cycles
        """
        # Combine and sort idxs to mark the start of each cycle, including the last data point
        cycle_starts = sorted(charge_idxs + discharge_idxs + [len(time_series) - 1])

        averages_charge = []
        averages_discharge = []
        
        # Calculate the average for each cycle
        for i in range(len(cycle_starts) - 1):
            start_idx, end_idx = cycle_starts[i], cycle_starts[i + 1]
            time_delta = time_series[end_idx] - time_series[start_idx]
            
            if time_delta > 0:
                cycle_data = data[start_idx:end_idx]
                cycle_time = time_series[start_idx:end_idx]
                average = np.trapz(cycle_data, cycle_time) / time_delta
            else:
                average = 0
            
            # Assign the calculated average to the corresponding list based on cycle type
            if start_idx in charge_idxs:
                averages_charge.append(average)
            else:
                averages_discharge.append(average)
        
        return np.array(averages_charge), np.array(averages_discharge)

    #-----------------Shared Methods-----------------#

    def max_min_cycle_data(self, data: pd.Series, cycle_idxs_minmax: list):
        """
        Calculate the min and max data for each cycle.
        e.g. voltage, temperature, or expansion

        Parameters
        ----------
        data : pd.Series
            Data to calculate min and max
        cycle_idxs_minmax : list
            Cycle idxs

        Returns
        -------
        list
            Max data for each cycle
        list
            Min data for each cycle
        """
        max_vals  = []
        min_vals  = []

        for i in range(len(cycle_idxs_minmax) - 1):
            # If there's cycle data between two consecutive points, calculate max and min
            if len(data[cycle_idxs_minmax[i]:cycle_idxs_minmax[i + 1]]) > 0:
                max_vals.append(max(data[cycle_idxs_minmax[i]:cycle_idxs_minmax[i+1]]))
                min_vals.append(min(data[cycle_idxs_minmax[i]:cycle_idxs_minmax[i+1]]))
            # Handling edge cases
            else: 
                max_vals.append(data[cycle_idxs_minmax[i]])   
                min_vals.append(data[cycle_idxs_minmax[i]])  

        return max_vals, min_vals