import sys
import math
import csv
from tables import STANDARD_VALUES, get_error, interpretation, get_BHN, get_k_from_bhn, get_bhn_from_k


def module(s_d, Y, z, N, power, Cv=0.5, k=10):
    Mt = (9.55 * 10**6 * power) / N
    return (2 * Mt) / (s_d * Cv * k * Y * z)


def form_factor(z):
    return (0.154 - (0.912 / int(z)))


def m_standard(m, values):
    return next(value for value in values if m < value)


power = float(input("Enter power in KW: "))


n1 = n2 = 'n'
while n1 == 'n' and n2 == 'n':
    n1 = input("Enter N1 (press n/N to skip): ").lower()
    n2 = input("Enter N2 (press n/N to skip): ").lower()
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


z1 = z2 = 'n'
while z1 == 'n' and z2 == 'n':
    z1 = input("Enter Z1 (press n/N to skip): ").lower()
    z2 = input("Enter Z2 (press n/N to skip): ").lower()
    if z1 == z2 == 'n':
        print("Invalid! z1 or z2 required!")

if z1 == 'n' or z2 == 'n':
    if z1 == 'n':
        z2 = int(z2)
        z1 = z2 / vr
    else:
        z1 = int(z1)
        z2 = vr * z1
else:
    z1, z2 = float(z1), float(z2)


s_d1 = float(
    input("Enter value of allowable stress of pinion from DHB in MPa: "))
s_d2 = float(
    input("Enter value of allowable stress of gear from DHB in MPa: "))


y1 = form_factor(z1)
y2 = form_factor(z2)


if (s_d1 == s_d2) or (s_d1 * y1 < s_d2 * y2):
    print("Pinion is weaker")
    Y, z, s_d, N = y1 * math.pi, z1, s_d1, n1
else:
    print("Gear is weaker")
    Y, z, s_d, N = y2 * math.pi, z2, s_d2, n2


m = module(s_d, Y, z, N, power) ** (1/3)
m = m_standard(m, STANDARD_VALUES)

d1 = m*z1
d2 = m*z2

if (s_d1 == s_d2) or (s_d1 * y1 < s_d2 * y2):
    d = d1
else:
    d = d2

b = 10*m

Mt = (9.55 * 10**6 * power) / N
Ft = 2*Mt / d
v = math.pi * d * N / 60

if v < 8:
    Cv = 3.05 / (3.05 + v)
elif 8 <= v < 13:
    Cv = 4.58 / (4.58 + v)
elif 13 <= v < 20:
    Cv = 6.1 / (6.1 + v)
else:
    Cv = 5.55 / (5.55 + math.sqrt(v))

s_d_ind = Ft/(Cv*b*Y*m)

if s_d_ind > s_d:
    m = m_standard(m, STANDARD_VALUES)
    d1 = m*z1
    d2 = m*z2
    b = 10*m


k3 = 20.67

error = get_error(v)
C = interpretation(error, '1')  # Table given in csv
# C = float(input(f"Enter C from DHB for velocity = {v}: "))
Fd = Ft + (k3 * v * (C * b + Ft)) / (k3 * v + math.sqrt(C * b + Ft))

Q = 2*d2 / (d2+d1)
bhn1 = get_BHN(s_d1)
bhn2 = get_BHN(s_d2)
# K = float(input("Enter K from DHB: "))  # Get k from matlab
material = 'steel-steel'  # Read from input file
K = get_k_from_bhn(bhn1, bhn2, material)

Fw = d1 * b * Q * K

if Fw <= Fd:
    K = Fd / (d1 * b * Q)
    bhn1, bhn2 = get_bhn_from_k(K, material)
    # Get bhn1 bhn2, see tables.py TODO
# else:
#     # bhn1, bhn2 , no change

#     # print()


print("N1: ", n1)
print("N2: ", n2)
print("Z1: ", z1)
print("Z2: ", z2)
print("SD1: ", s_d1)
print("SD2: ", s_d2)
print("Velocity Ratio:", vr)

print("Value of m is: ", m)
print("standardized m value is: ", m_standard(m, STANDARD_VALUES))


# def interpretation(error, table):
#     if error in table:
#         return table[error]

#     if error < 0.01 or error > 0.05:
#         return print("Invalid error. Please check the input!")

#     E1 = math.floor(error*100)
#     E2 = math.ceil(error*100)
#     E1, E2 = E1/100, E2/100
#     while E1 not in table:
#         E1 -= 0.01

#     while E2 not in table:
#         E2 += 0.01

#     C1 = table[E1]
#     C2 = table[E2]

#     return ((error-E1) * (C2-C1) / (E2-E1)) + C1

roh = 1000  # get from input TODO
weight = ((math.pi * d1 ** 2 * b * roh) / 4) + \
    ((math.pi * d2 ** 2 * b * roh) / 4)
