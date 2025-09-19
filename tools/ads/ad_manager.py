import json, os
from sqlmodel import SQLModel, Field, Session, create_engine, select

engine = create_engine("sqlite:///ads.db")
class Campaign(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    platform: str
    budget: float
    status: str = "paused"
SQLModel.metadata.create_all(engine)

def create_campaign(name, platform, budget):
    with Session(engine) as s:
        c = Campaign(name=name, platform=platform, budget=budget)
        s.add(c); s.commit(); s.refresh(c)
        return c
