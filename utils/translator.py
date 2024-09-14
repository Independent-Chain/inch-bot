def language(language_code: str) -> str:
    if language_code not in ["ru", "en"]:
        return "en"
    else:
        return language_code