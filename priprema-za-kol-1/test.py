x = [[12313, 123, 23, 12], [123, 123, 12, 3], [123, 12, 3, 1], [12, 3, 1, 0]]

z = 0
for i in x:
    z += len(i)
print(z)


t = (lambda x: sum(len(i) for i in x))(x)
print(t)