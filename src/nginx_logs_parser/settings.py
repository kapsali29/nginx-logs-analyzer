import re

LOG_PATTERN = re.compile(
    r"^(?P<remote_addr>\S+) - (?P<remote_user>\S+) \[(?P<time_local>[^\]]+)\] "
    r'"(?P<request>[^"]*)" (?P<status>\d{3}) (?P<body_bytes_sent>\d+) '
    r'"(?P<http_referer>[^"]*)" "(?P<http_user_agent>[^"]*)"'
)
