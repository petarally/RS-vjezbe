def isPrime(broj):
    if broj <= 1:
        return False
    for i in range(2, int(broj**0.5) + 1):
        if broj % i == 0:
            return False
    return True

print(isPrime(7)) 
print(isPrime(10))


def primes_in_range(start, end):
    primes = []
    for num in range(start, end + 1):
        if isPrime(num):
            primes.append(num)
    return primes

print(primes_in_range(1, 10))