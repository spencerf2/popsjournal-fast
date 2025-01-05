import pytest
from pathlib import Path

from sqlmodel import Session, select
from src.entities import Theme, ThemeUserLink, User


FIXTURE_DIR = Path(__file__).parent.parent.parent / "fixtures"


@pytest.mark.asyncio
async def test_theme_generator_generates_and_saves_themes(session: Session, theme_generator):
    generator, themes = await theme_generator

    assert len(themes) > 0
    for theme in themes:
        session.add(theme)

    session.commit()

    # Query back and verify themes were saved
    statement = select(Theme)
    results = session.exec(statement).all()

    assert len(results) == len(themes)

    # Verify first theme's content
    db_theme = results[0]
    assert db_theme.title is not None
    assert db_theme.description is not None
    assert db_theme.confidence_score is not None
    assert isinstance(db_theme.supporting_snippets, list)
    assert len(db_theme.supporting_snippets) > 0

    # Verify snippet structure and relationships
    first_snippet = db_theme.supporting_snippets[0]
    assert "content" in first_snippet
    assert "source" in first_snippet
    assert "page" in first_snippet

    # Verify Theme to User relationships are established
    test_user = User(phone_number="+1234567890", name="Test User")
    session.add(test_user)
    session.commit()

    theme_link = ThemeUserLink(theme_id=db_theme.id, user_id=test_user.id)
    session.add(theme_link)
    session.commit()

    db_theme = session.get(Theme, db_theme.id)
    assert len(db_theme.user_links) == 1
    assert db_theme.user_links[0].user.name == "Test User"


@pytest.mark.asyncio
async def test_theme_generator_snippets_exist_in_source(theme_generator):
    generator, themes = await theme_generator

    full_text = " ".join(generator.store.get()["documents"]).lower()

    for theme in themes:
        for snippet in theme.supporting_snippets:
            snippet_text = snippet['content'].lower()
            assert snippet_text in full_text, f"Snippet not found in source: {snippet_text}"
