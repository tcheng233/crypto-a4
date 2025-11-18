import random


def generate_random_bits(length: int) -> int:
    """Generate a random integer of specified bit length with first and last bits set to 1."""
    random_bits = random.getrandbits(length)
    # Ensure first and last bits are set to 1, credit to https://medium.com/@ntnprdhmm/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
    random_bits |= (1 << length - 1) | 1
    return random_bits


def miller_rabin_helper(n: int) -> tuple:
    """Helper function for Miller-Rabin primality test."""
    k = 0
    q = n - 1
    while q % 2 == 0:
        k += 1
        q //= 2
    return k, q


def miller_rabin_test(n: int, round) -> bool:
    """Perform Miller-Rabin primality test on n for a given number of rounds."""
    k, q = miller_rabin_helper(n)
    for _ in range(round):
        a = random.randint(2, n - 2)
        x = pow(a, q, n)
        # a^q mod n =1 or a^[(2^j)q] mod n = n-1 when j = 0
        if x == 1 or x == n - 1:
            continue
        for _ in range(k - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
            # if its square mod n does equal 1 but it is not equal to n-1 then n is composite
            if x == 1:
                return False
        else:
            return False
    return True

def gnerate_large_prime(length: int, round: int) -> int:
    """Generate a large prime number of specified bit length using Miller-Rabin test."""
    while True:
        candidate = generate_random_bits(length)
        if miller_rabin_test(candidate, round):
            return candidate

def generate_blum_prime(length: int, rounds: int) -> int:
    while True:
        large_prime = gnerate_large_prime(length, rounds)
        if large_prime % 4 == 3:
            return large_prime

def generate_blum_seed(n: int) -> int:
    while True:
        s = random.randint(2, n - 1)
        if gcd(n, s) == 1:
            return s

def blum_blum_shub(n: int, x_last: int, length: int) -> int:
    blum_output = 0
    for _ in range(length):
        x_i = pow(x_last, 2, n)
        bi = x_i % 2
        blum_output = (blum_output << 1) | bi
        x_last = x_i
    return blum_output, x_last


def generate_rsa_prime(n, x_last, length: int, rounds: int):
    while True:
        candidate_prime, x_last = blum_blum_shub(n, x_last, length)
        # Force msb and lsb to 1 so it is length size candidate prime
        candidate_prime |= (1 << (length - 1)) | 1
        if miller_rabin_test(candidate_prime, rounds):
            return candidate_prime, x_last

def task1():
    length = 256
    rounds = 10
    p = generate_blum_prime(length, rounds)
    q = generate_blum_prime(length, rounds)
    n = p * q
    seed = generate_blum_seed(n)
    x_last = seed
    prime1, x_last = generate_rsa_prime(n, x_last, length, rounds)
    prime2, x_last = generate_rsa_prime(n, x_last, length, rounds)
    while prime1 == prime2:
        prime2, x_last = generate_rsa_prime(n, x_last, length, rounds)
    print(f"[+] Prime numbers are {prime1}")
    print(f"[+] Prime numbers are {prime2}")


def gcd(a, b):
    a, b = abs(a), abs(b)
    if a > b:
        b, a = a, b
    if b == 0:
        return a
    remainder = a % b
    while remainder > 0:
        a, b = b, remainder
        remainder = a % b
    return b

def main():
    task1()

if __name__ == "__main__":
    main()
