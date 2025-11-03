from __future__ import annotations

import textwrap
import docker
from pydantic import BaseModel, ConfigDict
from docker.client import DockerClient
from docker.models.containers import Container
from src.logger import setup_logger
from .models import NginxContainerMetadata, NginxLogRecord
from .settings import LOG_PATTERN

logger = setup_logger(__name__)


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


def extract_container_logs(
    container: str, metadata: bool = False
) -> list[NginxLogRecord]:
    """Extracts logs from Nginx Container"""
    logs_parser = NginxLogsParser.create()
    nginx_container = logs_parser.get_nginx_container(name=container)
    raw_container_logs = nginx_container.logs()
    clean_logs = logs_parser.process_container_logs(raw_container_logs)
    if metadata:
        metadata_records = logs_parser.get_nginx_metadata(container=nginx_container)
        metadata_report = metadata_records.to_report()
        logger.info(textwrap.dedent(metadata_report).strip())
    return clean_logs
