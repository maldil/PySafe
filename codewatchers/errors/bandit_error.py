from codewatchers.errors.ierror import IError


class BanditError(IError):
    def __init__(self, key: str, issue: str, severity: str, confidence: str, lineno: int):
        super().__init__(key)
        self.issue = issue
        self.severity = severity
        self.confidence = confidence
        self.lineno = lineno

    def get_key(self):
        return self.issue

    def get_issue(self):
        return self.issue

    def get_line_number(self):
        return self.lineno

    def __eq__(self, other):
        if isinstance(other, BanditError):
            return self.get_key() == other.get_key()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((type(self), self.get_key()))

    def __repr__(self):
        return f"BanditError(key={self.key}, issue={self.issue}, " \
               f"severity={self.severity}, confidence={self.confidence}, lineno={self.lineno})"
