#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tues Jan 8 2:11pm 2019

Extracting the GTIs from the FITS files. Use the event_cl files.

"""
from __future__ import division, print_function
from astropy.io import fits
import numpy as np
import Lv0_dirs,Lv1_data_filter
from scipy import stats
import matplotlib.pyplot as plt

def binning_t(eventfile,par_list,tbin_size,t1,t2):
    """
    Binning routine for when I truncate the data by JUST time interval.
    Got to make sure I have TIME and PI called!

    eventfile - path to the event file. Will extract ObsID from this for the NICER files.
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    tbin_size - the size of the time bins (in seconds!)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    t1 - lower time boundary
    t2 - upper time boundary
    """
    if type(eventfile) != str:
        raise TypeError("eventfile should be a string!")
    if type(tbin_size) != int and type(tbin_size) != np.float:
        raise TypeError("tbin_size should be a float or integer!")
    if 'PI' and 'TIME' not in par_list:
        raise ValueError("You should have BOTH 'PI' and 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")

    truncated_t = Lv1_data_filter.filter_time(eventfile,par_list,t1,t2)
    counts = np.ones(len(truncated_t))
    startt = int(t1)
    endt = int(t2)

    t_bins = np.linspace(startt,endt,(endt-startt)*1/tbin_size+1) #getting an array of time values for the bins
    summed_data, bin_edges, binnumber = stats.binned_statistic(truncated_t,counts,statistic='sum',bins=t_bins) #binning the counts in the data

    print("The data is binned by " + str(tbin_size) + 's')

    return t_bins, summed_data

def binning_E(eventfile,par_list,tbin_size,Ebin_size,E1,E2):
    """
    Binning routine for when I truncate the data by JUST energy range.
    Got to make sure I have TIME and PI called!

    eventfile - path to the event file. Will extract ObsID from this for the NICER files.
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    tbin_size - the size of the time bins (in seconds!)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    Ebin_size - the size of the energy bins (in keV!)
    >> e.g., Ebin_size = 0.1 means bin by 0.1keV
    >> e.g., Ebin_size = 0.05 means bin by 0.05keV
    E1 - lower energy boundary
    E2 - upper energy boundary
    """
    if type(eventfile) != str:
        raise TypeError("eventfile should be a string!")
    if type(tbin_size) != int and type(tbin_size) != np.float:
        raise TypeError("tbin_size should be a float or integer!")
    if type(Ebin_size) != int and type(Ebin_size) != np.float:
        raise TypeError("Ebin_size should be a float or integer!")
    if 'PI' and 'TIME' not in par_list:
        raise ValueError("You should have BOTH 'PI' and 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")

    truncated_t, truncated_E = Lv1_data_filter.filter_energy(eventfile,par_list,E1,E2)
    counts = np.ones(len(truncated_t))
    startt = int(truncated_t[0])
    endt = np.ceil(truncated_t[-1])

    t_bins = np.linspace(startt,endt,(endt-startt)*1/tbin_size+1) #getting an array of time values for the bins
    summed_data_t, bin_edges, binnumber = stats.binned_statistic(truncated_t,counts,statistic='sum',bins=t_bins) #binning the time values in the data

    if E1 < 1: #if less than 1keV, the binning for 0.3-1keV is slightly different.
        E_bins = np.linspace(E1,E2,(E2-E1)*1/Ebin_size+2) #getting an array of energy values for the bins
    else:
        E_bins = np.linspace(E1,E2,(E2-E1)*1/Ebin_size+1) #getting an array of energy values for the bins
    summed_data_E, bin_edges, binnumber = stats.binned_statistic(truncated_E,counts,statistic='sum',bins=E_bins) #binning the energy values in the data

    print("The data is binned by " + str(tbin_size) + 's, and ' + str(Ebin_size) + 'keV')

    return t_bins, summed_data_t, E_bins, summed_data_E

def binning_tE(eventfile,par_list,tbin_size,Ebin_size,t1,t2,E1,E2):
    """
    Binning routine for when I truncated the data by BOTH time interval AND energy range.
    Got to make sure I have TIME and PI called!

    eventfile - path to the event file. Will extract ObsID from this for the NICER files.
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    tbin_size - the size of the time bins (in seconds!)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    Ebin_size - the size of the energy bins (in keV!)
    >> e.g., Ebin_size = 0.1 means bin by 0.1keV
    >> e.g., Ebin_size = 0.05 means bin by 0.05keV
    t1 - lower time boundary
    t2 - upper time boundary
    E1 - lower energy boundary
    E2 - upper energy boundary
    """
    if type(eventfile) != str:
        raise TypeError("eventfile should be a string!")
    if type(tbin_size) != int and type(tbin_size) != np.float:
        raise TypeError("tbin_size should be a float or integer!")
    if type(Ebin_size) != int and type(Ebin_size) != np.float:
        raise TypeError("Ebin_size should be a float or integer!")
    if 'PI' and 'TIME' not in par_list:
        raise ValueError("You should have BOTH 'PI' and 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")
    if t2<t1:
        raise ValueError("t2 should be greater than t1!")
    if E2<E1:
        raise ValueError("E2 should be greater than E1!")

    truncated_t, truncated_E = Lv1_data_filter.filter_data(eventfile,par_list,t1,t2,E1,E2)
    counts = np.ones(len(truncated_t))
    startt = int(t1)
    endt = int(t2)

    t_bins = np.linspace(startt,endt,(endt-startt)*1/tbin_size+1) #getting an array of time values for the bins
    summed_data_t, bin_edges, binnumber = stats.binned_statistic(truncated_t,counts,statistic='sum',bins=t_bins) #binning the time values in the data

    if E1 < 1: #if less than 1keV, the binning for 0.3-1keV is slightly different.
        E_bins = np.linspace(E1,E2,(E2-E1)*1/Ebin_size+2) #getting an array of energy values for the bins
    else:
        E_bins = np.linspace(E1,E2,(E2-E1)*1/Ebin_size+1) #getting an array of energy values for the bins
    summed_data_E, bin_edges, binnumber = stats.binned_statistic(truncated_E,counts,statistic='sum',bins=E_bins) #binning the energy values in the data

    print("The data is binned by " + str(tbin_size) + 's, and ' + str(Ebin_size) + 'keV')

    return t_bins, summed_data_t, E_bins, summed_data_E

if __name__ == "__main__":
    obsid = '1034070101'
    eventfile = Lv0_dirs.NICER_DATADIR + obsid + '/xti/event_cl/ni' + obsid + '_0mpu7_cl_bary.evt'
    par_list = ['TIME','PI','PI_RATIO']
    t1 = 0
    t2 = 300
    E1 = 0.3
    E2 = 6

    tbin_size = 1
    Ebin_size = 0.05

    tbins,summed_data = binning_t(eventfile,par_list,tbin_size,t1,t2)
    #print(len(tbins),len(summed_data))
    tbins,summed_t_data,Ebins,summed_E_data = binning_E(eventfile,par_list,tbin_size,Ebin_size,E1,E2)
    #print(len(tbins),len(summed_t_data),len(Ebins),len(summed_E_data))
    tbins,summed_t_data,Ebins,summed_E_data = binning_tE(eventfile,par_list,tbin_size,Ebin_size,t1,t2,E1,E2)
    #print(len(tbins),len(summed_t_data),len(Ebins),len(summed_E_data))
