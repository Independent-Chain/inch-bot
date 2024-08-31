class Markdown:
    @staticmethod
    def bold(text: str) -> str:
        return f"<b>{text}</b>"

    @staticmethod
    def monospaced(text: str) -> str:
        return f"<code>{text}</code>"

    @staticmethod
    def url(text: str, url: str) -> str:
        return f"<a href='{url}'>{text}</a>"