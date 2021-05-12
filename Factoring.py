#file: Factoring.py
#authors: Kamiel Fokkink, Bram Mak

#This code tries to factor the number N, after the phase s/r has been found

from math import gcd
from fractions import Fraction

def factoring(phase, a):
    N = 15
    frac = Fraction(phase).limit_denominator(15)
    s, r = frac.numerator, frac.denominator
    if phase != 0:
        guesses = [gcd(a**(r//2)-1, N), gcd(a**(r//2)+1, N)]
        print("Guessed Factors: %i and %i" % (guesses[0], guesses[1]))