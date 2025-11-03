import sys
import textwrap

import click

from .logger import setup_logger
from .nginx_logs_parser.container import NginxLogsParser
from .nginx_logs_analyzer.reports import NginxLogsReports
from .nginx_logs_parser.file import FileLogsParser
from .nginx_logs_parser.models import NginxLogRecord

logger = setup_logger(__name__)


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


def extract_file_logs(filename: str) -> list[NginxLogRecord]:
    """Extracts logs from file"""
    file_logs_parser = FileLogsParser.create_from_log_file(filename=filename)
    clean_logs = file_logs_parser.logs
    return clean_logs


@click.command()
@click.option("--container", "-c", type=str, help="Container Name")
@click.option("--metadata", "-m", is_flag=True, help="Print Container Metadata")
@click.option(
    "--to-csv", type=str, default="output.txt", help="Store Report result to file"
)
@click.option("--filename", "-f", type=str, default="", help="Extract from Log file")
def runner(container: str, metadata: bool, to_csv: str, filename: str) -> None:
    """cli runner"""
    try:
        if filename:
            clean_logs = extract_file_logs(filename=filename)
        else:
            clean_logs = extract_container_logs(container=container, metadata=metadata)
        analyzer = NginxLogsReports.create(nginx_logs=clean_logs)
        report_results = analyzer.log_report()
        analyzer.write_report(filename=to_csv, report_contents=report_results)

    except Exception as ex:
        logger.error(ex)
        sys.exit(1)


if __name__ == "__main__":
    runner()
