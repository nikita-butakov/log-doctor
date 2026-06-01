# Log Doctor

## What it does

Analyze log files from the program with different levels and output written into report file.

The tool can also explain found problems using AI when the `--ai` option is enabled.

## Usage

```bash
usage: log_doctor.py [-h] [--output OUTPUT] [--last LAST] [--level {ERROR,WARNING,CRITICAL}] [--ai] log_file
```

## Examples

```bash
python .\log_doctor.py .\sample.log
```

```bash
python .\log_doctor.py .\sample.log --level ERROR
```

```bash
python.exe .\log_doctor.py .\sample.log --last 1
```

```bash
python.exe .\log_doctor.py .\sample.log --output incident.md
```

```bash
python.exe .\log_doctor.py .\sample.log --ai
```

```bash
python.exe .\log_doctor.py .\sample.log --level ERROR --ai
```

## Options

* `--output` - different output file (default `report.md`)
* `--last` - number of the last logs you want to check
* `--level` - level of observability (`ERROR`, `WARNING`, `CRITICAL`), by default is `ALL`
* `--ai` - explain found problems using AI

## What I learned

* import and use Python modules
* write and define functions
* define arguments
* create lists and dictionaries
* use conditions
* filter args from dictionaries
* write output to files
* use OpenAI API for AI explanations
