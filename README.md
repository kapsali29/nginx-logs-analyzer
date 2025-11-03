# Nginx Logs Analyzer
Nginx Logs Analyzer is a CLI project responsible to extract, perform modelling and analyze NGINX Access logs.
The CLI tool provides capabilities to end users to extract logs from static log files and running containers.

## Instructions

```shell
$ poetry install --no-root
$ python -m src.main -c nginx -l
```
### Available Arguments

```shell
Usage: python -m src.main [OPTIONS]

Options:
  -c, --container TEXT  Container Name
  -m, --metadata        Print Container Metadata
  --to-txt TEXT         Store Report result to text file
  -j, --to-json TEXT    Store Report result to JSON file
  -f, --filename TEXT   Extract from Log file
  --help                Show this message and exit.
```