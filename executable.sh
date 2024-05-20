#!/bin/bash

#installation
conda create --name N python=3.9
conda activate N 
conda install minimap2
conda install Filtlong
conda install bedtools
git clone https://github.com/zwets/taxo.git
cd taxo
mv ./taxo > ./anaconda3/envs/N/bin/taxo
conda install taxonkit