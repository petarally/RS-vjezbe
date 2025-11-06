# Zbroj svih parnih brojeva od 1 do 100
suma = 0

for i in range(2, 101, 2):
    suma += i

print("Zbroj svih parnih brojeva od 1 do 100 je:", suma)

# Pomoću while petlje
suma = 0
i = 2
while i <= 100:
    suma += i
    i += 2

print("Zbroj svih parnih brojeva od 1 do 100 je:", suma)

# Prvih 10 neparnih brojeva u obrnutom redoslijedu
print("Prvih 10 neparnih brojeva u obrnutom redoslijedu su:")
for i in range(19, 0, -2):
    print(i, end=' ')
print()

# Pomoću while petlje

print("Prvih 10 neparnih brojeva u obrnutom redoslijedu su:")
i = 19
while i > 0:
    print(i, end=' ')
    i -= 2
print()


# Fibonaccijevi brojevi do 1000
a, b = 0, 1
print("Fibonaccijevi brojevi do 1000 su:")
for _ in range(100):
    if a > 1000:
        break
    print(a, end=' ')
    a, b = b, a + b
print()


# Pomoću while petlje

a, b = 0, 1
print("Fibonaccijevi brojevi do 1000 su:")
while a <= 1000:
    print(a, end=' ')
    a, b = b, a + b
print()