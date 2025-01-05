from src.entities.theme import Theme, ThemeUserLink
from src.entities.user import User

# Prevents forward reference error
Theme.model_rebuild()
User.model_rebuild()
ThemeUserLink.model_rebuild()
