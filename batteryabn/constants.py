from datetime import timedelta, timezone


class Constants:
    DEFAULT_TIME_ZONE_INFO = timezone(timedelta(days=-1, seconds=72000))
    
    FILE_TYPE_2_TEST_TYPE = {'res': 'Arbin', 'mpt': 'BioLogic', 'xlsx': 'Neware', 'csv': 'Neware_Vdf'}

    ARBIN_RENAME_DICT = {'step_time': 'time',
                     'test_time': 'total time',
                     'date_time': 'timestamp',
                     'current': 'current(a)',
                     'voltage': 'voltage(v)',
                     'charge_capacity': 'chg. cap.(ah)',
                     'discharge_capacity': 'dchg. cap.(ah)',
                     'charge_energy': 'chg. energy(wh)',
                     'discharge_energy': 'dchg. energy(wh)',
                     'internal_resistance': 'contact resistance(mω)'}
    
    BIOLOGIC_RENAME_DICT = {'cycle number': 'cycle index',
                        'mode': 'step type',
                        'time/s': 'total time',
                        'i': 'current(a)',
                        'ecell/v': 'voltage(v)',
                        # TODO: Check the correct units for the ma.h columns
                        'capacity/ma.h': 'capacity(ah)',
                        'q charge/ma.h': 'chg. cap.(ah)',
                        'q discharge/ma.h': 'dchg. cap.(ah)',
                        'energy charge/w.h': 'chg. energy(wh)',
                        'energy discharge/w.h': 'dchg. energy(wh)',
                        'half cycle': 'dqm/dv(mah/v.g)',
                        'temperature/°c': 'cell temperature (c)',
                        'efficiency/%': 'ambient temperature (c)'}
    
    NEWARE_RENAME_DICT = {'t1(℃)': 'cell temperature (c)'}

    NEWARE_VDF_RENAME_DICT = {'test time (second)': 'time',
                          'timestamp (epoch)': 'timestamp',
                          'current (amp)': 'current(a)',
                          'potential (volt)': 'voltage(v)',
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