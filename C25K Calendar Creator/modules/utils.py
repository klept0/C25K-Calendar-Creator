# --- Utility functions for C25K Calendar Creator ---

from typing import Any, Dict


def anonymize_user(user: Dict[str, Any]) -> Dict[str, Any]:
    if not user.get("anonymize"):
        return user
    anon_user = user.copy()
    anon_user["name"] = "Anonymous"
    anon_user["email"] = ""
    return anon_user


# Add more utility functions as needed
