import pytest
from pathlib import Path

from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from src.services.rag.generator import ThemeGenerator


FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(name="theme_generator")
async def theme_generator_fixture():
    """Creates a ThemeGenerator instance and generates themes for each test.

    Note: While this fixture could be optimized with module scope since
    ThemeGenerator uses temperature=0, we prioritize test isolation over
    performance. This makes tests more reliable and easier to debug, even
    though it means regenerating themes for each test.
    """
    path = f"{FIXTURE_DIR}/douglass_ch1.pdf"
    generator = ThemeGenerator(path, "Frederick Douglass")
    themes = await generator.generate_themes()
    return generator, themes


@pytest.fixture(name="session")
def session_fixture():
    """Creates an in-memory SQLite session for testing purposes."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
