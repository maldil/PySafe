from __future__ import annotations
from codewatchers.errors.ierror import IError
from collections import Counter
from typing import List



class AllErrors:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if isinstance(item, IError):
            self.items.append(item)
        else:
            raise ValueError("Can only add ItemClass objects")

    def extend(self, errors: AllErrors):
        self.items.extend(errors.get_all_errors())

    def get_additional_error(self, errors) -> List[IError]:
        diff = []
        for error in errors.get_all_errors():
            if error not in self.items:
                diff.append(error)
        return diff

    def __repr__(self):
        return f"AllErrors(items={self.items})"

    def __eq__(self, other):
        if isinstance(other, AllErrors):
            return Counter(self.items) == Counter(other.items)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_all_errors(self):
        return self.items
