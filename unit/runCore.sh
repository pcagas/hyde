#!/bin/bash

# delete old Redis DB dump
rm -f dump.rdb
# launch redis-server
redis-server 
