from __future__ import annotations
import polars as pl
from pydantic import BaseModel, ConfigDict
from src.nginx_logs_parser.container import NginxLogRecord


class BaseAnalyzer(BaseModel):
    """Base Logs Analyzer"""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    logs_df: pl.DataFrame

    @classmethod
    def create(cls, nginx_logs: list[NginxLogRecord]) -> BaseAnalyzer:
        """instantiate the BaseModel"""
        clean_logs_dict = [obj.model_dump() for obj in nginx_logs]
        return cls(logs_df=pl.DataFrame(clean_logs_dict))

    @staticmethod
    def write_report(filename: str, report_contents: str) -> None:
        """store report contents"""
        with open(filename, "w", encoding="utf-8") as report_file:
            report_file.write(report_contents)
