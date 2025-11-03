from pydantic import BaseModel


class Counter(BaseModel):
    """BaseCounter"""

    counter: int


class IPVisit(Counter):
    """Count IP Visits"""

    ip: str

    def to_str(self) -> str:
        """to string"""
        return f"""{self.ip}:{self.counter}"""


class StatusCounter(Counter):
    """Count Status requests"""

    status: int

    def to_str(self) -> str:
        """to string"""
        return f"""Status Code={self.status} Counts={self.counter}"""


class HTTPMethodCounter(Counter):
    """Count HTTP Methods"""

    method: str

    def to_str(self) -> str:
        """to string"""
        return f"""HTTP Method={self.method} Counts={self.counter}"""


class IPMethods(BaseModel):
    """Get Method Counter for each IP"""

    ip: str
    list_of_methods: list[HTTPMethodCounter]

    def to_str(self) -> str:
        """to string"""
        list_of_methods_str = "\n".join([obj.to_str() for obj in self.list_of_methods])
        sections = [(f"Most Frequest Methods for IP={self.ip}", list_of_methods_str)]
        return "\n\n".join(f"{title}\n{'-' * 30}\n{body}\n" for title, body in sections)


class EndpointCounter(Counter):
    """Counts endpoints appearances"""

    endpoint: str

    def to_str(self) -> str:
        """to string"""
        return f"""Endpoint='{self.endpoint}' Counts={self.counter}"""
