#!/bin/bash

# activate the virtual environment
source /home/nikopelkonen/workspace/homescreen/bienv/bin/activate

# run the ruuvitag.py script
python /home/nikopelkonen/workspace/homescreen/ruuvitag.py
python /home/nikopelkonen/workspace/homescreen/temperature/printtemptosjson.py