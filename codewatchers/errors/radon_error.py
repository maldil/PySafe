from codewatchers.errors.ierror import IError


class NoLineNumber(Exception):
    pass


class RadonError(IError):
    def __init__(self, key: str, cyclomatic_complexity, maintainability_index, halstead_metric):
        super().__init__(key)
        self.cyclomatic = cyclomatic_complexity
        self.maintainability = maintainability_index
        self.halstead = halstead_metric

    def get_key(self):
        return self.key

    def get_line_number(self):
        raise NoLineNumber()

    def get_cyclomatic_complexity(self):
        return self.cyclomatic

    def get_maintainability_index(self):
        return self.maintainability

    def get_halstead_metric(self):
        return self.halstead

    def __eq__(self, other):
        if isinstance(other, Radon):
            return other.get_key() == self.get_key()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((type(self), self.get_key()))

    def __repr__(self):
        return f"Radon(key : {self.get_key()}, cyclomatic: {self.cyclomatic}, maintainability: {self.maintainability}" \
               f", halstead: {self.halstead})"
