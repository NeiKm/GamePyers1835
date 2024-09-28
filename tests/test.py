def solve(input_string1: str, input_string2: str) -> str:
    from collections import Counter
    list1 = list(map(int, input_string1.strip().split()))
    list2 = list(map(int, input_string2.strip().split()))
    if Counter(list1) == Counter(list2):
        return "Да"
    else:
        return "Нет"

        

input_string1 = input()
input_string2 = input()
result = solve(input_string1, input_string2)
print(result)

