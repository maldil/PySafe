from codewatchers.errors.ierror import IError


class PyLintError(IError):
    def __init__(self, key, issue: str, lineno: int):
        super().__init__(key)
        self.issue = issue
        self.lineno = lineno

    def get_line_number(self):
        return self.lineno

    def get_key(self):
        return self.key

    def get_issue(self):
        return self.issue

    def __eq__(self, other):
        if isinstance(other, PyLintError):
            return other.get_key() == self.get_key()
        return False

    def __repr__(self):
        return f"PyLintError(key : {self.get_key()}, issue: {self.issue}, lineno: {self.lineno})"

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((type(self), self.get_key()))
