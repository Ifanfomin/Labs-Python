
# doctest сделайте doctest-примеры, которые проверяют:

# создание объекта с разными комбинациями границ и начального значения;

# работу методов increment, decrement, set_value, reset в граничных ситуациях (например, попытка выйти за пределы диапазона);

# корректность работы операторов + и - (включая ситуации, когда результат выходит за границы);

# обработку исключений при некорректных параметрах конструктора.


import doctest


class BoundedCounter:
    """
    Счётчик, значения которого не могут выходить за заданные границы.

    Параметры:
        min_value (int): минимальное допустимое значение (включительно).
        max_value (int): максимальное допустимое значение (включительно).
        initial_value (int, optional): начальное значение. Если не указано,
            устанавливается в min_value.
    """

    def __init__(self, min_value: int, max_value: int, initial_value: int = None):
        """
        
    >>> _ = BoundedCounter(-2, 10)
    >>> _ = BoundedCounter(-123, 5869, 123)

    >>> _ = BoundedCounter(20, 10)
    Traceback (most recent call last):
    ...
    ValueError: min_value must be <= max_value

    >>> _ = BoundedCounter(10, 20, 9999)
    Traceback (most recent call last):
    ...
    ValueError: initial_value out of bounds

    >>> _ = BoundedCounter(10, 20, -9999)
    Traceback (most recent call last):
    ...
    ValueError: initial_value out of bounds

    >>> _ = BoundedCounter("lol", "kek", [1, 9, 8, 4])
    Traceback (most recent call last):
    ...
    ValueError: min_value must be <= max_value

    >>> _ = BoundedCounter("lol", b"kek", [1, 9, 8, 4], (34, 69))
    Traceback (most recent call last):
    ...
    TypeError: BoundedCounter.__init__() takes from 3 to 4 positional arguments but 5 were given"""
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")
        self._min = min_value
        self._max = max_value
        self._initial = initial_value if initial_value is not None else min_value
        if not (self._min <= self._initial <= self._max):
            raise ValueError("initial_value out of bounds")
        self._current = self._initial

    def increment(self, delta: int = 1) -> None:
        """
        Увеличивает текущее значение на delta.
        Если результат превысит max_value, выбрасывает ValueError.

        >>> c = BoundedCounter(-10, 20, -7)
        >>> c.increment(17)
        >>> c.get_value()
        10

        >>> c = BoundedCounter(-10, 20, -7)
        >>> c.increment(9999)
        Traceback (most recent call last):
        ...
        ValueError: Increment would exceed upper bound
        """
        new_value = self._current + delta
        if new_value > self._max:
            raise ValueError("Increment would exceed upper bound")
        self._current = new_value

    def decrement(self, delta: int = 1) -> None:
        """
        Уменьшает текущее значение на delta.
        Если результат станет меньше min_value, выбрасывает ValueError.

        >>> c = BoundedCounter(-10, 20, -7)
        >>> c.decrement(2)
        >>> c.get_value()
        -9

        >>> c = BoundedCounter(-10, 20, -7)
        >>> c.decrement(9999)
        Traceback (most recent call last):
        ...
        ValueError: Decrement would fall below lower bound
        """
        new_value = self._current - delta
        if new_value < self._min:
            raise ValueError("Decrement would fall below lower bound")
        self._current = new_value

    def set_value(self, value: int) -> None:
        """
        Устанавливает новое текущее значение, если оно находится в границах.
        Иначе выбрасывает ValueError.

        >>> c = BoundedCounter(-10, 20, -7)
        >>> c.set_value(12)
        >>> c.get_value()
        12

        >>> c = BoundedCounter(-10, 20, -7)
        >>> c.set_value(9999)
        Traceback (most recent call last):
        ...
        ValueError: Value out of bounds
        """
        if not (self._min <= value <= self._max):
            raise ValueError("Value out of bounds")
        self._current = value

    def reset(self) -> None:
        """
        Сбрасывает счётчик к начальному значению, переданному в конструкторе.

        >>> c = BoundedCounter(-10, 20, -7)
        >>> c.set_value(8)
        >>> c.reset()
        >>> c.get_value()
        -7
        """
        self._current = self._initial

    def get_value(self) -> int:
        """
        Возвращает текущее значение счётчика.

        >>> c = BoundedCounter(0, 5)
        >>> c.get_value()
        0
        """
        return self._current

    def __add__(self, other: 'BoundedCounter') -> 'BoundedCounter':
        """
        Создаёт новый счётчик, текущее значение которого равно сумме текущих
        значений self и other. Границы нового счётчика — те же, что у self.
        Если сумма выходит за эти границы, выбрасывает ValueError.

        >>> c1 = BoundedCounter(-10, 20, -7)
        >>> c2 = BoundedCounter(-10, 20, 11)
        >>> (c1 + c2).get_value()
        4

        >>> c1 = BoundedCounter(-10, 20, 11)
        >>> c2 = BoundedCounter(-10, 20, 11)
        >>> c1 + c2
        Traceback (most recent call last):
        ...
        ValueError: Sum out of bounds
        """
        new_value = self._current + other._current
        if not (self._min <= new_value <= self._max):
            raise ValueError("Sum out of bounds")
        return BoundedCounter(self._min, self._max, new_value)

    def __sub__(self, other: 'BoundedCounter') -> 'BoundedCounter':
        """
        Создаёт новый счётчик, текущее значение которого равно разности текущих
        значений self и other. Границы нового счётчика — те же, что у self.
        Если разность выходит за границы, выбрасывает ValueError.

        >>> c1 = BoundedCounter(-10, 20, 11)
        >>> c2 = BoundedCounter(-10, 20, -7)
        >>> (c1 - c2).get_value()
        18

        >>> c1 = BoundedCounter(-10, 20, -7)
        >>> c2 = BoundedCounter(-10, 20, 11)
        >>> c1 - c2
        Traceback (most recent call last):
        ...
        ValueError: Difference out of bounds
        """
        new_value = self._current - other._current
        if not (self._min <= new_value <= self._max):
            raise ValueError("Difference out of bounds")
        return BoundedCounter(self._min, self._max, new_value)


doctest.testmod()