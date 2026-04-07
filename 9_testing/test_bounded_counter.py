# doctest - создайте файл test_bounded_counter.py и реализуйте в нём тестовые функции, покрывающие:

#     Нормальное поведение
#     Проверьте, что счётчик корректно увеличивается, уменьшается, устанавливается и сбрасывается.

#     Граничные случаи
#     Проверьте поведение при достижении верхней и нижней границы, при попытке выйти за них, при передаче начального значения, равного границе.

#     Обработка исключений
#     Убедитесь, что методы выбрасывают ValueError в ожидаемых ситуациях (выход за границы, некорректные параметры конструктора).

#     Операторы + и -
#     Проверьте, что они возвращают новый объект, не изменяют исходные, правильно обрабатывают допустимые и недопустимые суммы/разности.

#     Инициализация
#     Проверьте, что конструктор корректно обрабатывает


import pytest
from bounded_counter import BoundedCounter


class TestBoundedCounter:
    def test_borders(self):
        c1 = BoundedCounter(-2, 10)
        assert c1.get_value() == -2

        c2 = BoundedCounter(-123, 5869, 123)
        assert c2.get_value() == 123

        with pytest.raises(ValueError):
            BoundedCounter(20, 10)

        with pytest.raises(ValueError):
            BoundedCounter(10, 20, 9999)

        with pytest.raises(ValueError):
            BoundedCounter(10, 20, -9999)
    
    def test_increment(self):
        counter = BoundedCounter(-10, 20, -7)
        counter.increment(17)
        assert counter.get_value() == 10

        with pytest.raises(ValueError):
            counter.increment(9999)
        
        with pytest.raises(ValueError):
            counter.increment(-9999)

    def test_decrement(self):
        counter = BoundedCounter(-10, 20, -7)
        counter.decrement(2)
        assert counter.get_value() == -9
        
        with pytest.raises(ValueError):
            counter.decrement(9999)
        
        with pytest.raises(ValueError):
            counter.decrement(-9999)

    def test_set_value(self):
        counter = BoundedCounter(-10, 20, -7)
        counter.set_value(12)
        assert counter.get_value() == 12
        
        with pytest.raises(ValueError):
            counter.set_value(-99999)
        
        with pytest.raises(ValueError):
            counter.set_value(9999)
        
    def test_reset(self):
        counter = BoundedCounter(-10, 20, -7)
        counter.set_value(8)
        assert counter.get_value() == 8
        
        counter.reset()
        assert counter.get_value() == -7

    def test_add(self):
        c1, c2 = BoundedCounter(-10, 20, -7), BoundedCounter(-10, 20, 11)
        c3 = c1 + c2
        assert c3.get_value() == 4
        
        with pytest.raises(ValueError):
            c4 = c2 + c2
        
        with pytest.raises(ValueError):
            c5 = c1 + c1

    def test_sub(self):
        c1, c2 = BoundedCounter(-10, 20, -7), BoundedCounter(-10, 20, 11)
        c3 = c2 - c1
        assert c3.get_value() == 18
        
        with pytest.raises(ValueError):
            c4 = c1 - c2
        
        with pytest.raises(ValueError):
            c5 = c2 - c1 - c1

    def test_init(self):
        with pytest.raises(TypeError):
            BoundedCounter("lol", "kek", [1, 9, 8, 4])

        with pytest.raises(TypeError):
            BoundedCounter("lol", b"kek", [1, 9, 8, 4])
        
        with pytest.raises(TypeError):
            BoundedCounter("lol", b"kek", [1, 9, 8, 4], (34, 69))
