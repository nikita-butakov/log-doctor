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

## Run with Docker

Build the Docker image:

```bash
docker build -t log-doctor .
```

Run basic analysis:

```bash
docker run --rm -v "$PWD":/app log-doctor sample.log
```

Run with level filter:

```bash
docker run --rm -v "$PWD":/app log-doctor sample.log --level ERROR
```

Run with custom output file:

```bash
docker run --rm -v "$PWD":/app log-doctor sample.log --last 1 --output incident.md
```

Run with AI explanation:

```bash
export OPENAI_API_KEY="your_api_key_here"

docker run --rm \
  -e OPENAI_API_KEY \
  -v "$PWD":/app \
  log-doctor sample.log --ai
```

## Options

* `--output` - different output file (default `report.md`)
* `--last` - number of the last logs you want to check
* `--level` - level of observability (`ERROR`, `WARNING`, `CRITICAL`), by default is `ALL`
* `--ai` - explain found problems using AI

## Project files

* `log_doctor.py` - main Python script
* `requirements.txt` - Python dependencies
* `Dockerfile` - Docker image build instructions
* `.dockerignore` - files excluded from Docker build context
* `sample.log` - example log file
* `report.md` - generated report file

## What I learned

* import and use Python modules
* write and define functions
* define arguments
* create lists and dictionaries
* use conditions
* filter args from dictionaries
* write output to files
* use OpenAI API for AI explanations
* build and run a Python application inside Docker
* pass environment variables into Docker containers
* mount local project files into a Docker container