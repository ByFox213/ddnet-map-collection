from pydantic import BaseModel, Field


class Postresql(BaseModel):
    host: str = Field(default=None)
    port: int = Field(default=None)
    user: str = Field(default=None)
    passwd: str = Field(default=None)
    db: str = Field(default=None)

    def __str__(self) -> str:
        return f"dbname={self.db} host={self.host} port={self.port} user={self.user} password={self.passwd}"