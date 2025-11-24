from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime
import os

DB_URL = os.getenv("BNB_DB_URL", "sqlite:///bnb_pages.db")

# Needed for SQLite concurrency issues when using Streamlit
connect_args = {"check_same_thread": False}
engine = create_engine(DB_URL, echo=False, connect_args=connect_args)


class Page(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    html: str
    css: str
    version: int = Field(default=1)
    published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


SQLModel.metadata.create_all(engine)


class PageStore:

    @staticmethod
    def save_page(name: str, html: str, css: str):
        """Create a new landing page. Auto-increments version if exists."""
        with Session(engine) as s:
            # Check duplicate
            existing = s.exec(select(Page).where(Page.name == name)).first()

            if existing:
                # Create new version
                new_version = existing.version + 1
            else:
                new_version = 1

            page = Page(
                name=name,
                html=html or "",
                css=css or "",
                version=new_version,
                published=False
            )

            s.add(page)
            s.commit()
            s.refresh(page)
            return page.id

    @staticmethod
    def update_page(page_id: int, html: str = None, css: str = None, published: bool = None):
        """Update an existing page."""
        with Session(engine) as s:
            page = s.get(Page, page_id)
            if not page:
                return None

            page.html = html if html is not None else page.html
            page.css = css if css is not None else page.css
            if published is not None:
                page.published = published

            page.version += 1
            page.updated_at = datetime.utcnow()

            s.add(page)
            s.commit()
            s.refresh(page)
            return page

    @staticmethod
    def delete_page(page_id: int):
        """Delete a page by ID."""
        with Session(engine) as s:
            page = s.get(Page, page_id)
            if not page:
                return False

            s.delete(page)
            s.commit()
            return True

    @staticmethod
    def list_pages():
        """Return all page names sorted by updated date."""
        with Session(engine) as s:
            q = s.exec(select(Page).order_by(Page.updated_at.desc()))
            return [p.name for p in q]

    @staticmethod
    def load_page(name: str):
        """Load the latest version of a page by name."""
        with Session(engine) as s:
            q = s.exec(
                select(Page)
                .where(Page.name == name)
                .order_by(Page.version.desc())
            )
            return q.first()

    @staticmethod
    def get_page_by_id(page_id: int):
        with Session(engine) as s:
            return s.get(Page, page_id)

    @staticmethod
    def search_pages(query: str):
        """Search by name."""
        with Session(engine) as s:
            q = s.exec(
                select(Page)
                .where(Page.name.contains(query))
                .order_by(Page.updated_at.desc())
            )
            return q.all()
