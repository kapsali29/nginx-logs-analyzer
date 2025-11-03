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
        logs_df = (
            pl.DataFrame(clean_logs_dict)
            .with_columns(pl.col("time_local").str.to_datetime("%d/%b/%Y:%H:%M:%S %z"))
            .with_columns(
                [
                    pl.col("time_local").dt.hour().alias("hour"),
                    pl.col("time_local").dt.day().alias("day"),
                ]
            )
        )
        return cls(logs_df=logs_df)

    @staticmethod
    def write_report(filename: str, report_contents: str) -> None:
        """store report contents"""
        with open(filename, "w", encoding="utf-8") as report_file:
            report_file.write(report_contents)
