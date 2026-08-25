import nullpunkt

import pytest
import random
import math

# (Inkluder nullpunkt-funksjonen her)

def generer_tilfeldige_koeffisienter():
    """ Hjelpefunksjon for å generere tilfeldige koeffisienter. """
    a = random.randint(-100, 100)/10
    if round(a, 2) == 0:
        a += 1
    b = random.randint(-100, 100)/10
    c = random.randint(-100, 100)/10
    if random.randint(1,20) == 1:
        c = b**2 / (4*a)
    return a, b, c
    
@pytest.mark.parametrize("a,b,c", [generer_tilfeldige_koeffisienter() for _ in range(100)])
def test_tilfeldige_nullpunkt(a, b, c):
    """ Tester nullpunkt-funksjonen med tilfeldig genererte koeffisienter. """
    discriminant = b**2 - 4*a*c
    expected = "Funksjonen har ingen nullpunkter!"
    if discriminant > 0:
        expected = (round((-b + math.sqrt(discriminant)) / (2 * a),2), 
                    round((-b - math.sqrt(discriminant)) / (2 * a),2))
    elif discriminant == 0:
        expected = round(-b / (2 * a), 2)
    
    assert nullpunkt.nullpunkt(a, b, c) == expected
