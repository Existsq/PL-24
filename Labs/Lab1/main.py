import sys
import math


def get_coef(index, prompt):
    try:
        coef_str = sys.argv[index]
    except IndexError:
        print(prompt)
        coef_str = input()
    coef = float(coef_str)
    return coef


def get_roots(a, b, c):
    result = []

    # Решаем квадратное уравнение относительно y: a * y^2 + b * y + c = 0
    D = b * b - 4 * a * c

    if D < 0:
        # Если дискриминант меньше нуля, действительных корней нет
        return result

    elif D == 0.0:
        # Один корень квадратного уравнения
        y = -b / (2.0 * a)
        if y >= 0:
            result.append(math.sqrt(y))
            result.append(-math.sqrt(y))

    elif D > 0.0:
        # Два корня квадратного уравнения
        sqD = math.sqrt(D)
        y1 = (-b + sqD) / (2.0 * a)
        y2 = (-b - sqD) / (2.0 * a)

        if y1 >= 0:
            result.append(math.sqrt(y1))
            result.append(-math.sqrt(y1))

        if y2 >= 0:
            result.append(math.sqrt(y2))
            result.append(-math.sqrt(y2))

    return result


def main():
    a = get_coef(1, 'Введите коэффициент A:')
    b = get_coef(2, 'Введите коэффициент B:')
    c = get_coef(3, 'Введите коэффициент C:')

    roots = get_roots(a, b, c)

    len_roots = len(roots)
    if len_roots == 0:
        print('Нет корней')
    elif len_roots == 2:
        print('Два корня: {} и {}'.format(roots[0], roots[1]))
    elif len_roots == 4:
        print('Четыре корня: {}, {}, {} и {}'.format(roots[0], roots[1], roots[2], roots[3]))


if __name__ == "__main__":
    main()
