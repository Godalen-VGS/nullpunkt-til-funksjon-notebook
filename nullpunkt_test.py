import math
import random

import pytest

from notebook_loader import last_notebook

nullpunkt = last_notebook("nullpunkt")

INGEN = "Funksjonen har ingen nullpunkter!"

# Faste tilfeller med heltall, så tilfellet med én løsning er eksakt
TO = [(1, -5, 6), (1, 0, -4), (2, -3, -5), (-1, 2, 3), (1, 1, -1), (3, -2, -7), (1, -3, 0)]
EN = [(1, -4, 4), (2, 4, 2), (-3, 6, -3), (1, 0, 0), (4, -4, 1), (9, 6, 1)]
INGEN_TILFELLER = [(1, 2, 5), (-2, 1, -3), (1, 0, 1), (5, -2, 1)]


def _naer_avrundingsgrense(x):
    # Røtter som 1.005 kan avrundes ulikt avhengig av hvordan formelen er skrevet
    return abs((abs(x) * 100) % 1 - 0.5) < 1e-6


def _tilfeldige(antall, seed=2025):
    rng = random.Random(seed)
    tilfeller = []
    while len(tilfeller) < antall:
        a = rng.randint(-100, 100) / 10
        b = rng.randint(-100, 100) / 10
        c = rng.randint(-100, 100) / 10
        d = b**2 - 4*a*c
        if a == 0 or abs(d) < 1e-6:
            continue
        if d > 0 and any(_naer_avrundingsgrense((-b + s * math.sqrt(d)) / (2*a)) for s in (1, -1)):
            continue
        tilfeller.append((a, b, c))
    return tilfeller


def fasit(a, b, c):
    d = b**2 - 4*a*c
    if d > 0:
        return (round((-b + math.sqrt(d)) / (2*a), 2), round((-b - math.sqrt(d)) / (2*a), 2))
    if d == 0:
        return round(-b / (2*a), 2)
    return INGEN


def sjekk(svar, forventet):
    # To løsninger godtas i hvilken som helst rekkefølge, som tuppel eller liste
    if isinstance(forventet, tuple):
        assert isinstance(svar, (tuple, list)) and len(svar) == 2, f"forventet to løsninger, fikk {svar!r}"
        assert sorted(svar) == sorted(forventet)
    else:
        assert svar == forventet


@pytest.mark.parametrize("a,b,c", TO + EN + INGEN_TILFELLER + _tilfeldige(30))
def test_nullpunkt(a, b, c):
    sjekk(nullpunkt.nullpunkt(a, b, c), fasit(a, b, c))
