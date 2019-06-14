#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 11:56am 2019

Plotting hardness ratio, or color diagrams

Updated on Mon Jun 3 - Added name_par_list for NICERsoft segments

"""
from __future__ import division, print_function
from astropy.io import fits
import numpy as np
import Lv0_dirs,Lv0_call_eventcl,Lv0_call_nicersoft_eventcl
import Lv1_data_bin
import Lv2_sources,Lv2_mkdir,Lv2_lc
from scipy import stats
import matplotlib.pyplot as plt
import os

Lv0_dirs.global_par() #obtaining the global parameters

def soft_counts(E_bound,pi_data):
    """
    Will get an array of PI values from the data, where each entry = 1 count.
    So construct an array of ones of equal length, then where E >= E_bound, set to 0.
    This will give an array where 0 = harder X-rays, 1 = softer X-rays, so when
    doing the binning, will get just soft counts.

    E_bound - boundary energy considered (in keV)
    pi_data - array of PI values
    """
    if E_bound < 0 or E_bound > 20:
        raise ValueError("Your E_bound is <0 keV or >20keV - check your input!")
#    if len(times) != len(pi_data):
#        raise ValueError("The time array and PI array are of different lengths. Investigate!")

    counts = np.ones(len(pi_data))
    PI_bound = E_bound*1000/10 #get the cut-off in terms of PI; cutoff is in keV!
    #we do assume that there will be NO bins in which you get ZERO counts

    np.place(counts,pi_data>=PI_bound,0) #get the counts for soft photons

    return counts

def hard_counts(E_bound,pi_data):
    """
    Will get an array of PI values from the data, where each entry = 1 count.
    So construct an array of ones of equal length, then where E < E_bound, set to 0.
    This will give an array where 0 = harder X-rays, 1 = softer X-rays, so when
    doing the binning, will get just soft counts.

    E_bound - boundary energy considered (in keV)
    pi_data - array of PI values
    """
    if E_bound < 0 or E_bound > 20:
        raise ValueError("Your E_bound is <0 keV or >20keV - check your input!")
#    if len(times) != len(pi_data):
#        raise ValueError("The time array and PI array are of different lengths. Investigate!")

    counts = np.ones(len(pi_data))
    PI_bound = E_bound*1000/10 #get the cut-off in terms of PI; cutoff is in keV!
    #we do assume that there will be NO bins in which you get ZERO counts

    np.place(counts,pi_data<PI_bound,0) #get the counts for hard photons

    return counts

def get_color(obsid,bary,name_par_list,par_list,E_bound,tbin_size):
    """
    Calculating the color - hard/soft and (hard-soft)/(hard+soft)

    obsid - Observation ID of the object of interest (10-digit str)
    bary - Whether the data is barycentered. True/False
    name_par_list - list of parameters specifying parameters like GTI number and/or energy range
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    E_bound - boundary energy considered (in keV)
    tbin_size - the size of the time bins (in seconds!)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!

    name_par_list should be [GTI_true,E_true,GTIno,segment_length,PI1,PI2]
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if bary != True and bary != False:
        raise ValueError("bary should either be True or False!")
    if type(name_par_list) != list and type(name_par_list) != np.ndarray:
        raise TypeError("name_par_list should either be a list or an array!")
    if len(name_par_list) != 6:
        raise ValueError("There seems to be fewer or more values in the list/array than there should be! You should have [GTI_true, E_true, GTIno, segment length, PI1, PI2]")
    if 'TIME' not in par_list:
        raise ValueError("You should have 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")

    if all(name_par_list[i] == '' for i in range(len(name_par_list))):
        data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    else:
        data_dict = Lv0_call_nicersoft_eventcl.get_eventcl(obsid,name_par_list,par_list)

    pi_data = data_dict['PI']
    soft = soft_counts(E_bound,pi_data)

    #reobtain the data, for some reason, "np.place" is a global effect...
    if all(name_par_list[i] == '' for i in range(len(name_par_list))):
        data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    else:
        data_dict = Lv0_call_nicersoft_eventcl.get_eventcl(obsid,name_par_list,par_list)

    pi_data = data_dict['PI']
    hard = hard_counts(E_bound,pi_data)

    times = data_dict['TIME']

    if len(soft) != len(hard):
        raise ValueError("Length of soft and hard array is not the same for some reason!")

    shifted_t = times - times[0]
    t_bins = np.linspace(0,int(shifted_t[-1]),int(shifted_t[-1])*1/tbin_size+1)
    sum_soft, bin_edges_soft, binnumber_soft = stats.binned_statistic(shifted_t,soft,statistic='sum',bins=t_bins)
    sum_hard, bin_edges_hard, binnumber_hard = stats.binned_statistic(shifted_t,hard,statistic='sum',bins=t_bins)
    np.place(sum_soft,sum_soft==0,1) #so that you get 0/1 instead

    color = sum_hard/sum_soft
    color_diff = (sum_hard-sum_soft)/(sum_soft+sum_hard)

    return t_bins,color,color_diff

#a,b,c = get_color('0034070101',True,[True,True,1,100,300,800],['TIME','PI'],3,1)
#plt.figure(1)
#plt.plot(a[:-1],b)
#plt.figure(2)
#plt.plot(a[:-1],c)
#plt.show()

def get_color_t(obsid,bary,name_par_list,par_list,E_bound,tbin_size,t1,t2):
    """
    Calculating the color - hard/soft and (hard-soft)/(hard+soft)

    obsid - Observation ID of the object of interest (10-digit str)
    bary - Whether the data is barycentered. True/False
    name_par_list - list of parameters specifying parameters like GTI number and/or energy range
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    E_bound - boundary energy considered (in keV)
    tbin_size - the size of the time bins (in seconds!)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    t1 - lower time boundary
    t2 - upper time boundary

    name_par_list should be [GTI_true,E_true,GTIno,segment_length,PI1,PI2]
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if bary != True and bary != False:
        raise ValueError("bary should either be True or False!")
    if type(name_par_list) != list and type(name_par_list) != np.ndarray:
        raise TypeError("name_par_list should either be a list or an array!")
    if len(name_par_list) != 6:
        raise ValueError("There seems to be fewer or more values in the list/array than there should be! You should have [GTI_true, E_true, GTIno, segment length, PI1, PI2]")
    if 'TIME' not in par_list:
        raise ValueError("You should have 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")

    if all(name_par_list[i] == '' for i in range(len(name_par_list))):
        data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    else:
        data_dict = Lv0_call_nicersoft_eventcl.get_eventcl(obsid,name_par_list,par_list)

    pi_data = data_dict['PI']
    soft = soft_counts(E_bound,pi_data)

    #reobtain the data, for some reason, "np.place" is a global effect...
    if all(name_par_list[i] == '' for i in range(len(name_par_list))):
        data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    else:
        data_dict = Lv0_call_nicersoft_eventcl.get_eventcl(obsid,name_par_list,par_list)

    pi_data = data_dict['PI']
    hard = hard_counts(E_bound,pi_data)

    times = data_dict['TIME']
    shifted_t = times-times[0]
    truncated_t = shifted_t[(shifted_t>=t1)&(shifted_t<=t2)]
    truncated_soft = soft[(shifted_t>=t1)&(shifted_t<=t2)]
    truncated_hard = hard[(shifted_t>=t1)&(shifted_t<=t2)]

    if len(truncated_soft) != len(truncated_hard):
        raise ValueError("Length of truncated soft and hard arrays are not the same for some reason!")

    startt = int(t1)
    endt = int(t2)
    t_bins = np.linspace(startt,endt,(endt-startt)*1/tbin_size+1)
    sum_soft, bin_edges_soft, binnumber_soft = stats.binned_statistic(shifted_t,soft,statistic='sum',bins=t_bins)
    sum_hard, bin_edges_hard, binnumber_hard = stats.binned_statistic(shifted_t,hard,statistic='sum',bins=t_bins)
    np.place(sum_soft,sum_soft==0,1) #so that you get 0/1 instead

    color = sum_hard/sum_soft
    color_diff = (sum_hard-sum_soft)/(sum_soft+sum_hard)

    return t_bins,color,color_diff

#a,b,c = get_color_t('0034070101',True,[True,True,1,100,300,800],['TIME','PI'],3,1,0,100)
#plt.figure(1)
#plt.plot(a[:-1],b)
#plt.figure(2)
#plt.plot(a[:-1],c)
#plt.show()

def plotting(obsid,bary,name_par_list,par_list,E_bound,tbin_size,mode):
    """
    Plotting the hardness ratio/color diagrams.

    t_bins,color,color_diff = get_color(obsid,bary,name_par_list,par_list,E_bound,tbin_size)

    obsid - Observation ID of the object of interest (10-digit str)
    bary - Whether the data is barycentered. True/False
    name_par_list - list of parameters specifying parameters like GTI number and/or energy range
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    E_bound - boundary energy considered (in keV)
    tbin_size - the size of the time bins (in seconds!)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    mode - whether we want to show or save the plot.

    name_par_list should be [GTI_true,E_true,GTIno,segment_length,PI1,PI2]
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if bary != True and bary != False:
        raise ValueError("bary should either be True or False!")
    if type(name_par_list) != list and type(name_par_list) != np.ndarray:
        raise TypeError("name_par_list should either be a list or an array!")
    if len(name_par_list) != 6:
        raise ValueError("There seems to be fewer or more values in the list/array than there should be! You should have [GTI_true, E_true, GTIno, segment length, PI1, PI2]")
    if 'TIME' not in par_list:
        raise ValueError("You should have 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")
    if mode != 'show' and mode != 'save':
        raise ValueError("Mode should either be 'show' or 'save'!")

    #### FOR LIGHT CURVE
    if all(name_par_list[i] == '' for i in range(len(name_par_list))):
        data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)
    else:
        data_dict = Lv0_call_nicersoft_eventcl.get_eventcl(obsid,name_par_list,par_list)

    data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)

    times = data_dict['TIME']
    counts = np.ones(len(times))

    shifted_t = times-times[0]
    tbins_lc = np.linspace(0,int(shifted_t[-1]),int(shifted_t[-1])*1/tbin_size+1)
    lc, bin_edges, binnumber = stats.binned_statistic(shifted_t,counts,statistic='sum',bins=tbins_lc) #binning the time values in the data

    ############################################################################
    obj_name = Lv2_sources.obsid_to_obj(obsid)

    tbins,color,color_diff = get_color(obsid,bary,name_par_list,par_list,E_bound,tbin_size)

    fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex=True,figsize=(10,8))
    fig.suptitle('Light curve + color diagram for ' + obj_name + ', ObsID ' + str(obsid) + '\n for whole time interval' + '\n Boundary energy: ' + str(E_bound) + ' keV', fontsize=12)

    ax1.plot(tbins_lc[:-1],lc,'k')
    ax1.set_ylabel('Count/'+str(tbin_size)+'s',fontsize=12)

    ax2.plot(tbins[:-1],color,'b')
    ax2.set_ylabel('H/S',fontsize=12)

    ax3.plot(tbins[:-1],color_diff,'r')
    ax3.set_xlabel('Time (s)',fontsize=12)
    ax3.set_ylabel('(H-S)/(H+S)',fontsize=12)

    plt.subplots_adjust(hspace=0.2)

    if mode == 'show':
        plt.show()

    elif mode == 'save':
        if all(name_par_list[i] == '' for i in range(len(name_par_list))):
            dir = Lv0_dirs.BASE_DIR+'outputs/' + obsid + '/co/'
            if bary == True:
                filename = dir + obsid + '_bary_bin' + str(tbin_size) + 's.pdf'
            elif bary == False:
                filename = dir + obsid + '_bin' + str(tbin_size) + 's.pdf'
            Lv2_mkdir.makedir(dir)
            plt.savefig(filename,dpi=900)
            plt.close()
        else:
            dir = Lv0_dirs.NICERSOFT_DATADIR+obsid+'_pipe/outputs/co/'
            filename = dir + obsid + '_nicersoft_bin' + str(tbin_size) + 's.pdf'
            Lv2_mkdir.makedir(dir)
            plt.savefig(filename,dpi=900)
            plt.close()

#plotting('0034070101',True,[True,True,1,100,300,800],['TIME','PI'],3,1,'show')

def plotting_t(obsid,bary,name_par_list,par_list,E_bound,tbin_size,t1,t2,mode):
    """
    Plotting the hardness ratio/color diagrams.

    t_bins,color,color_diff = get_color_t(obsid,bary,par_list,E_bound,tbin_size)

    obsid - Observation ID of the object of interest (10-digit str)
    bary - Whether the data is barycentered. True/False
    name_par_list - list of parameters specifying parameters like GTI number and/or energy range
    par_list - A list of parameters we'd like to extract from the FITS file
    (e.g., from eventcl, PI_FAST, TIME, PI,)
    E_bound - boundary energy considered (in keV)
    tbin_size - the size of the time bins (in seconds!)
    >> e.g., tbin_size = 2 means bin by 2s
    >> e.g., tbin_size = 0.05 means bin by 0.05s!
    t1 - lower time boundary
    t2 - upper time boundary
    mode - whether we want to show or save the plot.

    name_par_list should be [GTI_true,E_true,GTIno,segment_length,PI1,PI2]
    """
    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")
    if bary != True and bary != False:
        raise ValueError("bary should either be True or False!")
    if type(name_par_list) != list and type(name_par_list) != np.ndarray:
        raise TypeError("name_par_list should either be a list or an array!")
    if len(name_par_list) != 6:
        raise ValueError("There seems to be fewer or more values in the list/array than there should be! You should have [GTI_true, E_true, GTIno, segment length, PI1, PI2]")
    if 'TIME' not in par_list:
        raise ValueError("You should have 'TIME' in the parameter list!")
    if type(par_list) != list and type(par_list) != np.ndarray:
        raise TypeError("par_list should either be a list or an array!")
    if mode != 'show' and mode != 'save':
        raise ValueError("Mode should either be 'show' or 'save'!")

    #### FOR LIGHT CURVE

    truncated_t, truncated_counts = Lv1_data_bin.binning_t(obsid,bary,name_par_list,par_list,tbin_size,t1,t2)

    obj_name = Lv2_sources.obsid_to_obj(obsid)
    tbins,color,color_diff = get_color_t(obsid,bary,name_par_list,par_list,E_bound,tbin_size,t1,t2)

    fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex=True,figsize=(10,8))
    fig.suptitle('Color diagram for ' + obj_name + ', ObsID ' + str(obsid) + '\n for time interval: ' + str(t1) + 's-'+str(t2)+'s'+ '\n Boundary energy: ' + str(E_bound) + ' keV', fontsize=12)

    ax1.plot(truncated_t[:-1],truncated_counts,'k')
    ax1.set_ylabel('Count/'+str(tbin_size)+'s',fontsize=12)

    ax2.plot(tbins[:-1],color,'b')
    ax2.set_ylabel('Hard/Soft',fontsize=12)

    ax3.plot(tbins[:-1],color_diff,'r')
    ax3.set_ylabel('(Hard-Soft)/(Hard+Soft)',fontsize=12)

    plt.subplots_adjust(hspace=0.2)

    if mode == 'show':
        plt.show()

    elif mode == 'save':
        if all(name_par_list[i] == '' for i in range(len(name_par_list))):
            dir = Lv0_dirs.BASE_DIR+'outputs/' + obsid + '/lc/'
            if bary == True:
                filename = dir + obsid + '_bary_bin' + str(tbin_size) + 's_'+str(t1)+'s-'+str(t2)+'s.pdf'
            elif bary == False:
                filename = dir + obsid + '_bin' + str(tbin_size) + 's_'+str(t1)+'s-'+str(t2)+'s.pdf'
            Lv2_mkdir.makedir(dir)
            plt.savefig(filename,dpi=900)
            plt.close()
        else:
            dir = Lv0_dirs.NICERSOFT_DATADIR+obsid+'_pipe/outputs/lc/'
            filename = dir + obsid + '_nicersoft_bin' + str(tbin_size) + 's_'+str(t1)+'s-'+str(t2)+'s.pdf'
            Lv2_mkdir.makedir(dir)
            plt.savefig(filename,dpi=900)
            plt.close()

#plotting('0034070101',True,['PI','TIME','PI_FAST'],2.7,1,'show')
#plotting_t('1034070104',True,['PI','TIME','PI_FAST'],2.7,1,11113,11945,'show')
#plotting_t('0034070101',True,[True,True,1,100,300,800],['PI','TIME','PI_FAST'],2.7,1,0,99,'show')
