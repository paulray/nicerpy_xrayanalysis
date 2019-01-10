#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thurs Jan 10 10:26am 2019

Filtering out the data based on time interval and/or energy ranges.
When binning by energy range, I could probably choose the count rate.
"""
from __future__ import division, print_function
from astropy.io import fits
import numpy as np
import Lv0_dirs,Lv0_call_eventcl

Lv0_dirs.global_par() #obtaining the global parameters

def filter_time(obsid,bary,par_list,t1,t2):
    """
    Obtain the time stamps that fall in a desired time interval.

    obsid - Observation ID of the object of interest (10-digit str)
    bary - Whether the data is barycentered. True/False
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    t1 - time value for the lower boundary (in s)
    t2 - time value for the upper boundary (in s)
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if bary != True and bary != False:
        raise ValueError("bary should either be True or False!")
    if 'TIME' not in par_list:
        raise ValueError("You should have 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")
    if t2<t1:
        raise ValueError("t2 should be greater than t1!")

    # RECALL THAT PI * 10/1000 = keV

    data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    times = data_dict['TIME'] #extract the timestamps
    shifted_t = times-times[0] #so that we start at t = 0

    t_cut = shifted_t[(shifted_t>=t1)&(shifted_t<=t2)] #only consider timestamps
    #where they fall in a desired time interval. Ignore the counts for now, as I
    #can generate them in Lv1_data_bin with np.ones anyways.

    return t_cut

def filter_energy(obsid,bary,par_list,E1,E2):
    """
    Obtain the time stamps and the corresponding energy value (of the photon)
    in a desired energy range.

    obsid - Observation ID of the object of interest (10-digit str)
    bary - Whether the data is barycentered. True/False
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    E1 - energy value for the lower boundary (in keV)
    E2 - energy value for the upper boundary (in keV)
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if bary != True and bary != False:
        raise ValueError("bary should either be True or False!")
    if 'PI' and 'TIME' not in par_list:
        raise ValueError("You should have BOTH 'PI' and 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")
    if (E1<0) or (E2>20):
        raise ValueError("You're asking for boundaries <0 keV or > 20 keV. Do check!")
    if E2<E1:
        raise ValueError("E2 should be greater than E1!")

    # RECALL THAT PI * 10/1000 = keV

    data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    times = data_dict['TIME'] #extract the timestamps
    PI_data = data_dict['PI'] #extract the energy values
    E_data = PI_data * 10/1000 #convert PI to keV
    shifted_t = times-times[0] #so that we start at t = 0
    counts_data = np.ones(len(PI_data)) #each datum = 1 count

    t_cut = shifted_t[(E_data>=E1)&(E_data<=E2)]
    E_cut = E_data[(E_data>=E1)&(E_data<=E2)]

    return t_cut, E_cut

def filter_data(obsid,bary,par_list,t1,t2,E1,E2):
    """
    Truncate the data such that you get counts in a given time interval and
    energy range.

    obsid - Observation ID of the object of interest (10-digit str)
    bary - Whether the data is barycentered. True/False
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    t1 - time value for the lower boundary (in s)
    t2 - time value for the upper boundary (in s)
    E1 - energy value for the lower boundary (in keV)
    E2 - energy value for the upper boundary (in keV)
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if bary != True and bary != False:
        raise ValueError("bary should either be True or False!")
    if 'PI' and 'TIME' not in par_list:
        raise ValueError("You should have BOTH 'PI' and 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")
    if (E1<0) or (E2>20):
        raise ValueError("You're asking for boundaries <0 keV or >20 keV. Do check!")
    if E2<E1:
        raise ValueError("E2 should be greater than E1!")
    if t2<t1:
        raise ValueError("t2 should be greater than t1!")

    # RECALL THAT PI * 10/1000 = keV

    data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    times = data_dict['TIME'] #extract the timestamps
    PI_data = data_dict['PI'] #extract the energy values
    E_data = PI_data * 10/1000 #convert PI to keV
    shifted_t = times-times[0] #so that we start at t = 0

    truncated_time = shifted_t[(E_data>=E1)&(E_data<=E2)&(shifted_t>=t1)&(shifted_t<=t2)] #truncate the shifted time array by energy values and time interval
    truncated_E = E_data[(E_data>=E1)&(E_data<=E2)&(shifted_t>=t1)&(shifted_t<=t2)] #truncate the energy array by energy values and time interval

    print('Here is what you have truncated by:')
    print("You've constrained the data such that it is with")
    print("Time interval: " + str(t1) + 's to ' + str(t2) + 's')
    print("Energy range: " + str(E1) + 'keV to ' + str(E2) + 'keV.')

    return truncated_time, truncated_E
