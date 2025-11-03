import json
from .df import NginxLogsReports


class LogsReport(NginxLogsReports):
    """Generates the report"""

    def to_str(self) -> str:
        """gathers reports"""
        status_counters_str = "\n".join(
            [obj.to_str() for obj in self.get_status_counter()]
        )
        ip_visits_str = "\n".join([obj.to_str() for obj in self.get_ip_visits()])
        num_of_methods_str = "\n".join(
            [obj.to_str() for obj in self.get_methods_counter()]
        )
        ip_methods_str = "\n".join([obj.to_str() for obj in self.ip_methods_counter()])
        endpoints_str = "\n".join([obj.to_str() for obj in self.endpoint_counter()])
        traffic_str = "\n".join([obj.to_str() for obj in self.traffic_per_hours()])
        average_bytes_per_hour_str = "\n".join(
            [obj.to_str() for obj in self.average_bytes_per_hour()]
        )

        sections = [
            ("Status Information", status_counters_str),
            ("Most Frequent IPs", ip_visits_str),
            ("Most Frequent Methods", num_of_methods_str),
            ("Most Frequent Methods per IP", ip_methods_str),
            ("Most Frequent Endpoints", endpoints_str),
            ("Requests per Hour", traffic_str),
            ("Mean Bytes Sent per Hour", average_bytes_per_hour_str),
        ]
        result = "\n\n".join(f"{title}\n{'-' * 30}\n{body}" for title, body in sections)
        return result

    def to_json(self) -> str:
        """to JSON representation"""
        return json.dumps(
            {
                "Status Information": [
                    obj.model_dump() for obj in self.get_status_counter()
                ],
                "Most Frequent IPs": [obj.model_dump() for obj in self.get_ip_visits()],
                "Most Frequent Methods": [
                    obj.model_dump() for obj in self.get_methods_counter()
                ],
                "Most Frequent Methods per IP": [
                    obj.model_dump() for obj in self.ip_methods_counter()
                ],
                "Most Frequent Endpoints": [
                    obj.model_dump() for obj in self.endpoint_counter()
                ],
                "Requests per Hour": [
                    obj.model_dump() for obj in self.traffic_per_hours()
                ],
                "Mean Bytes Sent per Hour": [
                    obj.model_dump() for obj in self.average_bytes_per_hour()
                ],
            }
        )
