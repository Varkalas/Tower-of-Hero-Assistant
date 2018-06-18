from decimal import Decimal
import re

if __name__ == "__main__":
    summon = "900K293"
    money = "2,582"
    print(re.findall(r"\d+([a-zA-Z]+)\d+[a-zA-Z]+", money))
    print("\n")
    print(re.findall(r"\d+[a-zA-Z]+\d+([a-zA-Z]+)", money))
    if not re.findall(r"\d+[a-zA-Z]+\d+([a-zA-Z]+)", money):
        print("Yes")
    print(re.findall(r"(\d+)[a-zA-Z]+\d+", summon))
    print(re.findall(r"(\d+)[a-zA-Z]+\d+", summon)[0])
    test_1 = "5K200"
    print(re.findall(r"\d+([a-zA-Z]+)\d+", test_1)[0])
    if re.findall(r"\d+([a-zA-Z]+)\d+", test_1)[0] == "K":
        print("Good")
    test_2 = "5K100"
    print(re.findall(r"\d+[K](\d+)", test_2)[0])
    print(re.findall(r"([a-zA-Z])", test_2)[0])
    test_3 = "5M100K"
    if not re.findall(r"\d+[K](\d+)", test_3):
        print("Fantastic")
    test_4 = "5ad150ac"

    print(len(re.findall(r"\d+[a-zA-Z]+\d+([a-zA-Z]+)", test_4)[0]))
    print(re.findall(r"\d+[a-zA-Z]+\d+([a-zA-Z]+)", test_4)[0][0])
    print(re.findall(r"\d+[a-zA-Z]+\d+([a-zA-Z]+)", test_4)[0][1])

    a_number_string = "900000000000000000000000"
    print("%.3E" % Decimal(a_number_string))

    test_5 = "2ar582aq"
    some_text = ""
    incremental_format_first_letters = re.findall(r"\d+([a-zA-Z]+)\d+", some_text)
    if not incremental_format_first_letters:
        print("Yes")
