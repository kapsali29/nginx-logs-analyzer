from __future__ import annotations

import docker
import re
from pydantic import BaseModel, ConfigDict
from docker.client import DockerClient
from docker.models.containers import Container
from .models import NginxContainerMetadata, NginxLogRecord


class NginxLogsParser(BaseModel):
    """Extract nginx logs"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: DockerClient

    @classmethod
    def create(cls) -> NginxLogsParser:
        """initialize docker client"""
        return cls(client=docker.from_env())

    def get_nginx_container(self, name: str) -> Container:
        """retrieves nginx container"""
        nginx_container = self.client.containers.get(name)
        return nginx_container

    @staticmethod
    def get_nginx_metadata(container: Container) -> NginxContainerMetadata:
        """retrieves nginx metadata"""
        container_attrs = container.attrs
        return NginxContainerMetadata(
            id=container_attrs["Id"],
            created=container_attrs["Created"],
            args=container_attrs["Args"],
            state=container_attrs["State"]["Status"],
            restart_count=container_attrs["RestartCount"],
            platform=container_attrs["Platform"],
            image=container_attrs["Config"]["Image"],
            env=container_attrs["Config"]["Env"],
        )

    @staticmethod
    def transform_to_log_record(log_line: str) -> NginxLogRecord | None:
        """transform log line"""

        pattern = re.compile(
            r"^(?P<remote_addr>\S+) - (?P<remote_user>\S+) \[(?P<time_local>[^\]]+)\] "
            r'"(?P<request>[^"]*)" (?P<status>\d{3}) (?P<body_bytes_sent>\d+) '
            r'"(?P<http_referer>[^"]*)" "(?P<http_user_agent>[^"]*)"'
        )
        match = pattern.match(log_line)
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

    def process_container_logs(self, raw_logs: bytes) -> list[NginxLogRecord]:
        """function to process raw nginx logs"""
        clean_logs = []
        decoded_logs = raw_logs.decode()
        decoded_logs_list = decoded_logs.split("\n")
        for log_line in decoded_logs_list:
            nginx_log_record = self.transform_to_log_record(log_line=log_line)
            if nginx_log_record:
                clean_logs.append(nginx_log_record)
        return clean_logs
