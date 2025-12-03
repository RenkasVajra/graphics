import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify, sympify
from math import sin, cos

x = symbols('x')
func1_str = "0.98**x*sin(2*x)"
func2_str = "0.98**x*sin(5*x)"

# Преобразование строковых формул в символьные выражения
func1 = sympify(func1_str)
func2 = sympify(func2_str)

# Преобразование формул в функции, которые можно вычислить
func1_lambda = lambdify(x, func1, 'numpy')
func2_lambda = lambdify(x, func2, 'numpy')

# Генерация точек для построения графика
x_values = np.linspace(-10, 10, 400)
y1_values = func1_lambda(x_values)
y2_values = func2_lambda(x_values)

# Построение графиков
plt.figure(figsize=(10, 6))

# График первой функции
plt.plot(x_values, y1_values, label=f'f(x) = {func1}', marker='o', markersize=5, linestyle='-', color='blue')

# График второй функции
plt.plot(x_values, y2_values, label=f'f(x) = {func2}', marker='s', markersize=5, linestyle='--', color='red')

# Настройка осей и меток
plt.title('Графики функций')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()

# Отображение графика
plt.show()
