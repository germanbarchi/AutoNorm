import pandas as pd 
import sys
import librosa
import soundfile
import os

def trim_audio(y,fs,df,out_path,pad):

    for i in range(df.shape[0]):
        
        start=int((df.iloc[i]['start']*fs)-pad)
        end=int((df.iloc[i]['stop']*fs)+pad)
        filename=df.iloc[i]['name']
        trim=y[start:end]

        soundfile.write(out_path+'/'+filename+'.wav',trim,fs)

if __name__=='__main__':

    #print('-->Trimming audios...')
    timestamps_df=sys.argv[1]    
    audio=sys.argv[2]
    out_path=sys.argv[3]
    list_name=sys.argv[4]
    voice_type=sys.argv[5]

    df=pd.read_csv(timestamps_df)
    
    out_path=out_path+'/'+voice_type+'/'+list_name
    
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    y,fs=librosa.core.load(audio,sr=None)
    
    pad_seconds=0.2 
    pad_samples=int(pad_seconds*fs) 

    trim_audio(y,fs,df,out_path,pad_samples)
    
    print(out_path)