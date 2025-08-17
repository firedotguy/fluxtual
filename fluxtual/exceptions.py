class FlutterError(Exception):
    """Error class used to report Flutter-specific assertion failures and contract violations."""
    def __init__(self, message: str):
        """Create an error message from a string."""
        super().__init__(self._format_message(message))
        self.message = message

    def _format_message(self, msg: str) -> str:
        return f"FlutterError: {msg}"

    def __str__(self):
        return self._format_message(self.message)