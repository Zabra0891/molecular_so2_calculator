import math


# Global constants

N1 = 0.655664
N2 = 0.0698386
N3 = 0.02015
N4 = 0.000621693

M1 = 0.482724
M2 = 0.00883782
M3 = 0.004437521
M4 = 0.0000489638
M5 = 0.0000489638

Q1 = 1.61645
Q2 = 0.000935347
Q3 = 0.000479931
Q4 = 0.00000492357
Q5 = 0.0000315093

I = 0.056  # ionic strength



# pKt 

def pKt_quad(temp, alc):
    """Compute pKt using a quadratic model based on temperature and alcohol."""
    return N1 + (N2 * temp) + (N3 * alc) - (N4 * (temp ** 2))



# A and B 

def A_quad(temp, alc):
    """Compute coefficient A using a quadratic model based on temperature and alcohol."""
    return (
        M1
        + (M2 * temp)
        + (M3 * alc)
        + (M4 * (temp ** 2))
        + (M5 * (alc ** 2))
    )


def B_quad(temp, alc):
    """Compute coefficient B using a quadratic model based on temperature and alcohol."""
    return (
        Q1
        + (Q2 * temp)
        + (Q3 * alc)
        + (Q4 * (temp ** 2))
        + (Q5 * (alc ** 2))
    )



# Ionic ratio

def ionic_ratio(temp, alc):
    """Compute the ionic correction ratio using coefficients A and B and ionic strength I."""
    costA = A_quad(temp, alc)
    costB = B_quad(temp, alc)
    sqrtI = math.sqrt(I)
    return (costA * sqrtI) / (1 + costB * sqrtI)



# pKm

def pKm(temp, alc):
    """Compute pKm as pKt minus the ionic correction ratio."""
    dissociation = pKt_quad(temp, alc)
    ratio = ionic_ratio(temp, alc)
    return dissociation - ratio


# Molecular SO2

def mol_SO2(free_so2, pH, temp, alc):
    """Compute molecular SO2 from free SO2 using pH and pKm (temperature/alcohol dependent)."""
    pkm_value = pKm(temp, alc)
    return free_so2 / (1 + (10 ** (pH - pkm_value)))