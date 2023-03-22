#!/bin/bash

set -e -x

echo 'Simulation starts'

sudo make stop
sudo make clean
sudo make run
sudo make stop

cd ./logs
sudo grep "]  INFO CSV" s1.log > /home/p4/tutorials/exercises/basic20/s1.log
cd ..
echo 'Classification results'
sudo python3 Classification ResultsFilter.py
