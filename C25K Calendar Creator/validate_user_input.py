def validate_user_input(user):
    """
    Unified input validation for both CLI and GUI. Raises ValueError on invalid input.
    """
    # Name
    name = user.get("name", "").strip()
    if not name:
        raise ValueError("Name is required.")
    # Age
    try:
        age = int(user.get("age"))
        if not (5 <= age <= 120):
            raise ValueError
    except Exception:
        raise ValueError("Please enter a valid age (5-120).")
    # Weight
    try:
        weight = float(user.get("weight"))
        if not (30 <= weight <= 500):
            raise ValueError
    except Exception:
        raise ValueError("Please enter a valid weight (30-500 lbs/kg).")
    # Gender
    gender = user.get("gender", "").lower()
    if gender not in ("male", "female", "other"):
        raise ValueError("Gender must be 'male', 'female', or 'other'.")
    # Unit
    unit = user.get("unit", "").lower()
    if unit not in ("i", "m"):
        raise ValueError("Unit must be 'i' (imperial) or 'm' (metric).")
    # Time
    try:
        hour = int(user.get("hour"))
        minute = int(user.get("minute"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError
    except Exception:
        raise ValueError("Session time must be in HH:MM 24-hour format.")
    # Language
    lang = user.get("lang", "").lower()
    if lang not in ("e", "s"):
        raise ValueError("Language must be 'e' (English) or 's' (Spanish).")
    # Export
    export = user.get("export", "").lower()
    if export not in ("i", "c", "j", "g", "m"):
        raise ValueError("Export must be one of: i, c, j, g, m.")
    # Weeks
    try:
        weeks = int(user.get("weeks"))
        if not (1 <= weeks <= 52):
            raise ValueError
    except Exception:
        raise ValueError("Weeks must be between 1 and 52.")
    # Days per week
    try:
        days_per_week = int(user.get("days_per_week"))
        if not (1 <= days_per_week <= 7):
            raise ValueError
    except Exception:
        raise ValueError("Days per week must be between 1 and 7.")
    # Alert minutes
    try:
        alert_minutes = int(user.get("alert_minutes", 30))
        if not (0 <= alert_minutes <= 1440):
            raise ValueError
    except Exception:
        raise ValueError("Alert minutes must be between 0 and 1440.")
    # Rest days
    rest_days = user.get("rest_days", ["Sat", "Sun"])
    if not isinstance(rest_days, list) or not all(isinstance(d, str) and d for d in rest_days):
        raise ValueError("Rest days must be a list of day names.")
    # All good
    return True
