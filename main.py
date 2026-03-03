import math


# Global constants (model coefficients)

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

IONIC_STRENGTH = 0.056  # Ionic strength (I), used for ionic correction



# Input handling

def control_input():
    """
    Collect and validate user inputs:
    - free_so2: free SO2 in mg/L, allowed range [0, 80]
    - ph:       pH, allowed range [2.8, 4.0] (must be entered with 2 decimals)
    - temp:     temperature in °C, allowed range [0, 40] (must be entered with 2 decimals)
    - alc:      alcohol in %vol, allowed range [0, 20]

    Returns:
        (free_so2, ph, temp, alc)
    """

    # Free SO2 (mg/L)
    while True:
        raw = input("Insert free SO2 value (0-80 mg/L): ").strip()
        try:
            free_so2 = float(raw)
        except ValueError:
            print("Invalid input: please insert a numeric value (e.g. 12.5).")
            continue

        if 0 <= free_so2 <= 80:
            break
        print("Please insert a value between 0 and 80.")

    # pH (2 decimals required)
    while True:
        raw = input("Insert pH value (2.80-4.00): ").strip()
        raw = raw.replace(",", ".")  # accept comma, enforce 2 decimals anyway

        if "." not in raw:
            print("Invalid input: please use exactly 2 decimals (e.g. 3.20).")
            continue

        left, right = raw.split(".", 1)
        if not left.isdigit() or len(right) != 2 or not right.isdigit():
            print("Invalid input: please use exactly 2 decimals (e.g. 3.20).")
            continue

        ph = float(raw)

        if 2.80 <= ph <= 4.00:
            break
        print("Please insert a value between 2.80 and 4.00.")

    # Temperature (°C) (2 decimals required)
    while True:
        raw = input("Insert temperature (0.00-40.00 °C): ").strip()
        raw = raw.replace(",", ".")

        if "." not in raw:
            print("Invalid input: please use exactly 2 decimals (e.g. 20.00).")
            continue

        left, right = raw.split(".", 1)
        if not left.isdigit() or len(right) != 2 or not right.isdigit():
            print("Invalid input: please use exactly 2 decimals (e.g. 20.00).")
            continue

        temp = float(raw)

        if 0.00 <= temp <= 40.00:
            break
        print("Please insert a value between 0.00 and 40.00.")

    # Alcohol (%vol)
    while True:
        raw = input("Insert alcoholic degree (0-20 %vol): ").strip()
        try:
            alc = float(raw)
        except ValueError:
            print("Invalid input: please insert a numeric value (e.g. 11.5).")
            continue

        if 0 <= alc <= 20:
            break
        print("Please insert a value between 0 and 20.")

    return free_so2, ph, temp, alc



# Thermodynamic / model functions

def pKt_quad(temp, alc):
    return N1 + (N2 * temp) + (N3 * alc) - (N4 * (temp ** 2))


def A_quad(temp, alc):
    return (
        M1
        + (M2 * temp)
        + (M3 * alc)
        + (M4 * (temp ** 2))
        + (M5 * (alc ** 2))
    )


def B_quad(temp, alc):
    return (
        Q1
        + (Q2 * temp)
        + (Q3 * alc)
        + (Q4 * (temp ** 2))
        + (Q5 * (alc ** 2))
    )


def ionic_ratio(temp, alc):
    costA = A_quad(temp, alc)
    costB = B_quad(temp, alc)
    sqrtI = math.sqrt(IONIC_STRENGTH)
    return (costA * sqrtI) / (1 + costB * sqrtI)


def pKm(temp, alc):
    dissociation = pKt_quad(temp, alc)
    ratio = ionic_ratio(temp, alc)
    return dissociation - ratio


def mol_SO2(free_so2, ph, temp, alc):
    pkm_value = pKm(temp, alc)
    return free_so2 / (1 + (10 ** (ph - pkm_value)))



# Script entry point

def main():
    free_so2, ph, temp, alc = control_input()
    print("Molecular SO2:", mol_SO2(free_so2, ph, temp, alc))


if __name__ == "__main__":
    main()