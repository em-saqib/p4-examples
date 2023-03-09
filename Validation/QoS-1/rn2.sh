#!/bin/bash

simple_switch_CLI --thrift-port 9090 < rules-s1.cmd
simple_switch_CLI --thrift-port 9091 < rules-s2.cmd
simple_switch_CLI --thrift-port 9092 < rules-s2.cmd
#atom --no-sandbox ./logs/s1.log
