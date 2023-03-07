#!/bin/bash
parallel ::: "sudo python3 send3.py 10.0.5.5" "sudo python3 send1.py 10.0.5.5"

sleep 10

rm -r s1.log s2.log s3.log foo.png my_file.csv
cd ./logs
sudo grep "]  INFO ClassID : " s1.log > /home/p4/tutorials/exercises/basic21/s1.log
sudo grep "]  INFO ClassID : " s2.log > /home/p4/tutorials/exercises/basic21/s2.log
sudo grep "]  INFO ClassID : " s3.log > /home/p4/tutorials/exercises/basic21/s3.log
cd ../
#sudo python3 csvFilter.py
#nomacs foo.png
