import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np 
import pandas as pd

from batteryabn import logger, Constants as Const
from batteryabn.utils import Processor, Utils

class Viewer:

    def __init__(self):
        """
        A class to visualize battery test data.
        """
        pass

    def plot(self, processor: Processor, cell_name: str):
        """
        Plot the processed cell data.

        Parameters
        ----------
        processor : Processor
            Processor object with processed cell data
        cell_name : str
            The name of the cell
        """

        cell_data = processor.cell_data
        cell_data_vdf = processor.cell_data_vdf
        cell_cycle_metrics = processor.cell_cycle_metrics
        
        fig1 = self.plot_process_cell(cell_data, cell_data_vdf, cell_cycle_metrics, cell_name)
        fig2 = self.plot_cycle_metrics_time(cell_data, cell_data_vdf, cell_cycle_metrics, cell_name)
        fig3 = self.plot_cycle_metrics_aht(cell_data, cell_data_vdf, cell_cycle_metrics, cell_name)

        return fig1, fig2, fig3
        
    def plot_process_cell(self, cell_data: pd.DataFrame, cell_data_vdf: pd.DataFrame, 
                          cell_cycle_metrics: pd.DataFrame, cell_name: str, downsample = 100):

        # Cell data
        t = cell_data[Const.TIMESTAMP]
        i = cell_data[Const.CURRENT]
        v = cell_data[Const.VOLTAGE]
        temperature = cell_data[Const.TEMPERATURE]
        aht = cell_data[Const.AHT]

        # Choose cell_data_vdf[Const.EXPANSION_UM] > -5000 to remove outliers
        vdf_filter_idx = cell_data_vdf[Const.EXPANSION_UM] > -5000
        t_vdf = pd.to_datetime(cell_data_vdf[Const.TIMESTAMP][vdf_filter_idx], unit='ms')
        exp_vdf = cell_data_vdf[Const.EXPANSION_UM][vdf_filter_idx]
        temperature_vdf = cell_data_vdf[Const.TEMPERATURE][vdf_filter_idx]

        # CCM
        t_cycle = cell_cycle_metrics[Const.TIMESTAMP]
        q_c = cell_cycle_metrics[Const.CHARGE_CAPACITY]
        q_d = cell_cycle_metrics[Const.DISCHARGE_CAPACITY]

        # Index metrics
        cycle_idx = cell_data[cell_data[Const.CYCLE_IDC]].index
        capacity_check_idx = cell_data[cell_data[Const.CAPACITY_CHECK_IDC]].index
        # TODO
        cycle_vdf_idx = cell_data_vdf[cell_data_vdf[Const.CYCLE_IDC]].index
        capacity_check_in_cycle_idx = cell_cycle_metrics[cell_cycle_metrics[Const.CAPACITY_CHECK_IDC]].index
        charge_idx = cell_data[cell_data[Const.CHARGE_CYCLE_IDC]].index

        # t_array = Utils.time_str_to_seconds(t)
        # _, ips, vps, idxs = self.downsample_data(t_array, i.to_numpy(), v.to_numpy())
        # tt = t[idxs]

        logger.info("Plotting cell: " + cell_name)
        # Setup plot 
        fig, axes = plt.subplots(6,1, figsize=(6,6), sharex=True)
        
        # Plot current 
        ax0 = axes.flat[0]
        ax0.plot_date(t, i, '-')
        ax0.plot_date(t[cycle_idx], i[cycle_idx], "x")
        ax0.plot_date(t[capacity_check_idx], i[capacity_check_idx], "*", c = "r")
        ax0.set_ylabel("Current [A]")
        ax0.grid()

        # Plot voltage 
        ax1 = axes.flat[1]
        ax1.plot_date(t,v,'-')
        ax1.plot_date(t[cycle_idx], v[cycle_idx], "x")
        ax1.plot_date(t[charge_idx], v[charge_idx], "o")
        ax1.plot_date(t[capacity_check_idx], v[capacity_check_idx], "*", c = "r")
        ax1.set_ylabel("Voltage [V]")
        ax1.grid()

        # Plot temperature
        ax2 = axes.flat[2]
        ax2.plot_date(t[0::downsample], temperature[0::downsample], '-')
        ax2.plot_date(t_vdf[0::downsample], temperature_vdf[0::downsample], '--', c='grey')
        ax2.plot_date(t[capacity_check_idx], temperature[capacity_check_idx], "*", c = "r")
        ax2.plot_date(t[cycle_idx], temperature[cycle_idx], "x")
        ax2.set_ylabel("Temperature \n [degC]")
        ax2.grid()

        # Set up expansion plot with points aligning with the end of the cycle
        ax3 = axes.flat[3]
        if not all(t_vdf.isnull()):
            ax3.plot_date(t_vdf[0::100], exp_vdf[0::100], '-')
            if cycle_vdf_idx is not None:
                try:
                    ax3.plot_date(t_vdf[cycle_vdf_idx], exp_vdf[cycle_vdf_idx], "x")
                except Exception as e:
                    logger.error(f"Error plotting cycle index: {e}")
    
        ax3.set_ylabel("Expansion [um]")
        ax3.grid()

        # Plot AhT 
        ax4 = axes.flat[4]
        ax4.plot_date(t[0::downsample], aht[0::downsample],'-')
        ax4.plot_date(t[cycle_idx], aht[cycle_idx], "x")
        ax4.set_ylabel("AhT [A.h]")
        ax4.grid()
        
        # Plot capacity 
        ax5 = axes.flat[5]
        ax5.plot_date(t_cycle, q_c)
        ax5.plot_date(t_cycle, q_d)
        ax5.plot_date(t[capacity_check_idx], q_c[capacity_check_in_cycle_idx], "*", c = "r")
        ax5.plot_date(t[capacity_check_idx], q_d[capacity_check_in_cycle_idx], "*", c = "r")
        ax5.set_ylabel("Apparent \n capacity [A.h]")
        ax5.grid()

        fig.autofmt_xdate()
        fig.suptitle("Cell: " + cell_name)
        fig.tight_layout()
        return fig
    

    def plot_cycle_metrics_time(self, cell_data: pd.DataFrame, cell_data_vdf: pd.DataFrame, 
                          cell_cycle_metrics: pd.DataFrame, cell_name: str, downsample = 100):

        # Cell data
        t = cell_data[Const.TIMESTAMP]
        i = cell_data[Const.CURRENT]
        v = cell_data[Const.VOLTAGE]
        temperature = cell_data[Const.TEMPERATURE]
        aht = cell_data[Const.AHT]

        # Choose cell_data_vdf[Const.EXPANSION_UM] > -5000 to remove outliers
        vdf_filter_idx = cell_data_vdf[Const.EXPANSION_UM] > -5000
        t_vdf = pd.to_datetime(cell_data_vdf[Const.TIMESTAMP][vdf_filter_idx], unit='ms')
        exp_vdf = cell_data_vdf[Const.EXPANSION_UM][vdf_filter_idx]
        temperature_vdf = cell_data_vdf[Const.TEMPERATURE][vdf_filter_idx]

        t_cycle = cell_cycle_metrics[Const.TIMESTAMP]
        q_c = cell_cycle_metrics[Const.CHARGE_CAPACITY]
        q_d = cell_cycle_metrics[Const.DISCHARGE_CAPACITY]
        v_min = cell_cycle_metrics[Const.MIN_CYCLE_VOLTAGE]
        v_max = cell_cycle_metrics[Const.MAX_CYCLE_VOLTAGE]
        temperature_min = cell_cycle_metrics[Const.MIN_CYCLE_TEMP]
        temperature_max = cell_cycle_metrics[Const.MAX_CYCLE_TEMP]
        exp_min = cell_cycle_metrics[Const.MIN_CYCLE_EXPANSION_UM]
        exp_max = cell_cycle_metrics[Const.MAX_CYCLE_EXPANSION_UM]
        exp_rev = cell_cycle_metrics[Const.REV_CYCLE_EXPANSION_UM]

        # Index metrics
        cycle_idx = cell_data[cell_data[Const.CYCLE_IDC]].index
        capacity_check_idx = cell_data[cell_data[Const.CAPACITY_CHECK_IDC]].index
        # TODO
        cycle_vdf_idx = cell_data_vdf[cell_data_vdf[Const.CYCLE_IDC]].index
        capacity_check_in_cycle_idx = cell_cycle_metrics[cell_cycle_metrics[Const.CAPACITY_CHECK_IDC]].index
        charge_idx = cell_data[cell_data[Const.CHARGE_CYCLE_IDC]].index

        logger.info("Plotting cycle metrics: " + cell_name)
        # Setup plot 
        fig, axes = plt.subplots(3,4,figsize=(18,6), sharex=True)

        # Plot current 
        ax0 = axes.flat[0]
        ax0.plot_date(t[0::downsample], i[0::downsample],'-')
        ax0.plot_date(t[cycle_idx], i[cycle_idx], "x")
        ax0.plot_date(t[charge_idx], i[charge_idx], "o")
        ax0.plot_date(t[capacity_check_idx], i[capacity_check_idx], "*", c = "r")
        ax0.set_ylabel("Current[A]")
        ax0.grid()

        # Plot voltage 
        ax1 = axes.flat[1]
        ax1.plot_date(t[0::downsample], v[0::downsample],'-')
        ax1.plot_date(t[cycle_idx], v[cycle_idx], "x")
        ax1.plot_date(t[charge_idx], v[charge_idx], "o")
        ax1.plot_date(t[capacity_check_idx], v[capacity_check_idx], "*", c = "r")
        ax1.set_ylabel("Voltage [V]")
        ax1.grid()

        # Plot temperature
        ax2 = axes.flat[2]
        ax2.plot_date(t[0::downsample], temperature[0::downsample], '-')
        ax2.plot_date(t_vdf[0::downsample], temperature_vdf[0::downsample], '--',  c = 'grey')
        ax2.plot_date(t[cycle_idx], temperature[cycle_idx], "x")
        ax2.plot_date(t[capacity_check_idx], temperature[capacity_check_idx], "*", c = "r")
        ax2.set_ylabel("Temp [degC]")
        ax2.grid()

        # Plot exponsion
        ax3 = axes.flat[3]
        if not all(t_vdf.isnull()):
            ax3.plot_date(t_vdf[0::downsample], exp_vdf[0::downsample], '-') 
            ax3.plot_date(t_vdf[cycle_vdf_idx], exp_vdf[cycle_vdf_idx], "x")
        ax3.set_ylabel("Expansion [um]")
        ax3.grid()

        # Plot AhT 
        ax4 = axes.flat[4]
        ax4.plot_date(t[0::downsample], aht[0::downsample],'-')
        ax4.plot_date(t[cycle_idx], aht[cycle_idx], "x")
        ax4.plot_date(t[capacity_check_idx], aht[capacity_check_idx], "*", c = "r")
        ax4.set_ylabel("Ah Throughput")
        ax4.grid()

        # Plot capacity 
        ax8 = axes.flat[8]
        ax8.plot_date(t_cycle, q_c)
        ax8.plot_date(t_cycle, q_d)
        ax8.plot_date(t[capacity_check_idx], q_c[capacity_check_in_cycle_idx], "*", c = "r")
        ax8.plot_date(t[capacity_check_idx], q_d[capacity_check_in_cycle_idx], "*", c = "r")
        ax8.set_ylabel("Apparent \n capacity [A.h]")
        ax8.grid()

        # Plot min/max voltage 
        ax5 = axes.flat[5]
        ax5.plot_date(t_cycle, v_max)
        ax5.plot_date(t[capacity_check_idx], v_max[capacity_check_in_cycle_idx], "*", c = "r")
        ax5.set_ylabel("Max Voltage [V]")
        ax5.grid()

        ax9 = axes.flat[9]
        ax9.plot_date(t_cycle,v_min)
        ax9.plot_date(t[capacity_check_idx], v_min[capacity_check_in_cycle_idx], "*", c = "r")
        ax9.set_ylabel("Min Voltage [V]")
        ax9.grid()

        # Plot min/max temperature
        ax6 = axes.flat[6]
        ax6.plot_date(t_cycle, temperature_max)
        ax6.plot_date(t[capacity_check_idx], temperature_max[capacity_check_in_cycle_idx], "*", c = "r")
        ax6.set_ylabel("Max Temp [degC]")
        ax6.grid()

        ax10 = axes.flat[10]
        ax10.plot_date(t_cycle, temperature_min)
        ax10.plot_date(t[capacity_check_idx], temperature_min[capacity_check_in_cycle_idx], "*", c = "r")
        ax10.set_ylabel("Min Temp [degC]")
        ax10.grid()

        # Plot min/max/rev expansion  
        ax7 = axes.flat[7]
        ax7.plot_date(t_cycle, exp_max) 
        ax7.plot_date(t_cycle, exp_min)
        ax7.plot_date(t_cycle[capacity_check_in_cycle_idx], exp_max[capacity_check_in_cycle_idx], "*", c = "r") 
        ax7.plot_date(t_cycle[capacity_check_in_cycle_idx], exp_min[capacity_check_in_cycle_idx], "*", c = "r")
        ax7.set_ylabel("Min/Max Exp [um]")
        ax7.grid()

        ax15 = axes.flat[11]
        ax15.plot_date(t_cycle, exp_rev)
        ax15.plot_date(t_cycle[capacity_check_in_cycle_idx], exp_rev[capacity_check_in_cycle_idx], "*", c = "r")
        ax15.set_ylabel("Rev expansion [um]")
        ax15.grid()

        fig.autofmt_xdate()
        fig.suptitle("Cell: " + cell_name)
        fig.tight_layout()
        return fig

    def plot_cycle_metrics_aht(self, cell_data: pd.DataFrame, cell_data_vdf: pd.DataFrame, 
                          cell_cycle_metrics: pd.DataFrame, cell_name: str, downsample = 100):

        # Cell data
        i = cell_data[Const.CURRENT]
        v = cell_data[Const.VOLTAGE]
        temperature = cell_data[Const.TEMPERATURE]
        aht = cell_data[Const.AHT]

        # CCM
        q_c = cell_cycle_metrics[Const.CHARGE_CAPACITY]
        q_d = cell_cycle_metrics[Const.DISCHARGE_CAPACITY]
        v_min = cell_cycle_metrics[Const.MIN_CYCLE_VOLTAGE]
        v_max = cell_cycle_metrics[Const.MAX_CYCLE_VOLTAGE]
        temperature_min = cell_cycle_metrics[Const.MIN_CYCLE_TEMP]
        temperature_max = cell_cycle_metrics[Const.MAX_CYCLE_TEMP]
        exp_min = cell_cycle_metrics[Const.MIN_CYCLE_EXPANSION_UM]
        exp_max = cell_cycle_metrics[Const.MAX_CYCLE_EXPANSION_UM]
        exp_rev = cell_cycle_metrics[Const.REV_CYCLE_EXPANSION_UM]
        aht_cycle = cell_cycle_metrics[Const.AHT]

        # Index metrics
        cycle_idx = cell_data[cell_data[Const.CYCLE_IDC]].index
        capacity_check_idx = cell_data[cell_data[Const.CAPACITY_CHECK_IDC]].index
        capacity_check_in_cycle_idx = cell_cycle_metrics[cell_cycle_metrics[Const.CAPACITY_CHECK_IDC]].index

        logger.info("Plotting cycle metrics AhT: " + cell_name)

        # Setup plot 
        fig, axes = plt.subplots(3,4,figsize=(12,6), sharex=True)

        # Plot current 
        ax0 = axes.flat[0]
        ax0.plot(aht[0::downsample], i[0::downsample], zorder=1)
        ax0.scatter(aht[cycle_idx], i[cycle_idx], marker = "x", c = "m", zorder=2)
        ax0.scatter(aht[capacity_check_idx], i[capacity_check_idx], marker = "*", c = "r", zorder=3)
        ax0.set_ylabel("Current[A]")
        ax0.grid()

        # Plot voltage 
        ax1 = axes.flat[1]
        ax1.plot(aht[0::downsample], v[0::downsample], zorder=1)
        ax1.scatter(aht[cycle_idx], v[cycle_idx], marker = "x", c = "m", zorder=2)
        ax1.scatter(aht[capacity_check_idx], v[capacity_check_idx], marker = "*", c = "r", zorder=3)
        ax1.set_ylabel("Voltage [V]")
        ax1.grid()

        # Plot temperature
        ax2 = axes.flat[2]
        ax2.plot(aht[0::downsample], temperature[0::downsample], zorder=1)
        ax2.scatter(aht[capacity_check_idx], temperature[capacity_check_idx], marker = "*", c = "r", zorder=3)
        ax2.set_ylabel("Temp [degC]")
        ax2.grid()

        # Plot capacity 
        ax8 = axes.flat[8]
        ax8.scatter(aht_cycle,q_c, marker = "x", c = "g")
        ax8.scatter(aht_cycle,q_d, facecolors='none', edgecolors='c')
        ax8.scatter(aht[capacity_check_idx], q_c[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax8.scatter(aht[capacity_check_idx], q_d[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=4)
        ax8.set_ylabel("Apparent \n capacity [A.h]")
        ax8.grid()

        # Plot min/max voltage 
        ax5 = axes.flat[5]
        ax5.scatter(aht_cycle,v_max)
        ax5.scatter(aht[capacity_check_idx], v_max[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax5.set_ylabel("Max Voltage [V]")
        ax5.grid()

        ax9 = axes.flat[9]
        ax9.scatter(aht_cycle,v_min)
        ax9.scatter(aht[capacity_check_idx], v_min[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax9.set_ylabel("Min Voltage [V]")
        ax9.grid()
        ax9.set_xlabel("Ah Throughput [A.h]")

        # Plot min/max temperature
        ax6 = axes.flat[6]
        ax6.scatter(aht_cycle, temperature_max)   
        ax6.scatter(aht[capacity_check_idx], temperature_max[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax6.set_ylabel("Max Temp [degC]")
        ax6.grid()

        ax10 = axes.flat[10]
        ax10.scatter(aht_cycle, temperature_min) 
        ax10.scatter(aht[capacity_check_idx], temperature_min[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax10.set_ylabel("Min Temp [degC]")
        ax10.grid()
        ax10.set_xlabel("Ah Throughput [A.h]")

        # Plot min/max/rev expansion 
        ax7 = axes.flat[7]
        ax7.scatter(aht_cycle, exp_max)
        ax7.scatter(aht_cycle, exp_min)
        ax7.scatter(aht[capacity_check_idx], exp_max[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax7.scatter(aht[capacity_check_idx], exp_min[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax7.set_ylabel("Max/ Min Exp [-]")
        ax7.grid()
            
        ax11 = axes.flat[11]
        ax11.scatter(aht_cycle, exp_rev)
        ax11.scatter(aht[capacity_check_idx], exp_rev[capacity_check_in_cycle_idx], marker = "*", c = "r", zorder=3)
        ax11.set_ylabel("Rev Exp [um]")
        ax11.set_xlabel('Ah Throughput')
        ax11.grid()

        fig.autofmt_xdate()
        fig.suptitle("Cell: " + cell_name)
        fig.tight_layout()
        return fig

    def downsample_data(self, t, i, v, dv=2e-3, di=0.1, dt=100):
        if (len(t) > 1000):
            dert = np.maximum(0.1, np.diff(t, prepend = 0))
            deriv_v = savgol_filter(v, 20, 3, deriv = 1) / dert # probably need to update this if the sampling rate is too slow.

            dv_changes = np.abs(deriv_v) > dv
            di_changes = (np.abs(np.diff(i, prepend = 0) / dert) > di) + (np.abs(np.diff(i, append=0) / np.maximum(0.1, np.diff(t, append=0))) > di)
            dt_changes = t < 0
            tlast=0
            for j in range(len(t)):
                if(t[j] >= tlast + dt):
                    tlast = t[j]
                    dt_changes[j] = True
            index=dt_changes + dv_changes + di_changes
        else:
            index=range(len(t))
        t_ds = t[index]
        i_ds = i[index]
        v_ds = v[index]
        return t_ds, i_ds, v_ds, index