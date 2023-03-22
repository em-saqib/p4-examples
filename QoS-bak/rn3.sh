#!/bin/bash
parallel ::: "./send3.py 10.0.5.5" "./send1.py 10.0.5.5" "./send2.py 10.0.5.5"

sleep 1

rm -r s1.log s2.log s3.log s1.csv s2.csv s3.csv

sleep 1

cd ./logs
sudo grep "]  INFO ClassID : " s1.log > /home/p4/tutorials/exercises/QoS-1/s1.log
sudo grep "]  INFO Deadline : " s1.log > /home/p4/tutorials/exercises/QoS-1/s1-deadline.log
sudo grep "]  INFO ClassID : " s2.log > /home/p4/tutorials/exercises/QoS-1/s2.log
sudo grep "]  INFO Deadline : " s2.log > /home/p4/tutorials/exercises/QoS-1/s2-deadline.log
sudo grep "]  INFO ClassID : " s3.log > /home/p4/tutorials/exercises/QoS-1/s3.log
sudo grep "]  INFO Deadline : " s3.log > /home/p4/tutorials/exercises/QoS-1/s3-deadline.log
cd ../

./csvFilter.py

parallel ::: "./drawS1.py" "./drawS2.py" "./drawS3.py"

#nomacs foo.png
