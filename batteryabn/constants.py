from datetime import timedelta, timezone


class Constants:
    DEFAULT_TIME_ZONE_INFO = timezone(timedelta(days=-1, seconds=72000))

    TIME = 'time' # TODO: Should match Time [ms]
    STEP_IDX = 'step index'
    CYCLE_IDX = 'cycle index'
    CURRENT = 'current(a)'
    VOLTAGE = 'voltage(v)'
    AHT = 'capacity(ah)'
    TEMPERATURE = 'cell temperature (c)'
    CHARGE_CAPACITY = 'chg. cap.(ah)'
    DISCHARGE_CAPACITY = 'dchg. cap.(ah)'
    
    FILE_TYPE_2_TEST_TYPE = {'res': 'Arbin', 'mpt': 'BioLogic', 'xlsx': 'Neware', 'csv': 'Neware_Vdf'}

    ARBIN_RENAME_DICT = {'step_time': 'time',
                        'step_index': STEP_IDX,
                        'cycle_index': CYCLE_IDX,
                        'test_time': 'total time',
                        'date_time': 'timestamp',
                        'current': CURRENT,
                        'voltage': VOLTAGE,
                        'charge_capacity': CHARGE_CAPACITY,
                        'discharge_capacity': DISCHARGE_CAPACITY,
                        'charge_energy': 'chg. energy(wh)',
                        'discharge_energy': 'dchg. energy(wh)',
                        'internal_resistance': 'contact resistance(mω)'}
    
    BIOLOGIC_RENAME_DICT = {'cycle number': CYCLE_IDX,
                        'mode': 'step type',
                        'time/s': 'total time',
                        'i': CURRENT,
                        'ecell/v': VOLTAGE,
                        # TODO: Check the correct units for the ma.h columns
                        'capacity/ma.h': AHT,
                        'q charge/ma.h': CHARGE_CAPACITY,
                        'q discharge/ma.h': DISCHARGE_CAPACITY,
                        'energy charge/w.h': 'chg. energy(wh)',
                        'energy discharge/w.h': 'dchg. energy(wh)',
                        'half cycle': 'dqm/dv(mah/v.g)',
                        'temperature/°c': TEMPERATURE,
                        'efficiency/%': 'ambient temperature (c)'}
    
    NEWARE_RENAME_DICT = {'t1(℃)': TEMPERATURE}

    NEWARE_VDF_RENAME_DICT = {'test time (second)': 'time',
                          'timestamp (epoch)': 'timestamp',
                          'current (amp)': CURRENT,
                          'potential (volt)': VOLTAGE,
                          'ambient temperature (celsius)': 'ambient temperature (c)'}
    ARBIN_NAME_KEYS = [
        "Project Name",
        "Cell ID",
        "Test Type",
        "Procedure Version",
        "Temperature",
        "Pressure",
        "Test Date",
        "Run Number"
        ]

    BIOLOGIC_NAME_KEYS = [
        "Project Name",
        "Cell ID",
        "Test Type",
        "Procedure Version",
        "Temperature",
        "Pressure",
        "Test Date",
        "Run Number",
        "Channel Number"
    ]

    NEWARE_NAME_KEYS = [
        "Project Name",
        "Cell ID",
        "Test Type",
        "Procedure Version",
        "Temperature",
        "Pressure",
        "Test Date",
        "Run Number",
        "Channel Number",
        "Start Time",
        "Device ID",
        "Unit ID",
        "CH ID",
        "Test ID"
    ]

    NEWARE_VDF_NAME_KEYS = [
        "Project Name",
        "Cell ID",
        "Test Type",
        "Procedure Version",
        "Temperature",
        "Pressure",
        "Test Date",
        "Run Number",
        "Channel Number"
    ]

    CYCLE_TYPES = ['CYC', 'RPT', 'Test11', 'EIS', 'CAL', '_F']

    V_MAX_CYCLE = 'v_max_cycle'
    V_MIN_CYCLE = 'v_min_cycle'
    DT_MIN = 'dt_min'
    DAH_MIN = 'dAh_min'

    CYCLE_ID_LIMS= {
    'CYC': {V_MAX_CYCLE:3.8, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.1}, # Default values for cycle type
    'RPT': {V_MAX_CYCLE:4.1, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.1},
    'Test11': {V_MAX_CYCLE:3.6, V_MIN_CYCLE:3.6, DT_MIN: 600, DAH_MIN:0.1},
    'EIS': {V_MAX_CYCLE:4.1, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.5}, # same as RPT, but says EIS in the filenames for some GM cells
    'CAL': {V_MAX_CYCLE:3.8, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.5},
    '_F': {V_MAX_CYCLE:3.8, V_MIN_CYCLE:3.8, DT_MIN: 3600, DAH_MIN:0.5} # Formation files handled via peak finding
    }


    DISCHARGE_CYCLE_IDC = 'discharge cycle indicator'
    CHARGE_CYCLE_IDC = 'charge cycle indicator'
    CAPACITY_CHECK_IDC = 'capacity check indicator'
    CYCLE_IDC = 'cycle indicator'
    INDICATORS = [DISCHARGE_CYCLE_IDC, CHARGE_CYCLE_IDC, CAPACITY_CHECK_IDC]

    CYCLE_TYPE = 'cycle type'
    TEST_NAME = 'test name'
    PROTOCOL = 'protocol'  

    MIN_CYCLE_VOLTAGE = 'min cycle voltage (v)' 
    MAX_CYCLE_VOLTAGE = 'max cycle voltage (v)'
    MIN_CYCLE_TEMP = 'min cycle temperature (c)'
    MAX_CYCLE_TEMP = 'max cycle temperature (c)'
    AVG_CYCLE_CHARGE_CURRENT = 'avg cycle charge current (a)'
    AVG_CYCLE_DISCHARGE_CURRENT = 'avg cycle discharge current (a)'

    CCM_COLUMNS = [TIME, AHT, CYCLE_TYPE, PROTOCOL, DISCHARGE_CYCLE_IDC, CHARGE_CYCLE_IDC, 
                   CAPACITY_CHECK_IDC, CYCLE_IDX, TEST_NAME]
    CCM_COLUMNS_ADDITIONAL = [CHARGE_CAPACITY, DISCHARGE_CAPACITY, MIN_CYCLE_VOLTAGE, MAX_CYCLE_VOLTAGE, 
                              MIN_CYCLE_TEMP, MAX_CYCLE_TEMP, AVG_CYCLE_CHARGE_CURRENT, AVG_CYCLE_DISCHARGE_CURRENT]

    QMAX = 3.8

    # TODO: These values should be placed in a configuration yaml or json file
    GMJULY2022_PULSE_CURRENTS = [3.0, 1.5, -3.0, -1.5, -0.5]
    GMFEB23_PULSE_CURRENTS = [2.0, 1.0, 0.5, -2.0, -1.0, -0.5]
    UMBL2022FEB_PULSE_CURRENTS = [2.0, 1.0, 0.5, -2.0, -1.0, -0.5]
    DEFAULT_PULSE_CURRENTS = [2.0, 1.0, -2.0, -1.0, -0.5]
    PROJECTS_SETTING = {
        'DEFAULT':{
            'pulse_currents':DEFAULT_PULSE_CURRENTS,
            'nominal_capacity':3.5, #A.h
            'Qmax': 3.8,
            'I_C20': 0.177,
        },
        'GMJULY2022':{
            'pulse_currents':GMJULY2022_PULSE_CURRENTS,
            'nominal_capacity':3.5, #A.h
            'Qmax': 3.8,
            'I_C20': 0.177,
        },
        'UNKNOWN_PROJECT':{
            'pulse_currents':GMJULY2022_PULSE_CURRENTS,
            'nominal_capacity':3.5, #A.h
            'Qmax': 3.8,
            'I_C20': 0.177,
        },
        'GMFEB23':{
            'pulse_currents':GMFEB23_PULSE_CURRENTS,
            'nominal_capacity':3.5, #A.h
            'Qmax': 3.8,
            'I_C20': 0.177,
        },
        'UMBL2022FEB':{
            'pulse_currents':UMBL2022FEB_PULSE_CURRENTS,
            'nominal_capacity':2.5, #A.h
            'Qmax': 2.8,
            'I_C20': 0.125,
        }
    }


    #----------------------------------VDF-----------------------------------------
    #TODO: Check the column for the VDF data
    EXPANSION = 'expansion'
    EXPANSION_UM = 'expansion (um)'

    TIME_VDF = 'time vdf (s)'
    MIN_CYCLE_EXPANSION = 'min cycle expansion'
    MAX_CYCLE_EXPANSION = 'max cycle expansion'
    REV_CYCLE_EXPANSION = 'reversible expansion'
    MIN_CYCLE_EXPANSION_UM = 'min cycle expansion (um)'
    MAX_CYCLE_EXPANSION_UM = 'max cycle expansion (um)'
    REV_CYCLE_EXPANSION_UM = 'reversible expansion (um)'
    # TODO: Following 3 columns should be in cell_data_vdf
    DRIVE_CURRENT = 'drive current'
    EXPANSION_STDDEV = 'expansion stddev (cnt)'
    REF_STDDEV = 'ref stddev (cnt)'

    CCM_COLUMNS_ADDITIONAL_VDF = [TIME_VDF, MIN_CYCLE_EXPANSION, MAX_CYCLE_EXPANSION, REV_CYCLE_EXPANSION, 
                                  MIN_CYCLE_EXPANSION_UM, MAX_CYCLE_EXPANSION_UM, REV_CYCLE_EXPANSION_UM, 
                                  DRIVE_CURRENT, EXPANSION_STDDEV, REF_STDDEV]
