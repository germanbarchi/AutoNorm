#!/bin/bash

conda install -c conda-forge montreal-forced-aligner
conda install -c conda-forge python=3.8 kaldi sox librosa biopython praatio tqdm requests colorama pyyaml pynini openfst baumwelch ngram

mfa models download acoustic spanish_mfa
mfa models download language_model spanish_mfa_lm
mfa models download g2p spanish_latin_america_mfa
mfa models download dictionary spanish_latin_america_mfa

mkdir ./output
mkdir ./input

git clone https://github.com/kylerbrown/textgrid.git