# Log Doctor

## What it does
Analyze log files from the program with different levels and output written into report file

## Usage
usage: log_doctor.py [-h] [--output OUTPUT] [--last LAST] [--level {ERROR,WARNING,CRITICAL}] log_file

## Examples
python .\log_doctor.py .\sample.log
python .\log_doctor.py .\sample.log --level ERROR
python.exe .\log_doctor.py .\sample.log --last 1
python.exe .\log_doctor.py .\sample.log --output incident.md

## Options
--output - different output file (default report.md)
--last - number of the last logs you want to check
--level - level of observability (ERROR, WARNING, CRITICAL), by default is ALL

## What I learned
import and use Python modules
write and define functions
define arguments
create lists, dictionaries
conditions
filter args from dictionaries
write output to files