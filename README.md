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
  -l, --logs            Extract logs
  -m, --metadata        Print Container Metadata
  --to-csv TEXT         Export logs to CSV
  --help                Show this message and exit.
```