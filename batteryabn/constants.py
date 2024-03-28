from datetime import timedelta, timezone


class Constants:
        
#------------------------------------Strings:------------------------------------------#
    TIME = 'time' # TODO: Should match Time [ms]
    STEP_IDX = 'step index'
    CYCLE_IDX = 'cycle index'
    CURRENT = 'current(a)'
    VOLTAGE = 'voltage(v)'
    AHT = 'capacity(ah)'
    TEMPERATURE = 'temperature (c)'
    CHARGE_CAPACITY = 'chg. cap.(ah)'
    DISCHARGE_CAPACITY = 'dchg. cap.(ah)'
    CHARGE_ENERGY = 'chg. energy(wh)'
    DISCHARGE_ENERGY = 'dchg. energy(wh)'
    TIMESTAMP = 'timestamp'
    TOTAL_TIME = 'total time'
    CONTACT_RESISTANCE = 'contact resistance(mω)'
    
    FILE_TYPE_2_TEST_TYPE = {'res': 'Arbin', 'mpt': 'BioLogic', 'xlsx': 'Neware', 'csv': 'Neware_Vdf'}

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


    DISCHARGE_CYCLE_IDC = 'discharge cycle indicator'
    CHARGE_CYCLE_IDC = 'charge cycle indicator'
    CAPACITY_CHECK_IDC = 'capacity check indicator'
    CYCLE_IDC = 'cycle indicator'
    INDICATORS = [DISCHARGE_CYCLE_IDC, CHARGE_CYCLE_IDC, CAPACITY_CHECK_IDC]

    CYCLE_TYPE = 'cycle type'
    TEST_NAME = 'test name'
    PROTOCOL = 'protocol'  
    # Protocols: HPPC, C/20 Charge, C/20 Discharge
    HPPC = 'HPPC'
    C20_CHARGE = 'C/20 Charge'
    C20_DISCHARGE = 'C/20 Discharge'

    MIN_CYCLE_VOLTAGE = 'min cycle voltage (v)' 
    MAX_CYCLE_VOLTAGE = 'max cycle voltage (v)'
    MIN_CYCLE_TEMP = 'min cycle temperature (c)'
    MAX_CYCLE_TEMP = 'max cycle temperature (c)'
    AVG_CYCLE_CHARGE_CURRENT = 'avg cycle charge current (a)'
    AVG_CYCLE_DISCHARGE_CURRENT = 'avg cycle discharge current (a)'

    CCM_COLUMNS = [TIME, TIMESTAMP, AHT, CYCLE_TYPE, PROTOCOL, DISCHARGE_CYCLE_IDC, CHARGE_CYCLE_IDC, 
                CAPACITY_CHECK_IDC, CYCLE_IDC, TEST_NAME]
    CCM_COLUMNS_ADDITIONAL = [CHARGE_CAPACITY, DISCHARGE_CAPACITY, MIN_CYCLE_VOLTAGE, MAX_CYCLE_VOLTAGE, 
                            MIN_CYCLE_TEMP, MAX_CYCLE_TEMP, AVG_CYCLE_CHARGE_CURRENT, AVG_CYCLE_DISCHARGE_CURRENT]


    #----------------------------------VDF-----------------------------------------#
    #TODO: Check the column for the VDF data
    EXPANSION = 'expansion'
    EXPANSION_UM = 'expansion (um)'
    EXPANSION_REF = 'expansion ref'

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

    VDF_COLUMNS = [TIME, EXPANSION, EXPANSION_REF, TEMPERATURE, CYCLE_IDC, DRIVE_CURRENT,EXPANSION_STDDEV, REF_STDDEV]

    CCM_COLUMNS_ADDITIONAL_VDF = [TIME_VDF, MIN_CYCLE_EXPANSION, MAX_CYCLE_EXPANSION, REV_CYCLE_EXPANSION, 
                                MIN_CYCLE_EXPANSION_UM, MAX_CYCLE_EXPANSION_UM, REV_CYCLE_EXPANSION_UM, 
                                DRIVE_CURRENT, EXPANSION_STDDEV, REF_STDDEV]


    #----------------------------------RPT-------------------------------------#

    RPT = 'RPT #'
    DATA = 'Data'
    DATA_VDF = 'Data VDF'
    RPT_TYPES = ['RPT', '_F', '_Cy100', '_Cby100']

    #-------HPPC-------#
    PULSE_CURRENT = 'pulse current'
    PULSE_DURATION = 'pulse duration'
    PULSE_Q = 'pulse q'
    R_S = 'R_s'
    R_L = 'R_l'

    CCM_COLUMNS_ADDITIONAL_HPPC = [PULSE_CURRENT, PULSE_DURATION, PULSE_Q, R_S, R_L]

    #-------eSOH-------#
    ESOH_C = 'C'
    ESOH_CN = 'Cn'
    ESOH_X0 = 'X0'
    ESOH_X100 = 'X100'
    ESOH_CP = 'Cp'
    ESOH_Y0 = 'Y0'
    ESOH_Y100 = 'Y100'
    RMSE_V = 'RMSE_V'
    RMSE_DVDQ = 'RMSE_dVdQ'
    P1_ERR = 'P1_err'
    P2_ERR = 'P2_err'
    P12_ERR = 'P12_err'

    CCM_COLUMNS_ADDITIONAL_ESOH = [ESOH_C, ESOH_CN, ESOH_X0, ESOH_X100, ESOH_CP, ESOH_Y0, 
                                   ESOH_Y100, RMSE_V, RMSE_DVDQ, P1_ERR, P2_ERR, P12_ERR]

    #-------------------RENAME_DICT-------------------#

    ARBIN_RENAME_DICT = {'step_time': TIME,
                        'step_index': STEP_IDX,
                        'cycle_index': CYCLE_IDX,
                        'test_time': TOTAL_TIME,
                        'date_time': TIMESTAMP,
                        'current': CURRENT,
                        'voltage': VOLTAGE,
                        'charge_capacity': CHARGE_CAPACITY,
                        'discharge_capacity': DISCHARGE_CAPACITY,
                        'charge_energy': CHARGE_ENERGY,
                        'discharge_energy': DISCHARGE_ENERGY,
                        'internal_resistance': CONTACT_RESISTANCE}
    
    BIOLOGIC_RENAME_DICT = {'cycle number': CYCLE_IDX,
                        'mode': 'step type',
                        'time/s': TOTAL_TIME,
                        'i': CURRENT,
                        'ecell/v': VOLTAGE,
                        # TODO: Check the correct units for the ma.h columns
                        'capacity/ma.h': AHT,
                        'q charge/ma.h': CHARGE_CAPACITY,
                        'q discharge/ma.h': DISCHARGE_CAPACITY,
                        'energy charge/w.h': CHARGE_ENERGY,
                        'energy discharge/w.h': DISCHARGE_ENERGY,
                        'half cycle': 'dqm/dv(mah/v.g)',
                        'temperature/°c': TEMPERATURE,
                        'efficiency/%': 'efficiency/%'}
    
    NEWARE_RENAME_DICT = {'t1(℃)': TEMPERATURE}

    NEWARE_VDF_RENAME_DICT = {'test time (second)': TIME,
                        'timestamp (epoch)': TIMESTAMP,
                        'current (amp)': CURRENT,
                        'potential (volt)': VOLTAGE,
                        'ldc sensor': EXPANSION,
                        'ldc ref': EXPANSION_REF,
                        'ambient temperature (celsius)': TEMPERATURE,
                        'ldc std': EXPANSION_STDDEV,
                        'ref std': REF_STDDEV,
                        'drivecurrent': DRIVE_CURRENT,}
    


#------------------------------------Numeric:------------------------------------#
    DEFAULT_TIME_ZONE_INFO = timezone(timedelta(days=-1, seconds=72000))

    QMAX = 3.8
    I_C20 = 0.177

    #------------------------Project Setting---------------------------#
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
    CYCLE_ID_LIMS= {
    'CYC': {V_MAX_CYCLE:3.8, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.1}, # Default values for cycle type
    'RPT': {V_MAX_CYCLE:4.1, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.1},
    'Test11': {V_MAX_CYCLE:3.6, V_MIN_CYCLE:3.6, DT_MIN: 600, DAH_MIN:0.1},
    'EIS': {V_MAX_CYCLE:4.1, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.5}, # same as RPT, but says EIS in the filenames for some GM cells
    'CAL': {V_MAX_CYCLE:3.8, V_MIN_CYCLE:3.8, DT_MIN: 600, DAH_MIN:0.5},
    '_F': {V_MAX_CYCLE:3.8, V_MIN_CYCLE:3.8, DT_MIN: 3600, DAH_MIN:0.5} # Formation files handled via peak finding
    }

    X0 = [4.2,0.85,5.5,0.3]
    LB = [1, 0, 1, 0]
    UB = [5, 1, 6.5, 1]

    W1 = 0.2
    W2 = 1
    W3 = 2

    UN_VAR1=[-3.54049607669295,0.00708244334002580,0.00774192469266890, 
        4.26893363759502,-0.0164043013936254,-4.05401806281007, 
        0.0426131798578846,-3.19444157210193,0.0503611972394406, 
        0.170261138869476,0.147567301186300,0.0382504766072001, 
        0.519446050169237,1.10619736534131,0.0145120887836752, 
        -0.0816693980616928,-0.0119716740325398,-0.00723858739498425, 
        -0.0877677643234304,0.0238786887373114,0.0452264234816890, 
        -0.00713413913218840]

    UN_VAR2=[-2.74740857138957,0.00443109156371119,0.0140962302368559, 
            3.10348817994589,-0.0128948359572101,-4.36083705035769, 
            0.0643328570911640,-3.88703879262989,0.0631828141079049, 
            0.213012646348329,0.174731100372283,0.0577291579271751, 
            0.518982409471130,1.21588542781399,0.0150389780167150, 
            -0.0584524226380269,-0.00702394962468186,-0.0342305292048576, 
            -0.0619846453717142,0.0123530018211038,0.0873816814557679, 
            -0.00843321991754559]

    P1 = -2253.9364
    P2 = 10756.6071
    P3 = -21755.8183
    P4 = 24277.2504
    P5 = -16299.5659
    P6 = 6728.9153
    P7 = -1670.2785
    P8 = 233.2321
    P9 = -18.3223
    P10 = 5.3936