import pytest


class NotInRangeError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


def test_not_in_range():
    a = 5
    with pytest.raises(NotInRangeError):
        if a not in range(10, 20):
            raise NotInRangeError("value is not in required range")
