import sys
import click
import polars as pl
import textwrap
from logger import setup_logger
from nginx_logs_parser.main import NginxLogsParser

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
            clean_logs_dict = [obj.model_dump() for obj in clean_logs]
            logs_df = pl.DataFrame(clean_logs_dict)
            if to_csv:
                logs_df.write_csv(to_csv, separator=",")
            logger.info(clean_logs)
    except Exception as ex:
        logger.error(ex)
        sys.exit(1)

if __name__ == "__main__":
    runner()
