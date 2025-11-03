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

#### NGINX Access Logs
The access logs needs to follow the following format

```python
LOG_PATTERN = re.compile(
    r"^(?P<remote_addr>\S+) - (?P<remote_user>\S+) \[(?P<time_local>[^\]]+)\] "
    r'"(?P<request>[^"]*)" (?P<status>\d{3}) (?P<body_bytes_sent>\d+) '
    r'"(?P<http_referer>[^"]*)" "(?P<http_user_agent>[^"]*)"'
)
```

Accepted logs are the following

```conf
192.0.2.15 - - [02/Nov/2025:19:59:11 +0000] "POST /login HTTP/1.1" 200 31896 "http://example.com/login" "Googlebot/2.1 (+http://www.google.com/bot.html)"
203.0.113.9 - - [03/Nov/2025:00:40:24 +0000] "GET /robots.txt HTTP/1.1" 403 27858 "http://localhost/" "Mozilla/5.0 (X11; Linux x86_64)"
203.0.113.5 - - [02/Nov/2025:18:07:23 +0000] "DELETE /api/v1/users HTTP/1.1" 403 46837 "http://example.com/" "Googlebot/2.1 (+http://www.google.com/bot.html)"
198.51.100.88 - - [03/Nov/2025:04:26:24 +0000] "GET /static/js/app.js HTTP/1.1" 502 40708 "-" "kube-probe/1.29"
198.51.100.88 - - [02/Nov/2025:22:31:19 +0000] "POST /api/v1/users HTTP/1.1" 404 47411 "http://localhost/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
198.51.100.23 - - [03/Nov/2025:07:13:05 +0000] "DELETE /dashboard HTTP/1.1" 301 34393 "http://example.com/login" "Mozilla/5.0 (X11; Linux x86_64)"
203.0.113.5 - - [02/Nov/2025:23:18:34 +0000] "POST /api/v1/users HTTP/1.1" 302 2757 "-" "Mozilla/5.0 (X11; Linux x86_64)"
```