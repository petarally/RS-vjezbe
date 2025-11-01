a = float(input("Unesite prvi broj: "))
b = float(input("Unesite drugi broj: "))
operator = input("Unesite operator (+, -, *, /): ")

if operator == "+":
    rezultat = a + b
    print(f"Rezultat operacije {a} {operator} {b} = {rezultat}")
elif operator == "-":
    rezultat = a - b
    print(f"Rezultat operacije {a} {operator} {b} = {rezultat}")
elif operator == "*":
    rezultat = a * b
    print(f"Rezultat operacije {a} {operator} {b} = {rezultat}")
elif operator == "/":
    if b == 0.0:
        print("Dijeljenje s nulom nije dozvoljeno!")
    else:
        rezultat = a / b
        print(f"Rezultat operacije {a} {operator} {b} = {rezultat}")
else:
    print("Nepodržani operator!")