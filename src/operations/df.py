from collections import Counter

import polars as pl

from .base import BaseAnalyzer
from .models import (
    IPVisit,
    StatusCounter,
    HTTPMethodCounter,
    IPMethods,
    EndpointCounter,
    TrafficPerHour,
    AvgBytesPerHour,
)


class NginxLogsReports(BaseAnalyzer):
    """analyser"""

    def get_ip_visits(self) -> list[IPVisit]:
        """retrieves unique ip visits"""
        list_of_visits = (
            self.logs_df.group_by(["remote_add"])
            .agg(pl.col("http_referer").count().alias("counter"))
            .to_dicts()
        )
        return [
            IPVisit(ip=data["remote_add"], counter=data["counter"])
            for data in list_of_visits
        ]

    def get_status_counter(self) -> list[StatusCounter]:
        """Retrieves status counter"""
        list_of_requests = (
            self.logs_df.group_by(["status"])
            .agg(pl.col("http_referer").count().alias("counter"))
            .to_dicts()
        )
        return [
            StatusCounter(status=data["status"], counter=data["counter"])
            for data in list_of_requests
        ]

    def get_methods_counter(self) -> list[HTTPMethodCounter]:
        """Get method Counter"""
        self.logs_df = self.logs_df.with_columns(
            pl.col("request")
            .map_elements(lambda row: row.split(" ")[0])
            .alias("method")
        )
        methods_counter = (
            self.logs_df.group_by(["method"])
            .agg(pl.col("http_referer").count().alias("counter"))
            .to_dicts()
        )
        return [
            HTTPMethodCounter(method=data["method"], counter=data["counter"])
            for data in methods_counter
        ]

    def ip_methods_counter(self) -> list[IPMethods]:
        """get method for each ip address"""
        ipdf = (
            self.logs_df.group_by(["remote_add"])
            .agg(pl.col("method").alias("methods"))
            .to_dicts()
        )
        ip_methods_objs = []
        for item in ipdf:
            ip_methods_counter = Counter(item["methods"])
            method_counter_objs = [
                HTTPMethodCounter(
                    method=method_key, counter=ip_methods_counter[method_key]
                )
                for method_key in ip_methods_counter
            ]
            ip_methods_objs.append(
                IPMethods(ip=item["remote_add"], list_of_methods=method_counter_objs)
            )
        return ip_methods_objs

    def endpoint_counter(self) -> list[EndpointCounter]:
        """Get endpoint items"""
        self.logs_df = self.logs_df.with_columns(
            pl.col("request")
            .map_elements(lambda rows: rows.split(" ")[1], return_dtype=pl.String)
            .alias("endpoint")
        )
        endpoint_items = (
            self.logs_df.group_by(["endpoint"])
            .agg(pl.col("http_referer").count().alias("counter"))
            .to_dicts()
        )
        return [
            EndpointCounter(endpoint=data["endpoint"], counter=data["counter"])
            for data in endpoint_items
        ]

    def traffic_per_hours(self) -> list[TrafficPerHour]:
        """traffic per hour"""
        traffic = (
            self.logs_df.group_by(["hour"])
            .agg(pl.col("remote_add").count().alias("requests"))
            .sort(by="hour")
            .to_dicts()
        )
        return [
            TrafficPerHour(hour=data["hour"], counter=data["requests"])
            for data in traffic
        ]

    def average_bytes_per_hour(self) -> list[AvgBytesPerHour]:
        """calculations"""
        avg_bytes = (
            self.logs_df.group_by(["hour"])
            .agg(pl.col("body_bytes_sent").mean().alias("avg_bytes_per_hour"))
            .sort(by="hour")
            .to_dicts()
        )
        return [
            AvgBytesPerHour(hour=data["hour"], bytes=data["avg_bytes_per_hour"])
            for data in avg_bytes
        ]
