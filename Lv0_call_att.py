#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tues Jan 8 11:51am 2019

Opening FITS files and obtaining data from the .att files

"""
from __future__ import division,print_function
from astropy.io import fits
import Lv0_dirs
import numpy as np

Lv0_dirs.global_par() #obtaining the global parameters

def open_fits(obsid):
    """
    Opening the FITS file for the attitude file

    obsid - Observation ID of the object of interest (10-digit str)
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")

    event = Lv0_dirs.NICER_DATADIR + obsid + '/auxil/ni' + obsid + '.att'
    event = fits.open(event)
    #see event.info() for each card
    #event[1].header for events; event[2].header for GTIs

    return event

def get_att(obsid,par_list):
    """
    Getting data from the FITS files, e.g., PI_FAST, TIME, PI, PI_RATIO, FLAGS

    obsid - Observation ID of the object of interest (10-digit str)
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI)
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")

    event = open_fits(obsid)
    data_dict = {}

    for i in range(len(par_list)):
        data_dict[par_list[i]] = event[1].data[par_list[i]]

    return data_dict

if __name__ == "__main__":
    print(get_att('0034070101',['TIME','QPARAM','STATE']))

# Variables (TTYPE) from the FITS file headers that I printed

# att

# TIME, QPARAM, STATE, MODE, SUBMODE_AZ, SUBMODE_EL, ST_VALID, QUATSRC, FINEMEAS

# instatt

# TIME, QPARAM, STATE, MODE, SUBMODE_AZ, SUBMODE_EL, ST_VALID, QUATSRC, FINEMEAS
