import sys

import click

from .logger import setup_logger
from .nginx_logs_parser.container import extract_container_logs
from .nginx_logs_analyzer.report import LogsReport
from .nginx_logs_parser.file import extract_file_logs

logger = setup_logger(__name__)


@click.command()
@click.option("--container", "-c", type=str, help="Container Name")
@click.option("--metadata", "-m", is_flag=True, help="Print Container Metadata")
@click.option(
    "--to-txt", type=str, default="output.txt", help="Store Report result to text file"
)
@click.option(
    "--to-json", "-j", type=str, default="", help="Store Report result to JSON file"
)
@click.option("--filename", "-f", type=str, default="", help="Extract from Log file")
def runner(
    container: str, metadata: bool, to_txt: str, filename: str, to_json: str
) -> None:
    """cli runner"""
    try:
        if filename:
            clean_logs = extract_file_logs(filename=filename)
        else:
            clean_logs = extract_container_logs(container=container, metadata=metadata)
        analyzer = LogsReport.create(nginx_logs=clean_logs)
        if to_json:
            report_contents = analyzer.to_json()
            report_name = to_json
        else:
            report_contents = analyzer.to_str()
            report_name = to_txt
        analyzer.write_report(filename=report_name, report_contents=report_contents)

    except Exception as ex:
        logger.error(ex)
        sys.exit(1)


if __name__ == "__main__":
    runner()
