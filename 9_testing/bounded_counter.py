
class BoundedCounter:
    """
    Счётчик, значения которого не могут выходить за заданные границы.

    Параметры:
        min_value (int): минимальное допустимое значение (включительно).
        max_value (int): максимальное допустимое значение (включительно).
        initial_value (int, optional): начальное значение. Если не указано,
            устанавливается в min_value.

    Атрибуты:
        _min (int): нижняя граница.
        _max (int): верхняя граница.
        _current (int): текущее значение.
        _initial (int): значение, на которое выполняется сброс.
    """

    def __init__(self, min_value: int, max_value: int, initial_value: int = None):
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
        """
        new_value = self._current + delta
        if new_value > self._max:
            raise ValueError("Increment would exceed upper bound")
        self._current = new_value

    def decrement(self, delta: int = 1) -> None:
        """
        Уменьшает текущее значение на delta.
        Если результат станет меньше min_value, выбрасывает ValueError.
        """
        new_value = self._current - delta
        if new_value < self._min:
            raise ValueError("Decrement would fall below lower bound")
        self._current = new_value

    def set_value(self, value: int) -> None:
        """
        Устанавливает новое текущее значение, если оно находится в границах.
        Иначе выбрасывает ValueError.
        """
        if not (self._min <= value <= self._max):
            raise ValueError("Value out of bounds")
        self._current = value

    def reset(self) -> None:
        """
        Сбрасывает счётчик к начальному значению, переданному в конструкторе.
        """
        self._current = self._initial

    def get_value(self) -> int:
        """
        Возвращает текущее значение счётчика.
        """
        return self._current

    def __add__(self, other: 'BoundedCounter') -> 'BoundedCounter':
        """
        Создаёт новый счётчик, текущее значение которого равно сумме текущих
        значений self и other. Границы нового счётчика — те же, что у self.
        Если сумма выходит за эти границы, выбрасывает ValueError.
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
        """
        new_value = self._current - other._current
        if not (self._min <= new_value <= self._max):
            raise ValueError("Difference out of bounds")
        return BoundedCounter(self._min, self._max, new_value)
