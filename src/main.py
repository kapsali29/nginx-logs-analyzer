import sys
import textwrap

import click

from .logger import setup_logger
from .nginx_logs_parser.main import NginxLogsParser
from .nginx_logs_analyzer.main import BaseAnalyzer

logger = setup_logger(__name__)


@click.command()
@click.option("--container", "-c", type=str, help="Container Name")
@click.option("--logs", "-l", is_flag=True, help="Extract logs")
@click.option("--metadata", "-m", is_flag=True, help="Print Container Metadata")
@click.option("--to-csv", type=str, default="", help="Export logs to CSV")
def runner(container: str, metadata: bool, logs: bool, to_csv: str) -> None:
    """cli runner"""
    try:
        logs_parser = NginxLogsParser.create()
        nginx_container = logs_parser.get_nginx_container(name=container)
        if metadata:
            metadata_records = logs_parser.get_nginx_metadata(container=nginx_container)
            metadata_report = metadata_records.to_report()
            logger.info(textwrap.dedent(metadata_report).strip())
        if logs:
            raw_container_logs = nginx_container.logs()
            clean_logs = logs_parser.process_container_logs(raw_container_logs)
            base_analyzer = BaseAnalyzer.create(nginx_logs=clean_logs)
            breakpoint()
            if to_csv:
                base_analyzer.to_csv(name=to_csv)
            logger.info(clean_logs)
    except Exception as ex:
        logger.error(ex)
        sys.exit(1)


if __name__ == "__main__":
    runner()
