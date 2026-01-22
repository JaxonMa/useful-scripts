#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This script calculates the molar mass of a chemical compound.
# Usage: python MolarMassCalc.py <compound_formula>
# Example: python MolarMassCalc.py H2O
#
# @author: Jaxon Ma

import json
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python MolarMassCalc.py <compound_formula>")
        sys.exit(1)

    compound_formula = sys.argv[1]
    molar_mass = calculate_molar_mass(compound_formula)
    print(f"The molar mass of {compound_formula} is {molar_mass:.2f} g/mol")


def get_atomic_weights() -> dict[str, float]:
    with open("atomic_weights.json", "r") as f:
        atomic_weights = json.load(f)
    return atomic_weights


def calculate_molar_mass(compound_formula: str) -> float:
    composition = parse_chemical_formula(compound_formula)
    atomic_weights = get_atomic_weights()
    molar_mass = 0.0

    for element in composition:
        molar_mass += atomic_weights[element] * composition[element]

    return molar_mass


def parse_chemical_formula(formula: str) -> dict[str, int]:
    composition = {}

    element = ""
    subscript = ""
    for i in range(len(formula)):
        char = formula[i]
        next_char = formula[i + 1] if i < len(formula) - 1 else None

        if char.isupper():
            element = element + char
            if next_char is None:
                composition[element] = 1
                element = ""
                subscript = ""
        elif char.islower():
            element = element + char
            if next_char is None:
                composition[element] = 1
                element = ""
                subscript = ""

        elif char.isdigit():
            subscript = subscript + char

            if next_char is not None:
                if next_char.isdigit():
                    continue
                elif next_char.isalpha():
                    composition[element] = int(subscript)
                    element = ""
                    subscript = ""
                else:
                    raise Exception("Invalid chemical formula, please recheck.")
            else:
                composition[element] = int(subscript)
                element = ""
                subscript = ""

    return composition


if __name__ == "__main__":
    main()
