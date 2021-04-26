import sys
import math
import csv
from tables import STANDARD_VALUES, get_error, dynamic_factor


def module(s_d, Y, Cs, power, Cv, Ft, k=10):
    return math.sqrt(Ft/(s_d * Cv * k * Y))


def form_factor(z):
    return (0.154 - (0.912 / int(z)))


def m_standard(m, values):
    return next(value for value in values if m < value)


power = float(input("Enter power in KW: "))


n1 = n2 = 'n'
while n1 == 'n' and n2 == 'n':
    n1 = input("Enter N1 in rpm (press n/N to skip): ").lower()
    n2 = input("Enter N2 in rpm (press n/N to skip): ").lower()
    if n1 == n2 == 'n':
        print("Invalid! n1 or n2 required!")

if n1 == 'n' or n2 == 'n':
    vr = float(input("Enter velocity ratio: "))
    if n1.lower() == 'n':
        n2 = int(n2)
        n1 = vr * n2
    else:
        n1 = int(n1)
        n2 = n1 / vr
else:
    n1, n2 = int(n1), int(n2)
    vr = n1/n2


d1 = d2 = 'n'
while d1 == 'n' and d2 == 'n':
    d1 = input("Enter d1 in mm (press n/N to skip): ").lower()
    d2 = input("Enter d2 in mm (press n/N to skip): ").lower()
    if d1 == d2 == 'n':
        print("Invalid! d1 or d2 required!")

if d1 == 'n' or d2 == 'n':
    if d1 == 'n':
        d2 = int(d2)
        d1 = d2 / vr
    else:
        d1 = int(d1)
        d2 = vr * d1
else:
    d1, d2 = float(d1), float(d2)

s_d1 = float(
    input("Enter value of allowable stress of pinion from DHB in MPa: "))
s_d2 = float(
    input("Enter value of allowable stress of gear from DHB in MPa: "))

# Assume
z1 = 20
z2 = vr * z1

y1 = form_factor(z1)
y2 = form_factor(z2)

Cs = input("Enter service factor (Type n to skip): ").lower()
Cs = 1 if Cs == 'n' else float(Cs)


if (s_d1 == s_d2) or (s_d1 * y1 < s_d2 * y2):
    print("Pinion is weaker")
    Y, d, s_d, N = y1 * math.pi, d1, s_d1, n1
else:
    print("Gear is weaker")
    Y, d, s_d, N = y2 * math.pi, d2, s_d2, n2


v = math.pi * d * N / (60 * 1000)

if v < 8:
    Cv = 3.05 / (3.05 + v)
elif 8 <= v < 13:
    Cv = 4.58 / (4.58 + v)
elif 13 <= v < 20:
    Cv = 6.1 / (6.1 + v)
else:
    Cv = 5.55 / (5.55 + math.sqrt(v))


Ft = 1000 * power * Cs / v
m = module(s_d, Y, Cs, power, Cv, Ft)
m = m_standard(m, STANDARD_VALUES)

z1 = d1/m
z2 = d2/m

b = 10*m


s_d_ind = Ft/(Cv*b*Y*m)

if s_d_ind > s_d:
    m = m_standard(m, STANDARD_VALUES)
    d1 = m*z1
    d2 = m*z2
    b = 10*m


k3 = 20.67
C = float(input(f"Enter C from DHB for velocity = {v} m/s: "))
Fd = Ft + (k3 * v * (C * b + Ft)) / (k3 * v + math.sqrt(C * b + Ft))

Q = 2*d2 / (d2+d1)
K = float(input("Enter K from DHB: "))
Fw = d1 * b * Q * K

if Fw < Fd:
    K = Fd / (d1 * b * Q)


choice = 'z'
while choice not in ['1', '2', '3']:
    print("1. CI and CI")
    print("2. CI and STEEL")
    print("3. STEEL and STEEL")
    choice = input("Select choice: ")

error = get_error(v)
C = dynamic_factor(error, choice)
print("Dynamic Factor C: ", C)
