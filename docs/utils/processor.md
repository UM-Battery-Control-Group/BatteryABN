# Processor Module Documentation

This document provides an in-depth overview of the `Processor` class and its methods within the `processor.py` module. The module is designed to process battery test data by extracting cycler and VDF data, calculating cycle metrics, and generating meaningful summaries. It leverages libraries such as **pandas**, **numpy**, and **scipy** (as well as auxiliary libraries like `rfcnt`) to perform data manipulation, numerical integration, interpolation, optimization, and signal processing.

---

## Table of Contents

- [Overview](#overview)
- [Class: Processor](#class-processor)
  - [Attributes](#attributes)
  - [Initialization](#initialization)
- [Data Processing Workflow](#data-processing-workflow)
- [Method Details](#method-details)
  - [set_processed_data(data, cycle_metrics, data_vdf)](#set_processed_data)
  - [process(cycler_trs, vdf_trs, project)](#process)
- [Cycler Expansion Processing](#cycler-expansion-processing)
  - [process_cycler_expansion(trs, cell_cycle_metrics)](#process_cycler_expansion)
  - [combine_cycler_expansion_data(trs)](#combine_cycler_expansion_data)
  - [process_cycler_expansion_tr(tr)](#process_cycler_expansion_tr)
  - [find_matching_timestamp(desired_timestamps, time_series, t_threshold)](#find_matching_timestamp)
- [Cycler Data Processing](#cycler-data-processing)
  - [process_cycler_data(trs, project)](#process_cycler_data)
  - [combine_cycler_data(trs)](#combine_cycler_data)
  - [process_cycle_tr(tr, pre_aht)](#process_cycle_tr)
  - [find_cycle_idxs(t, i)](#find_cycle_idxs)
  - [match_charge_discharge(charge_start_idxs, discharge_start_idxs)](#match_charge_discharge)
  - [calc_capacities(time_series, aht, charge_idxs, discharge_idxs, qmax)](#calc_capacities)
  - [calc_avg_cycle_data(time_stamps, data, charge_idxs, discharge_idxs)](#calc_avg_cycle_data)
- [Shared Methods](#shared-methods)
  - [max_min_cycle_data(data, cycle_idxs_minmax)](#max_min_cycle_data)
- [RPT Data Processing and eSOH Estimation](#rpt-data-processing-and-esoh-estimation)
  - [summarize_rpt_data(project)](#summarize_rpt_data)
  - [update_cycle_metrics_hppc(rpt_subcycle, i)](#update_cycle_metrics_hppc)
  - [update_cycle_metrics_esoh(rpt_subcycle, pre_rpt_subcycle, i, i_slow)](#update_cycle_metrics_esoh)
  - [load_v_data(ch_rpt, dh_rpt, i_slow, i_threshold, d_int)](#load_v_data)
  - [esoh_est(q_data, v_data, dvdq_data, q_full, window)](#esoh_est)
  - [filter_qv_data(qdata, vdata, window_length, polyorder)](#filter_qv_data)
  - [get_rs_soc(t, i, v, q)](#get_rs_soc)
  - [fitfunc(x, q_data, v_data, dvdq_data, dvdq_bool)](#fitfunc)
  - [get_peaks(q, dvdq)](#get_peaks)
  - [calc_opc(x, q)](#calc_opc)
  - [sort_trs(trs)](#sort_trs)
- [Data Combination](#data-combination)
  - [combine_data(cell_data, cell_data_vdf)](#combine_data)

---

## Overview

The `Processor` module is responsible for processing battery test data by:
- Extracting and combining cycler and VDF data from multiple test records.
- Calculating cycle metrics such as capacities, average cycle data, voltage/temperature extremes, and expansion parameters.
- Aligning timestamps between different datasets.
- Generating comprehensive cycle metrics for further analysis and reporting.
- Estimating equivalent state-of-health (eSOH) parameters using optimization and curve-fitting techniques on voltage and differential voltage data.
- Combining processed data from the cycler and VDF sources.

---

## Class: Processor

### Attributes

- **cell_data**: A pandas DataFrame storing the processed battery test data.
- **cell_cycle_metrics**: A DataFrame containing calculated cycle metrics.
- **cell_data_vdf**: A DataFrame holding processed VDF data from cycler expansion.
- **cell_data_rpt**: A DataFrame reserved for RPT data.
- **update**: A boolean flag indicating whether the processor has been updated.

### Initialization

The `Processor` class is instantiated via the `create_processor()` function or directly using `Processor()`. It initializes its attributes with empty DataFrames and sets a flag for tracking updates.

---

## Data Processing Workflow

The primary workflow includes:
1. Setting processed data via `set_processed_data`.
2. Processing cycler data and VDF expansion data with the `process` method.
3. Combining data from multiple test records.
4. Calculating cycle metrics such as capacities, average current, voltage extremes, temperature extremes, and expansion values.
5. Summarizing RPT data and estimating eSOH using dedicated methods.
6. Combining processed cycler data and VDF data for final analysis.

---

## Method Details

### set_processed_data(data, cycle_metrics, data_vdf)

**Purpose:**  
Stores processed cycler data, cycle metrics, and VDF data into the class attributes.

**Parameters:**
- `cell_dat`: Processed battery test data (DataFrame).
- `cycle_metrics`: Processed cycle metrics (DataFrame).
- `data_vdf`: Processed cycler voltage (VDF) data (DataFrame).

---

### process(cycler_trs, vdf_trs, project)

**Purpose:**  
Processes battery test data by handling cycler data and, optionally, VDF data; then summarizes the report data based on a provided project.

**Parameters:**
- `cycler_trs`: Dictionary where keys are test names and values are lists of `TestRecord` objects for cycler data.
- `vdf_trs`: (Optional) Dictionary where keys are test names and values are lists of `TestRecord` objects for VDF data.
- `project`: (Optional) A `Project` object containing project-specific parameters.

**Workflow:**
1. Processes cycler data using `process_cycler_data`.
2. Processes cycler expansion data with `process_cycler_expansion`.
3. Rearranges cycle metric columns for better readability.
4. Sets the processed data with `set_processed_data`.
5. Summarizes RPT data via `summarize_rpt_data`.

---

## Cycler Expansion Processing

### process_cycler_expansion(trs, cell_cycle_metrics)

**Purpose:**  
Processes cycler expansion data from test records.

**Parameters:**
- `trs`: Dictionary of test records for cycler expansion.
- `cell_cycle_metrics`: DataFrame containing cycler cycle metrics.

**Workflow:**
1. Combines cycler expansion data using `combine_cycler_expansion_data`.
2. Finds matching timestamps between the expansion data and cycler cycle metrics using `find_matching_timestamp`.
3. Adds a cycle indicator column to the VDF data.
4. Computes minimum, maximum, and reversible expansion values.
5. Updates the `cell_cycle_metrics` DataFrame with the calculated values.

---

### combine_cycler_expansion_data(trs)

**Purpose:**  
Combines cycler expansion data from multiple files into a single DataFrame.

**Parameters:**
- `trs`: Dictionary of test records for expansion data.

**Returns:**  
A concatenated and sorted DataFrame of cycler expansion data.

---

### process_cycler_expansion_tr(tr)

**Purpose:**  
Processes and formats cycler expansion data for a single test record.

**Parameters:**
- `tr`: A `TestRecord` object representing a single test record.

**Workflow:**
1. Retrieves test data from the record.
2. Filters the data to retain valid expansion signals.
3. Calculates calibrated expansion values in micrometers.
4. Adjusts temperature data and adds the test name.

**Returns:**  
A processed DataFrame for cycler expansion data.

---

### find_matching_timestamp(desired_timestamps, time_series, t_threshold)

**Purpose:**  
Finds matching timestamps between a desired set and an existing time series within a specified threshold.

**Parameters:**
- `desired_timestamps`: Series of desired timestamps.
- `time_series`: Series containing time data from the dataset.
- `t_threshold`: Timestamp matching threshold in seconds (default is 60 seconds).

**Returns:**  
- Matched timestamps (NumPy array).
- Indices of matched timestamps within the time series.
- Indices corresponding to the desired timestamps.

---

## Cycler Data Processing

### process_cycler_data(trs, project)

**Purpose:**  
Processes cycler data from test records and computes various cycle metrics.

**Parameters:**
- `trs`: Dictionary of test records for cycler data.
- `project`: A `Project` object used to retrieve project-specific parameters (e.g., maximum capacity `qmax`).

**Workflow:**
1. Combines cycler data using `combine_cycler_data`.
2. Calculates charge/discharge capacities and average cycle data.
3. Determines voltage and temperature extremes for cycles.
4. Updates the cycle metrics DataFrame with the calculated values.

**Returns:**  
A tuple of DataFrames: processed cycler data and cycle metrics.

---

### combine_cycler_data(trs)

**Purpose:**  
Combines cycler data from multiple test records into a single DataFrame and extracts cycle metrics.

**Parameters:**
- `trs`: Dictionary of test records for cycler data.

**Workflow:**
1. Sorts and processes each test record using `process_cycle_tr`.
2. Concatenates the resulting DataFrames.
3. Assigns cycle indicators based on charge/discharge markers.
4. Extracts cycle metrics into a separate DataFrame.

**Returns:**  
A tuple: combined cell data and a DataFrame of cycle metrics.

---

### process_cycle_tr(tr, pre_aht)

**Purpose:**  
Processes and formats cycle data for a single test record.

**Parameters:**
- `tr`: A `TestRecord` object.
- `pre_aht`: Previous Ah throughput value (float) to be added to the current data.

**Workflow:**
1. Retrieves and resets the test data.
2. Adjusts the Ah throughput column by adding `pre_aht`.
3. Localizes and converts timestamps.
4. Identifies cycle start indices for charging and discharging.
5. Adds auxiliary cycle indicator columns and assigns cycle types.
6. Computes cycle metrics for further analysis.

**Returns:**  
A processed DataFrame with cycle data.

---

### find_cycle_idxs(t, i)

**Purpose:**  
Identifies the indices corresponding to the start of charging and discharging cycles.

**Parameters:**
- `t`: Series of timestamps.
- `i`: Series of current values.

**Workflow:**
1. Converts timestamps to seconds.
2. Detects potential charge/discharge start indices based on current changes.
3. Uses cumulative integration and the `rfcnt` library to determine turning points.
4. Returns arrays of charge start indices and discharge start indices.

**Returns:**  
Two NumPy arrays for charge and discharge cycle start indices.

---

### match_charge_discharge(charge_start_idxs, discharge_start_idxs)

**Purpose:**  
Matches charge and discharge indices to ensure cycles are correctly paired.

**Parameters:**
- `charge_start_idxs`: Array of charge cycle start indices.
- `discharge_start_idxs`: Array of discharge cycle start indices.

**Workflow:**
1. Adjusts the indices to ensure each cycle begins with a charge.
2. Trims the sequences to the length of the shorter array.

**Returns:**  
Matched arrays of charge and discharge start indices.

---

### calc_capacities(time_series, aht, charge_idxs, discharge_idxs, qmax)

**Purpose:**  
Calculates the charge and discharge capacities for each cycle based on Ah throughput data.

**Parameters:**
- `time_series`: Series of timestamps.
- `aht`: Series of Ah throughput values.
- `charge_idxs`: List of indices marking charge cycle starts.
- `discharge_idxs`: List of indices marking discharge cycle starts.
- `qmax`: Maximum capacity (integer).

**Workflow:**
1. Determines cycle boundaries.
2. Computes capacity differences between consecutive cycles.
3. Validates capacities against `qmax` (assigning NaN if capacity exceeds `qmax`).

**Returns:**  
Two NumPy arrays: one for charge capacities and one for discharge capacities.

---

### calc_avg_cycle_data(time_stamps, data, charge_idxs, discharge_idxs)

**Purpose:**  
Calculates average values (e.g., voltage, temperature) for each cycle using numerical integration.

**Parameters:**
- `time_stamps`: List of timestamps.
- `data`: Array of data values for which the average is calculated.
- `charge_idxs`: List of indices for charge cycles.
- `discharge_idxs`: List of indices for discharge cycles.

**Workflow:**
1. Identifies cycle boundaries.
2. Uses integration over each cycle interval to compute the average.
3. Separates the averages for charge and discharge cycles.

**Returns:**  
Two NumPy arrays containing the average values for charge and discharge cycles.

---

## Shared Methods

### max_min_cycle_data(data, cycle_idxs_minmax)

**Purpose:**  
Calculates the maximum and minimum values within each cycle segment (e.g., voltage, temperature, expansion).

**Parameters:**
- `data`: Series of data values.
- `cycle_idxs_minmax`: List of indices marking the boundaries of each cycle.

**Workflow:**
1. Iterates through each cycle segment.
2. Computes the maximum and minimum values.
3. Handles edge cases when a segment contains no data.

**Returns:**  
Two lists: one containing maximum values and the other containing minimum values for each cycle.

---

## RPT Data Processing and eSOH Estimation

### summarize_rpt_data(project)

**Purpose:**  
Summarizes the RPT data for each RPT test record and updates the cell report data.

**Parameters:**
- `project`: A `Project` object.

**Workflow:**
1. Creates a mapping of RPT filenames to their corresponding indices in the cycle metrics.
2. Iterates over the cycle metrics to build subcycle data.
3. Updates cycle metrics with HPPC data using `update_cycle_metrics_hppc`.
4. Processes ESOH data for paired charge/discharge cycles via `update_cycle_metrics_esoh`.
5. Merges relevant VDF data based on timestamp matching.
6. Concatenates the subcycle data into a final report DataFrame, sorts it, and stores it in `cell_data_rpt`.

---

### update_cycle_metrics_hppc(rpt_subcycle, i)

**Purpose:**  
Updates the cycle metrics with HPPC (Hybrid Pulse Power Characterization) data for a given subcycle.

**Parameters:**
- `rpt_subcycle`: Dictionary containing subcycle data.
- `i`: Index of the subcycle in `cell_cycle_metrics`.

**Workflow:**
1. Extracts necessary data (timestamps, current, voltage, Ah throughput).
2. Computes HPPC data via `get_rs_soc`.
3. Dynamically updates additional HPPC metric columns in `cell_cycle_metrics`.

---

### update_cycle_metrics_esoh(rpt_subcycle, pre_rpt_subcycle, i, i_slow)

**Purpose:**  
Calculates eSOH (equivalent State-of-Health) for paired charge/discharge cycles and updates the cycle metrics.

**Parameters:**
- `rpt_subcycle`: Current subcycle data.
- `pre_rpt_subcycle`: Previous subcycle data.
- `i`: Index of the subcycle in `cell_cycle_metrics`.
- `i_slow`: The RPT discharge/charge current magnitude (e.g., C/20 current).

**Workflow:**
1. Determines the charge and discharge subcycles.
2. Loads voltage data using `load_v_data`.
3. Performs eSOH estimation via `esoh_est`.
4. Updates cycle metrics with eSOH values.

---

### load_v_data(ch_rpt, dh_rpt, i_slow, i_threshold, d_int)

**Purpose:**  
Loads and processes voltage data used for eSOH calculation.

**Parameters:**
- `ch_rpt`: Dictionary containing charge subcycle data.
- `dh_rpt`: Dictionary containing discharge subcycle data.
- `i_slow`: Slow current value.
- `i_threshold`: Current threshold (default 0.005).
- `d_int`: Increment step for interpolation (default 0.01).

**Workflow:**
1. Pre-processes and resets the timestamps of charge and discharge data.
2. Filters data based on current and voltage ranges.
3. Uses numerical integration to calculate cumulative charge.
4. Interpolates the voltage and differential voltage data.
5. Returns processed Q data, averaged voltage, differential voltage, and full capacity.

---

### esoh_est(q_data, v_data, dvdq_data, q_full, window)

**Purpose:**  
Estimates eSOH parameters by fitting the open-circuit potential model to the data.

**Parameters:**
- `q_data`: Array of charge data.
- `v_data`: Array of voltage data.
- `dvdq_data`: Array of differential voltage data.
- `q_full`: Full capacity value.
- `window`: Window length for data filtering (default 5).

**Workflow:**
1. Sets up bounds and nonlinear constraints.
2. Uses `minimize` from `scipy.optimize` to fit the model.
3. Extracts fitting parameters and computes model voltage.
4. Calculates errors and peak differences.
5. Returns fitted parameters, capacity, and error metrics.

---

### filter_qv_data(qdata, vdata, window_length, polyorder)

**Purpose:**  
Filters Q-V data using a Savitzky-Golay filter.

**Parameters:**
- `qdata`: Array of Q (charge) data.
- `vdata`: Array of voltage data.
- `window_length`: Length of the filter window.
- `polyorder`: Polynomial order (default 3).

**Returns:**  
Filtered Q data, filtered V data, and computed differential voltage (dV/dQ).

---

### get_rs_soc(t, i, v, q)

**Purpose:**  
Processes HPPC data to estimate DC resistance (RS) from pulse tests.

**Parameters:**
- `t`: Array of time data.
- `i`: Array of current data.
- `v`: Array of voltage data.
- `q`: Array of Ah throughput data.

**Workflow:**
1. Identifies pulse start and end indices.
2. Calculates short-term and long-term resistances.
3. Aggregates the pulse data into a DataFrame.

**Returns:**  
A DataFrame with HPPC metrics (pulse current, duration, Q, RS values).

---

### fitfunc(x, q_data, v_data, dvdq_data, dvdq_bool)

**Purpose:**  
Objective function for optimization in eSOH calculation.

**Parameters:**
- `x`: Parameter vector.
- `q_data`: Array of Q data.
- `v_data`: Array of voltage data.
- `dvdq_data`: Array of differential voltage data.
- `dvdq_bool`: Flag for applying weighting (default True).

**Workflow:**
1. Computes model voltage using `calc_opc`.
2. Applies weighting factors based on Q ranges.
3. Calculates the error norm.

**Returns:**  
The norm of the error, which is minimized during optimization.

---

### get_peaks(q, dvdq)

**Purpose:**  
Finds peaks in the dV/dQ data to identify characteristic Q values.

**Parameters:**
- `q`: Array of Q data.
- `dvdq`: Array of differential voltage data.

**Workflow:**
1. Identifies peaks with specified prominence.
2. Filters peaks within 10%-90% of maximum Q.
3. Returns the first and last peak positions.

---

### calc_opc(x, q)

**Purpose:**  
Calculates the open circuit potential (OPC) for a given stoichiometry.

**Parameters:**
- `x`: Parameter vector.
- `q`: Scalar Q value.

**Workflow:**
1. Calculates contributions from negative and positive electrode models.
2. Averages the results to compute OPC.

**Returns:**  
The calculated OPC.

---

### sort_trs(trs)

**Purpose:**  
Sorts TestRecord objects based on their timestamp.

**Parameters:**
- `trs`: Dictionary of TestRecord objects.

**Returns:**  
A sorted dictionary of TestRecords.

---

## Data Combination

### combine_data(cell_data, cell_data_vdf)

**Purpose:**  
Combines expansion data from VDF with cycler data based on timestamp matching.

**Parameters:**
- `cell_data`: DataFrame from the cycler.
- `cell_data_vdf`: DataFrame from the VDF.

**Workflow:**
1. Extracts relevant columns from the VDF data.
2. Converts timestamps and localizes them.
3. Merges the cycler and VDF data using `merge_asof` with a 1-second tolerance.

**Returns:**  
A merged DataFrame combining data from both sources.

---
