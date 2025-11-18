import random

def generate_random_bits(length:int)-> int :
    """Generate a random integer of specified bit length with first and last bits set to 1."""
    random_bits= random.getrandbits(length)
    # Ensure first and last bits are set to 1, credit to https://medium.com/@ntnprdhmm/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
    random_bits |= (1 << length - 1) | 1
    return random_bits

def miller_rabin_helper(n:int)-> tuple:
    """Helper function for Miller-Rabin primality test."""
    k=0
    q= n - 1
    while q % 2 == 0:
        k += 1
        q //= 2
    return k, q

def miller_rabin_test(n:int, round)-> bool:
    """Perform Miller-Rabin primality test on n for a given number of rounds."""
    k,q= miller_rabin_helper(n)
    for _ in range(round):
        a= random.randint(2, n - 2)
        x= pow(a, q, n)
        # a^q mod n =1 or a^[(2^j)q] mod n = n-1 when j = 0
        if x == 1 or x == n - 1:
            continue
        for _ in range(k - 1):
            x= pow(x, 2, n)
            if x == n - 1:
                break
            # if its square mod n does equal 1 but it is not equal to n-1 then n is composite
            if x == 1:
                return False
        else:
            return False
    return True
        
def gnerate_large_prime(length:int, round:int)-> int :
    """Generate a large prime number of specified bit length using Miller-Rabin test."""
    while True:
        candidate= generate_random_bits(length)
        if miller_rabin_test(candidate, round):
            return candidate
        
def main():
    length = 256  # Example length
    rounds = 10  # Number of rounds for Miller-Rabin test
    large_prime = gnerate_large_prime(length, rounds)
    print(f"Generated large prime: {large_prime}")
    
if __name__ == "__main__":
    main()