import math

STANDARD_VALUES = [1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0,
                   10.0, 12.0, 16.0, 20.0, 25.0, 32.0, 40.0, 50.0]

velocity_error_map = {1.0: 0.096,
                      2.0: 0.88,
                      2.5: 0.84,
                      3.0: 0.0785,
                      4.0: 0.0710,
                      5.0: 0.0640,
                      6.0: 0.0590,
                      8.0: 0.05,
                      10.0: 0.0386,
                      12.0: 0.033,
                      15.0: 0.023,
                      20.0: 0.0155,
                      25.0: 0.013,
                      26.0: 0.0127}

error_range = [0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15]
st_ci = [75.8, 151.6, 227.4, 303.2, 454.8, 606.4, 758.1, 909.7, 1137.1]
ci_ci = [55.2, 110.4, 165.6, 220.9, 331.3, 441.7, 552.1, 662.5, 828.2]
st_st = [110.3, 220.6, 330.9, 441.3, 662.0, 882.6, 1103.2, 1323.9, 1654.9]

material_map = {'steel-steel': st_st, 'steel-ci': st_ci, 'ci-ci': ci_ci}


def interpretation(error, table):
    if error in table:
        return table[error]

    if error < 0.01 or error > 0.05:
        return print("Invalid error. Please check the input!")

    E1 = math.floor(error*100)
    E2 = math.ceil(error*100)
    E1, E2 = E1/100, E2/100
    while E1 not in table:
        E1 -= 0.01

    while E2 not in table:
        E2 += 0.01

    C1 = table[E1]
    C2 = table[E2]

    return ((error-E1) * (C2-C1) / (E2-E1)) + C1


def get_error(v, table=velocity_error_map):
    if v in table:
        return table[v]

    if v < 1.0 or v > 26.0:
        return print("Invalid velocity. Please check the input!")

    v1 = math.floor(v)
    while v1 not in table:
        v1 -= 1

    return table[v1]


def dynamic_factor(error, material_choice):
    material = material_map[material_choice]
    mapping = dict(zip(error_range, material))
    return interpretation(error, mapping)


def get_BHN(s_d):
    mapping = {47.1: 200, 56.4: 225, 78.5: 300, 138.3: 180, 193.2: 250, 68.7: 80, 82.4: 100, 152: 180, 172.6: 150,
               220: 200, 220.6: 300, 207: 150, 233.4: 200, 345.2: 650, 462: 400, 516.8: 450}

    return mapping[s_d]


def get_k_from_bhn(bhn1, bhn2, material):
    st_st = {(150, 150): 0.205,
             (200, 150): 0.294,
             (250, 150): 0.402,
             (200, 200): 0.402,
             (250, 200): 0.520,
             (300, 300): 0.657,
             (250, 250): 0.657,
             (300, 250): 0.814,
             (350, 250): 0.990,
             (300, 300): 0.990,
             (350, 300): 1.177,
             (400, 300): 1.275,
             (350, 350): 1.383,
             (400, 350): 1.598,
             (450, 350): 1.716,
             (450, 450): 2.363,
             (500, 450): 2.500,
             (600, 450): 2.648,
             (500, 500): 2.952,
             (600, 600): 4.325
             }

    st_ci = {(150, 180): 0.304,
             (200, 180): 0.598,
             (250, 180): 0.990
             }

    ci_ci = {(180, 180): 1.324}

    print({v: k for k, v in st_st.items()})
    print({v: k for k, v in st_ci.items()})
    print({v: k for k, v in ci_ci.items()})

    material_map = {'steel-steel': st_st, 'steel-ci': st_ci, 'ci-ci': ci_ci}

    return material_map[material][(bhn1, bhn2)]


def get_bhn_from_k(k, material):
    st_st = {0.205: (150, 150), 0.294: (200, 150), 0.402: (200, 200),
             0.52: (250, 200), 0.99: (350, 250), 0.657: (250, 250),
             0.814: (300, 250), 1.177: (350, 300), 1.275: (400, 300),
             1.383: (350, 350), 1.598: (400, 350), 1.716: (450, 350),
             2.363: (450, 450), 2.5: (500, 450), 2.648: (600, 450),
             2.952: (500, 500), 4.325: (600, 600)
             }

    st_ci = {0.304: (150, 180), 0.598: (200, 180), 0.99: (250, 180)}

    ci_ci = {1.324: (180, 180)}

    material_map = {'steel-steel': st_st, 'steel-ci': st_ci, 'ci-ci': ci_ci}

    return material_map[material][k]
