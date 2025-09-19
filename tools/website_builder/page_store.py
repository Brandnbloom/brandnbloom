from sqlmodel import SQLModel, Field, Session, create_engine, select
import os

DB_URL = os.getenv("BNB_DB_URL", "sqlite:///bnb_pages.db")
engine = create_engine(DB_URL, echo=False)

class Page(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    html: str
    css: str

SQLModel.metadata.create_all(engine)

class PageStore:
    @staticmethod
    def save_page(name, html, css):
        with Session(engine) as s:
            page = Page(name=name, html=html, css=css)
            s.add(page)
            s.commit()
            s.refresh(page)
            return page.id

    @staticmethod
    def list_pages():
        with Session(engine) as s:
            q = s.exec(select(Page.name))
            return [r for r,_ in q] if q else []

    @staticmethod
    def load_page(name):
        with Session(engine) as s:
            q = s.exec(select(Page).where(Page.name==name))
            return q.first()
