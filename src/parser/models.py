from pydantic import BaseModel


class NginxContainerMetadata(BaseModel):
    """Nginx metadata model"""

    id: str
    created: str
    args: list[str]
    state: str
    restart_count: int
    platform: str
    image: str
    env: list[str]

    def to_report(self) -> str:
        """to string report"""
        report = f"""
            Container id: {self.id}
            Created: {self.created}
            State: {self.state}
            Image: {self.image}
            Restarts: {self.restart_count}
            Platform: {self.platform}
            Environment Variables: {", ".join(self.env)}
            Container Arguments: {", ".join(self.args)}
        """
        return report


class NginxLogRecord(BaseModel):
    """Log Record"""

    remote_add: str
    remote_user: str
    time_local: str
    request: str
    status: int
    body_bytes_sent: int
    http_referer: str
    http_user_agent: str
