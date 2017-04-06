from fractions import gcd

def fizz_buzz(x, fizz=3, buzz=5):
    lcm = fizz * buzz / gcd(fizz, buzz)
    if x % lcm == 0:
        return "fizzbuzz"
    elif x % fizz == 0:
        return "fizz"
    elif x % buzz == 0:
        return "buzz"
    return str(x)