#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Jan 5th

@author: masonng


"""
from __future__ import division, print_function
import datetime
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import matplotlib.gridspec as gridspec
import Lv0_dirs,Lv0_call_eventcl,Lv1_data_bin
from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats
from scipy import signal

timestart = time.time()

Lv0_dirs.global_par()

print(datetime.datetime.now())

"""

class Complex:
     def __init__(self, realpart, imagpart):
         self.r = realpart
         self.i = imagpart

x = Complex(4.0,3.0)
print(x.r,x.i)

obsid = '0034070101'
bary = True
par_list = ['PI','TIME','PI_FAST']
tbin_size=1
t1 = 0
t2 = 809

truncated_t, truncated_counts = Lv1_data_bin.binning_t(obsid,bary,par_list,tbin_size,t1,t2)

data_dict = Lv0_call_eventcl.get_eventcl(obsid,bary,par_list)

times = data_dict['TIME']
counts = np.ones(len(times))

shifted_t = times-times[0]
t_bins = np.linspace(0,int(shifted_t[-1]),int(shifted_t[-1])*1/tbin_size+1)
summed_data, bin_edges, binnumber = stats.binned_statistic(shifted_t,counts,statistic='sum',bins=t_bins) #binning the time values in the data

"""

#for i in range(len(counts)):
#    print(i,summed_data[i]-truncated_counts[i])
"""
import Lv0_call_mkf
datadict = Lv0_call_mkf.get_mkf('1034070102',['TIME','ANG_DIST'])
times = datadict['TIME']
shifted_t = times-times[0]
angdist = datadict['ANG_DIST']
plt.plot(shifted_t,angdist)
plt.xlim([0,625])
plt.show()
"""

obsids = ['0034070101','0034070102','0034070103','0034070104','1034070101','1034070102','1034070103','1034070104','1034070105','1034070106']
"""
import Lv0_call_ufa
from scipy.stats import norm
for i in range(len(obsids)):
    plt.figure(1)
    datadict = Lv0_call_ufa.get_ufa(obsids[i],'7',['TIME','PI'])
    pis = datadict['PI']
    times = datadict['TIME']
    pis_trunc = pis[(pis>=5)&(pis<=15)]
    plt.hist(pis_trunc,bins=20,range=(5,15),density=True)
    plt.title(obsids[i],fontsize=15)

    mu,std = norm.fit(pis_trunc)
    print(mu)
    x = np.linspace(5,15,1001)
    p = norm.pdf(x,mu,std)
    plt.plot(x,p,'k')

    plt.show()
"""
#plt.figure(2)
#event = '/Users/masonng/Documents/MIT/Research/ni1034070106_0mpu7_ufa.evt'
#event = fits.open(event)

#pis = event[1].data['PI']
#plt.hist(pis,bins=20,range=(5,15))

workingdir = '/Users/masonng/Documents/MIT/Research/nicer-data/0034070101_test_xsel/xti/event_cl/'
fitsfile = 'trymodel1.fits'
"""
E,c1,c2,c3,c4 = np.loadtxt(workingdir+fitsfile,skiprows=3,usecols=(0,1,2,3,4),unpack=True)
plt.semilogy(E,c2,'r-')
plt.semilogy(E,c3,'k-')
plt.semilogy(E,c4,'c-')
plt.ylim([1e-4,1])

plt.show()
"""
"""
import xspec
tryfile = '/Users/masonng/Documents/MIT/Research/nicer-data/0034070101/xti/event_cl/0034070101_spec.pi'
#tryfile = '0034070101_spec.pi'
s = xspec.Spectrum(tryfile)
"""

"""
renorm = '/Users/masonng/Documents/MIT/Research/nicer-data/crabcor.dat'
test_spec = '/Users/masonng/Documents/MIT/Research/nicer-data/0034070101/xti/event_cl/0034070101_spec.pi'
test_renormspec = '/Users/masonng/Documents/MIT/Research/nicer-data/0034070101/xti/event_cl/0034070101_renormspec.pi'

event = fits.open(test_spec)
event_renorm = fits.open(test_renormspec)

eventchan = event[1].data['CHANNEL']*10/1000
eventcount = event[1].data['COUNTS']

chan,ratio = np.loadtxt(renorm,usecols=(0,1),unpack=True)

renormchan = event_renorm[1].data['CHANNEL']*10/1000
renormcount = event_renorm[1].data['COUNTS']

#for i in range(100,500):
#    print(chan[i],eventcount[i],ratio[i],renormcount[i])

#plt.plot(chan,ratio)
#plt.plot(eventchan[100:500],eventcount[100:500],'rx')
#plt.plot(renormchan[100:500],renormcount[100:500],'bx')
#plt.plot(eventchan,eventcount,'rx')
#plt.plot(renormchan,renormcount,'bx')
#plt.legend(('Original','Renorm'),loc='best')
#plt.show()
"""

"""
event = Lv0_dirs.NICER_DATADIR + '0034070101/xti/event_cl/0034070101_truncated.pi'
event = fits.open(event)

counts = event[1].data['COUNTS']
print(sum(counts))

datadict = Lv0_call_eventcl.get_eventcl('0034070101',True,['PI','PI_FAST','TIME'])
times = datadict['TIME']
pi = datadict['PI']
T = times[-1]-times[0]
counts = np.ones(len(times))
print(min(pi),max(pi))
print(sum(counts))
print(sum(counts)/T)
print(T)
"""

"""
datadict = Lv0_call_eventcl.get_eventcl('1034070104',True,['PI','PI_FAST','TIME','EVENT_FLAGS'])
times = datadict['TIME']
flags = datadict['EVENT_FLAGS']
counts = np.ones(len(times))

shifted_t = times-times[0]
times_trunc = times[(shifted_t>=11700)&(shifted_t<=11900)] #55281
flags_trunc = flags[(shifted_t>=11700)&(shifted_t<=11900)]
t_bins = np.linspace(0,int(shifted_t[-1]),int(shifted_t[-1]+1))
#print(len(times_trunc)) #55281
#for i in range(23200,23500):
#    print(shifted_t[i],flags_trunc[i])

binned_counts, edges, binno = stats.binned_statistic(shifted_t,counts,statistic='sum',bins=t_bins)
#plt.plot(t_bins[:-1],binned_counts,'r-')
#plt.show()
"""


x = [np.linspace(0,100,10001),np.linspace(100,200,10001),np.linspace(200,300,10001),np.linspace(300,400,10001),np.linspace(400,500,10001),np.linspace(500,600,10001)]
y = [4*x[0]+34,4*x[1]+34,4*x[2]+34,4*x[3]+34,4*x[4]+34,4*x[5]+34]
"""
fig,axes = plt.subplots(1,1,sharex=True)
axes[0,0].plot(x,y)

plt.show()
"""

"""
#Creates four polar axes, and accesses them through the returned array
fig,(p10,p20,p30,p40,p50,p60) = plt.subplots(6,1,figsize=(12.8,4.0))
gs = gridspec.GridSpec(6,1)
p10 = plt.subplot(gs[0])
p20 = plt.subplot(gs[1])
p30 = plt.subplot(gs[2])
p40 = plt.subplot(gs[3])
p50 = plt.subplot(gs[4])
p60 = plt.subplot(gs[5])
plotting = [p10,p20,p30,p40,p50,p60]

for i in range(6):
    plt.subplot(gs[i]).plot(x[i],y[i])

plt.show()

"""

"""
import subprocess
import os
#subprocess.check_output(['/Users/masonng/Documents/MIT/Research/Nicer-Logistics/heasoft-6.25/x86_64-apple-darwin17.7.0/headas-init.sh'],shell=True)
#subprocess.call(['/bin/bash','-i','-c','heainit','nicerversion'],shell=True)
subprocess.check_call('nicerversion')#,env=os.environ)
timeend = time.time()
"""

"""
import subprocess
from astropy.io.fits import getdata,update

#event = '/Volumes/Samsung_T5/NICERsoft_outputs/1034090111_pipe/GTI_1000s/GTI1_breakup/ni1034090111_nicersoft_bary_GTI1_1000s.evt'
#newevent = '/Volumes/Samsung_T5/NICERsoft_outputs/1034090111_pipe/GTI_1000s/GTI1_breakup/ni1034090111_nicersoft_bary_GTI1_1000s_short.evt'
#subprocess.check_call(['cp',event,newevent])
#new_list = np.rec.array([(0,1000)])
event = '/Volumes/Samsung_T5/NICERsoft_outputs/1034090111_pipe/ni1034090111_nicersoft_bary_stitched.evt'
data,hdr = getdata(event,1,header=True)
times = data['TIME']
counts = np.ones(len(times))
shifted_t = times-times[0]
t_bins = np.linspace(0,shifted_t[-1],len(shifted_t)+1)
summed_data, bin_edges, binnumber = stats.binned_statistic(shifted_t,counts,statistic='sum',bins=t_bins)

plt.plot(t_bins[:-1],summed_data,'rx')
plt.show()
#update(newevent,new_list,2,header=hdr)
"""
#header = fits.Header()

"""
eventfile = '/Volumes/Samsung_T5/NICERsoft_outputs/1034090111_pipe_old/GTI_1000s/ni1034090111_nicersoft_bary_GTI1_1000s.dat'
contents = np.fromfile(eventfile,dtype='<f',count=-1)

print(len(contents),type(contents))
print(np.max(contents))

"""

"""
import subprocess
subprocess.check_call(['nicerversion'])
import sh
import glob

dir = '/Volumes/Samsung_T5/1060060127/xti/hk/'
hk_files = glob.glob(dir+'*.gz')

for i in range(len(hk_files)):
    sh.gunzip(hk_files[i])

#subprocess.check_call(['scp', '-r', 'masonng@ciri:/nfs/ciri/nicer/decrypted/1060060127','/Volumes/Samsung_T5'])
#subprocess.check_call(['gunzip','/Volumes/Samsung_T5/1060060127/xti/hk/*.gz'])
#subprocess.check_call(['psrpipe.py'])
#subprocess.check_call(['barycorr'])
#subprocess.check_call(['nicerfits2presto.py'])
#subprocess.check_call(['realfft'])
#subprocess.check_call(['accelsearch'])
#subprocess.check_call(['prepfold'])
"""

"""
import subprocess

infile = '/Volumes/Samsung_T5/NICERsoft_outputs/1034090111_pipe_old/GTI_1000s/ni1034090111_nicersoft_bary_GTI1_1000s_63.86Hz_Cand.pfd.ps'
outfile = '/Volumes/Samsung_T5/NICERsoft_outputs/1034090111_pipe_old/GTI_1000s/ni1034090111_nicersoft_bary_GTI1_1000s_63.86Hz_Cand.pfd.pdf'
subprocess.check_call(['ps2pdf',infile,outfile])
"""

"""
eventfile = Lv0_dirs.NICERSOFT_DATADIR + '1060060127_pipe/test.dat'
bins = np.fromfile(eventfile,dtype='<f',count=-1)
ts = np.linspace(0,100,200000)
tbins = np.linspace(0,100,101)
sumcounts,bin_edges,binnumber = stats.binned_statistic(ts,bins,statistic='sum',bins=tbins)

plt.plot(tbins[:-1],sumcounts,'r-')
plt.show()
print(len(bins[bins>0])/len(bins)*100)

"""

"""
obsdir = Lv0_dirs.NICERSOFT_DATADIR + '0034070101_pipe/'
test_dat = obsdir + 'test.dat'

bins = np.fromfile(test_dat,dtype='<f',count=-1) #reads the binary file ; converts to little endian, count=-1 means grab everything
bins_with_data = len(bins[bins>0]) #number of bins with data (NOT the ones with averaged count rate!)
average_count_rate = sum(bins)/len(bins)

segment_length = 1000
tbin = 0.00025
print(len(bins))
no_desired_bins = segment_length/tbin #number of desired bins, to go up to the desired segment length
no_padded = int(no_desired_bins-len(bins)) #number of bins *needed* for original segment to have desired segment length
padding = np.ones(no_padded,dtype=np.float32)*average_count_rate #generate the array of (averaged) counts needed to pad the original segment
#padding = np.zeros(no_padded,dtype=np.float32)
#padding = np.zeros(no_padded,dtype=np.float32)
new_bins = np.array(list(bins) + list(padding)) #the new set of bins where it contains the original segment, in addition to the padded bins (with counts = average of original segment)
print(len(new_bins))
new_bins.tofile('test3.dat')

import subprocess
subprocess.check_output(['mv','test3.dat',obsdir])

test3_dat = obsdir + 'test3.dat'
bins = np.fromfile(test3_dat,dtype='<f',count=-1)

print(len(bins))

times = np.linspace(0,len(bins)*tbin,len(bins))
plt.plot(times,bins,'r-')
plt.show()

def pad_binary(obsid,tbin,segment_length):

    To pad the binary file so that it will be as long as the desired segment length.
    The value to pad with for each time bin, is the average count rate in THAT segment!

    obsid - Observation ID of the object of interest (10-digit str)
    tbin - size of the bins in time
    segment_length - length of the individual segments

    if type(obsid) != str:
        raise TypeError("ObsID should be a string!")

    obsdir = Lv0_dirs.NICERSOFT_DATADIR + obsid + '_pipe/'
    dat_files = glob.glob(obsdir+'*.dat')
    for i in range(len(dat_files)):
        bins = np.fromfile(dat_files[i],dtype='<f',count=-1) #reads the binary file ; converts to little endian, count=-1 means grab everything
        bins_with_data = len(bins[bins>0]) #number of bins with data (NOT the ones with averaged count rate!)
        average_count_rate = sum(bins)/len(bins)

        no_desired_bins = segment_length/tbin #number of desired bins, to go up to the desired segment length
        no_padded = int(no_desired_bins-len(bins)) #number of bins *needed* for original segment to have desired segment length
        padding = np.ones(no_padded)*average_count_rate #generate the array of (averaged) counts needed to pad the original segment
        new_bins = list(bins) + list(padding) #the new set of bins where it contains the original segment, in addition to the padded bins (with counts = average of original segment)

        final_dat = open(dat_files[i],"wb")
        final_dat.write(new_bins)

    return
"""

"""
tbin = 0.00025
duty_cycle_bin = 1
gtino = 0
segment_length = 1000

binned_data = np.fromfile('/Volumes/Samsung_T5/NICERsoft_outputs/1034090111_pipe/ni1034090111_nicersoft_bary_GTI'+str(gtino)+'_'+str(segment_length)+'s.dat',dtype='<f',count=-1)
dat_times = np.arange(0,tbin*len(binned_data),tbin)

duty_cycle_times = np.arange(0,tbin*len(binned_data)+tbin,duty_cycle_bin)

summed_data, binedges, binnumber = stats.binned_statistic(dat_times,binned_data,statistic='sum',bins=duty_cycle_times)
print(len(summed_data))
print(len(summed_data[(summed_data[i]!=stats.mode(summed_data))&(sum(summed_data[i:i+5])!=5*stats.mode(summed_data) for i in range(len(summed_data)))&(summed_data>0)]))
print(len(summed_data[(summed_data!=stats.mode(summed_data)[0][0])&(summed_data>0)]))
plt.plot(duty_cycle_times[:-1],summed_data,'rx')
plt.axhline(y=stats.mode(summed_data)[0][0])
plt.show()
"""

# mkgti.py --gtiname testgti.gti 109451762 109451962
# niextract-events /Volumes/Samsung_T5/NICERsoft_outputs/0034070101_pipe/ni0034070101_nicersoft_bary.evt testtrunc.evt timefile=testgti.gti
# nicerfits2presto.py --dt=0.00025 testtrunc.evt

"""
bins = np.fromfile('testtrunc.dat',dtype='<f',count=-1)
print(sum(bins[:800000]))
print(sum(bins[800000:]))
"""

"""
from PyAstronomy.pyasl import foldAt
import matplotlib.pylab as plt
import numpy as np

# Generate some data ...
time = np.random.random(1000) * 100.
flux = 0.05 * np.sin(time*(2.*np.pi/21.5) + 15)
# ... and add some noise
flux += np.random.normal(0, 0.02, len(flux))

# Obtain the phases with respect to some
# reference point (in this case T0=217.4)
phases = foldAt(time, 21.5, T0=217.4)

# Sort with respect to phase
# First, get the order of indices ...
sortIndi = np.argsort(phases)
# ... and, second, rearrange the arrays.
phases = list(phases[sortIndi]) + list(phases[sortIndi]+1)
flux = list(flux[sortIndi])*2

phase_bins = np.linspace(0,2,51)
summed_profile, bin_edges, binnumber = stats.binned_statistic(phases,flux,statistic='sum',bins=phase_bins)

# Plot the result
plt.figure(1)
plt.plot(phases, flux, 'bp')
plt.axvline(x=1,alpha=0.5)
plt.figure(2)
plt.plot(phase_bins[:-1],summed_profile,'r')
plt.show()
"""

"""
#### TESTING semicolons; using multiple commands at once! Need shell=True
import os
import subprocess
#subprocess.check_call(['cd','/Volumes/Samsung_T5/NICERsoft_outputs/testdirha/',';', 'mv','testtest2.txt','renamedYAY.txt',';','cd','..',';', 'mv','testtest1.txt','renamedAGAIN.txt'],shell=True)
subprocess.Popen('cd /Volumes/Samsung_T5/NICERsoft_outputs/testdirha/ ; mv testtest2.txt renamedYAY.txt ; cd .. ; mv testtest1.txt renamedAGAIN.txt',shell=True)
"""

"""
input_filename = '/Volumes/Samsung_T5/NICERsoft_outputs/0034070101_pipe_old/ni0034070101_nicersoft_bary_ACCEL_200'
input_file = open(input_filename,'r').read().split('\n')
print(len(input_file),type(input_file))
a = "             Summed  Coherent  Num        Period          Frequency         FFT 'r'        Freq Deriv       FFT 'z'         Accel                           "
b = "                        Power /          Raw           FFT 'r'          Pred 'r'       FFT 'z'     Pred 'z'      Phase       Centroid     Purity                        "

print(len(a))
print(len(b))
print(input_file[0],len(input_file[0]),input_file[0]==a)
print(input_file[17],len(input_file[17]),input_file[17]==b)
print(np.where(np.array(input_file)==a)[0][0])
print(np.where(np.array(input_file)==b)[0][0])
"""

#import subprocess
#logfile = '/Volumes/Samsung_T5/NICERsoft_outputs/0034070101_pipe_old/logfile.txt'
#log = open(logfile,'a')
#subprocess.Popen('cd /Volumes/Samsung_T5/NICERsoft_outputs/0034070101_pipe_old/ ; prepfold -double -events -noxwin -n 50 -accelcand 1 -accelfile ni0034070101_nicersoft_bary_800-1200_ACCEL_0.cand ni0034070101_nicersoft_bary.events',stdout=log,shell=True)

"""
obsid = '1060060170'
base_folder = '/Volumes/Samsung_T5/NICERsoft_outputs/'+obsid+'_pipe/'
event = base_folder + 'ni'+obsid+'_nicersoft_bary.evt'
event = fits.open(event)
counts = len(event[1].data['TIME'])
gtis = event[2].data
total_gti = sum([ (gtis[i][1] - gtis[i][0]) for i in range(len(gtis))])
print('Number of counts: '+str(counts))
print(total_gti)
print('Exposure time is ' + str(gtis[-1][1]-gtis[0][0]) + ' s')
"""

"""
obsid = '1060060170'
base_folder = '/Volumes/Samsung_T5/NICERsoft_outputs/'+obsid+'_pipe/'
event = base_folder + 'ni'+obsid+'_nicersoft_bary.evt'
event = fits.open(event)
times = event[1].data['TIME']

import binary_psr
timea = binary_psr.binary_psr("/Volumes/Samsung_T5/NICERsoft_outputs/J1231-1411.par").demodulate_TOAs(times)
for i in range(100):
    print(times[i],timea[i])
"""

"""
basefolder = '/Volumes/Samsung_T5/NICERsoft_outputs/1034070104_pipe_old/'
event = basefolder + 'cleanfilt.evt'
event = fits.open(event)
times = event[1].data['TIME']

times_zero = times - times[0]
counts = np.ones(len(times))

tbins = np.linspace(0,len(times_zero),len(times_zero)+1)
summed_counts,binedges,binnumber = stats.binned_statistic(times_zero,counts,statistic='sum',bins=tbins)
plt.plot(tbins[:-1],summed_counts,'r-')
plt.title('Cen X-3 ; ObsID 1034070104',fontsize=12)
plt.xlabel('Elapsed time (s)',fontsize=12)
plt.ylabel('Counts/s',fontsize=12)
plt.show()
"""

### Testing FFT from PRESTO and FFT from manual method
"""
cenx3_data = '/Volumes/Samsung_T5/NICERsoft_outputs/0034070101_pipe/ni0034070101_nicersoft_bary.dat'
cenx3_fft = '/Volumes/Samsung_T5/NICERsoft_outputs/0034070101_pipe/ni0034070101_nicersoft_bary.fft'

raw_data = np.fromfile(cenx3_data,dtype='<f',count=-1)

freqs = np.fft.fftfreq(raw_data.size,0.00025)
N = len(freqs)
use_freqs = freqs[1:int(N/2)]

new_raw_data = raw_data - np.mean(raw_data)
my_fft = np.fft.fft(new_raw_data)
my_ps = 2/sum(raw_data)*np.abs(my_fft)**2
use_my_ps = my_ps[1:int(N/2)]
print(use_my_ps[:5])

fft_data = np.fromfile(cenx3_fft,dtype='complex64',count=-1)
fft_ps = 2/sum(raw_data)*np.abs(fft_data)**2
#fft_ps = signal.detrend(fft_ps,type='constant')
use_fft_ps = fft_ps[1:int(N/2)]
print(use_fft_ps[:5])

print('Mean of my power spectrum: ' + str(np.mean(use_my_ps[use_freqs>10])))
print('Mean of PRESTO power spectrum: ' + str(np.mean(use_fft_ps[use_freqs>10])))

plt.figure(1)
plt.plot(use_freqs,use_my_ps)
plt.figure(2)
plt.plot(use_freqs,use_fft_ps)
plt.show()
"""

"""
test_data = '/Volumes/Samsung_T5/NICERsoft_outputs/1060020113_pipe/ni1060020113_nicersoft_bary.evt'
event = fits.open(test_data)
times = event[1].data['TIME']

times_zero = times - times[0]
counts = np.ones(len(times_zero))

tbin_size = 0.00025
startt = 0
endt = int(times_zero[-1])
t_bins = np.linspace(startt,endt,(endt-startt)*1/tbin_size+1)
summed_data, bin_edges, binnumber = stats.binned_statistic(times_zero,counts,statistic='sum',bins=t_bins)

no_bins = (endt-startt)/tbin_size
nicersoft_t_bins = np.arange(no_bins+1,dtype=np.float)*tbin_size
sums,edges = np.histogram(times_zero,bins=nicersoft_t_bins)
dat = np.array(sums,np.float32)

print(t_bins[20],summed_data[20])
print(nicersoft_t_bins[20],sums[20])
print('--')
print(t_bins[-20:],summed_data[-20:])
print(nicersoft_t_bins[-20:],sums[-20:])

plt.plot(t_bins[:100000],summed_data[:100000],'rx-')
plt.plot(nicersoft_t_bins[:100000],sums[:100000],'bx-')
plt.show()
"""

"""
import Lv3_average_ps_segments
#### FROM PRESTO
testdata = '/Volumes/Samsung_T5/NICERsoft_outputs/1060020113_pipe/accelsearch_1000s/ni1060020113_nicersoft_bary_GTI0_1000s.dat'
presto_bin_data = np.fromfile(testdata,dtype='<f',count=-1)
binsize = 1000/len(presto_bin_data)
print(binsize)
presto_t_bins = np.arange(0,1000,binsize)

plt.figure(1)
plt.plot(presto_t_bins,presto_bin_data,'rx-')
#print(presto_t_bins[:20],presto_bin_data[:20])
#print(presto_t_bins[-20:],presto_bin_data[-20:])
print('--')

#### FROM MY Lv3_AVERAGE_PS_SEGMENTS!
#test_data = '/Volumes/Samsung_T5/NICERsoft_outputs/1060020113_pipe/accelsearch_1000s/ni1060020113_nicersoft_bary_GTI0_1000s.evt'
test_data = '/Volumes/Samsung_T5/NICERsoft_outputs/1060020113_pipe/ni1060020113_nicersoft_bary.evt'
event = fits.open(test_data)
times = event[1].data['TIME']

times_zero = times - event[2].data[0][0]
counts = np.ones(len(times_zero))

time_bins = np.arange(0,int(times_zero[-1]),1)
summed_threshold,bin_edges,binnumber = stats.binned_statistic(times_zero,counts,statistic='sum',bins=time_bins)

#binned_t,binned_data = Lv3_average_ps_segments.binned_data('1060020113',['TIME','PI','PI_FAST'],0.00025)

#truncated_t = binned_t[(binned_t>=0)&(binned_t<=1000)]
#truncated_counts = binned_data[(binned_t>=0)&(binned_t<=1000)]


#plt.figure(2)
plt.plot(time_bins[:-1],summed_threshold,'bx-')
#print(truncated_t[:20],truncated_counts[:20])
#print(truncated_t[-20:],truncated_counts[-20:])

plt.show()
"""

obsids = ['12002501' + str(i+1).zfill(2) for i in range(26)]
for i in range(len(obsids)):
    eventfile = '/Volumes/Samsung_T5/NICERsoft_outputs/' + obsids[i] + '_pipe/ni' + obsids[i] + '_nicersoft_bary.evt'
    event = fits.open(eventfile)
    gtis = event[2].data
    print('Observation duration for ' + obsids[i] + ': ' + str(gtis[-1][1]-gtis[0][0]))

timeend = time.time()

print(str(timeend-timestart) + ' seconds')
