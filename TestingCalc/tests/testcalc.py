import pytest
from app.Calculator import Calculator

class TestCalc:

    def setup_method(self):
        self.calc = Calculator()

    def test_adding_success(self):
        assert self.calc.adding(4, 5) == 9

    def test_multiply_calculate_success(self):
        assert self.calc.multiplication(5, 5) == 25

    def test_division_success(self):
        assert self.calc.division(5, 5) == 1

    def test_subtraction_success(self):
        assert self.calc.subtraction(5, 2) == 3

    def teardown_method(self):
        print('Выполнение метода Teardown')