# Nginx Logs Analyzer

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
  --to-csv TEXT         Store Report result to file
  -f, --filename TEXT   Extract from Log file
  --help                Show this message and exit.
```