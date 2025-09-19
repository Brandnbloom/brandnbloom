from sqlmodel import SQLModel, Field, create_engine, Session, select
import os
DB = os.getenv("BNB_CRM_DB", "sqlite:///crm.db")
engine = create_engine(DB)
class Lead(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str | None = None
    source: str | None = None
    stage: str = "new"
SQLModel.metadata.create_all(engine)

def create_lead(data):
    with Session(engine) as s:
        lead = Lead(**data)
        s.add(lead); s.commit(); s.refresh(lead)
        return lead
