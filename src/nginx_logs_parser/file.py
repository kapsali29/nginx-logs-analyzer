from __future__ import annotations
from pydantic import BaseModel
from .models import NginxLogRecord
from .settings import LOG_PATTERN


class FileLogsParser(BaseModel):
    """Parse logs from files"""

    logs: list[NginxLogRecord]

    @staticmethod
    def transform_to_log_record(log_line: str) -> NginxLogRecord | None:
        """transform log line"""
        match = LOG_PATTERN.match(log_line)
        if match:
            data = match.groupdict()
            nginx_record = NginxLogRecord(
                remote_add=data["remote_addr"],
                remote_user=data["remote_user"],
                time_local=data["time_local"],
                request=data["request"],
                status=int(data["status"]),
                body_bytes_sent=int(data["body_bytes_sent"]),
                http_referer=data["http_referer"],
                http_user_agent=data["http_user_agent"],
            )
            return nginx_record
        else:
            return None

    @classmethod
    def create_from_log_file(cls, filename: str) -> FileLogsParser:
        """instantiate the BaseModel"""
        clean_logs = []
        with open(filename) as file_log:
            for line in file_log:
                nginx_log_record = cls.transform_to_log_record(
                    log_line=line.rstrip("\n")
                )
                if nginx_log_record:
                    clean_logs.append(nginx_log_record)
        return cls(logs=clean_logs)
