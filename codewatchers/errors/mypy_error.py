from codewatchers.errors.ierror import IError


class MyPyError(IError):
    def __init__(self, key, issue: str, lineno: int):
        super().__init__(key)
        self.issue = issue
        self.lineno = lineno

    def get_key(self):
        return self.key

    def get_line_number(self):
        return self.lineno

    def get_issue(self):
        return self.issue

    def __eq__(self, other):
        if isinstance(other, MyPyError):
            return other.get_key() == self.get_key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((type(self), self.get_key()))

    def __repr__(self):
        return f"MyPyError(key={self.key}, issue={self.issue}, lineno={self.lineno})"
