import numpy as np
from scipy.signal import lfilter, resample, decimate
import matplotlib.pyplot as plt
import librosa
import glob
import tqdm
import os
import soundfile
import sys

def vumeter(x,fs):

    D = 8;  #Upsampling factor

    wn= 13.5119125366
    zeta= 0.81271698642867751129343563262192
    Td = 1/fs/D

    B = (Td**2)*(wn**2)*np.array([1,2,1])

    A = np.array([(4+4*zeta*wn*Td+wn**2*Td**2),(-8 + 2*wn**2*Td**2),(4-4*zeta*wn*Td+wn**2*Td**2)])

    #Scaling

    scaling = (np.pi/2)/(np.sqrt(600*0.001*2))

    #Upsample the input signal by 8x.

    x_u = resample(x,len(x)*8)

    out = lfilter(B, A, np.abs(x_u))
    y_u = scaling * out;
    y1= decimate(y_u,D)+0.000001

    y= 20*np.log10(y1)

    max_val_db=np.nanmax(y)
    print('max_value (dB): %f' % max_val_db)
    max_val_v=10**(max_val_db/20)
    print('max_value (v): %f' % max_val_v)

    return y,max_val_db


def scale(y,x,fs,max_val_db,target_val):
  
    delta=target_val-max_val_db
    scale_factor=10**(delta/20)

    print('delta(dB): %f' % delta)
    print('scale-factor: %f \n' % scale_factor)

    y_target=x*scale_factor

    print('Normalized Values: \n')
    vumeter(y_target,fs)

    return y_target

def calibration_value(calibration_path):

    y_,fs_=librosa.core.load(calibration_path,sr=None)
    target_val=vumeter(y_,fs_)[1]
    print('target_val: %f' %target_val)

    return target_val

def save_file (y_out,fs,out_path,audio):

    filename=audio.split('/')[-1]
    parent='/'.join((audio.split('/')[-3],audio.split('/')[-2]))
    rel_path=out_path+'/'+parent

    if not os.path.exists(rel_path):
        os.makedirs(rel_path)
    
    out_abs_path=rel_path+'/norm_'+filename

    soundfile.write(out_abs_path,y_out,fs)


if __name__=='__main__':
    
    print('-->Normalizing audios...')

    audio_dir=sys.argv[1]
    audio_list=sys.argv[2]
    calibration_path=sys.argv[3]
    
    print(audio_dir)
    cwd=os.getcwd()

    out_dir=os.path.join(cwd,'normalized_audios')
    print(out_dir)
    audio_path=glob.glob(audio_dir+'/*.wav')
    
    # Get calibration tone max val 

    target_val=calibration_value(calibration_path)

    for audio in tqdm.tqdm(audio_path):
       
        x,fs=librosa.core.load(audio,sr=None)
    
        y,max_val_db=vumeter(x,fs)
    
        y_scaled=scale(y,x,fs,max_val_db,target_val)

        save_file(y_scaled,fs,out_dir,audio)