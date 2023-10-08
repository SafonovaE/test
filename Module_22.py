num_sequence = input("Введите последовательность чисел через пробел: ")
num = int(input("Введите число: "))
list_num_sequence = list(map(int, num_sequence.split()))
list_num_sequence.sort()


def binary_search(array, element, left, right):
    if left > right:
        return -1

    middle = (right + left) // 2
    if element > array[middle]:  
        if middle == left:
            if array[right] < element:
                return right
            else:
                return left
        else:
            return binary_search(array, element, middle, right)
    else:
        return binary_search(array, element, left, middle - 1)


pos = binary_search(list_num_sequence, num, 0, len(list_num_sequence) - 1)
if pos < 0:
    print('no elem')
else:
    print('found pos ' + str(pos))
