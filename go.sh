#!/bin/bash

CWD=$(pwd)
VOICE_TYPE='VM'
LIST_NAME='Lista_3'

mfa align --clean ./input/$VOICE_TYPE/$LIST_NAME spanish_latin_america_mfa spanish_mfa ./output

OUT=$(python3 $CWD/textgrid/textgrid.py -o $CWD/output/textgrid.csv $CWD/output/$LIST_NAME.TextGrid)

TIMESTAMPS=$(python3 return_timestamps.py $OUT)

AUDIO=$CWD/input/$VOICE_TYPE/$LIST_NAME/$LIST_NAME.wav
AUDIO_OUT=$CWD/trimmed_audios

AUDIO_OUT=$(python3 $CWD/trim_audio.py $TIMESTAMPS $AUDIO $AUDIO_OUT $LIST_NAME $VOICE_TYPE)

echo $AUDIO_OUT

CALIBRATION_FILE_PATH=$CWD/calibration_file/Calibracion.wav

python3 vumeter_normalizer.py $AUDIO_OUT $LIST_NAME $CALIBRATION_FILE_PATH