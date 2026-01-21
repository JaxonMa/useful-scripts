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
    for i in range(len(formula)):
        char_1 = formula[i]
        char_2 = formula[i + 1]

        element = ""
        num = 0

        if char_1.isupper():
            # Valid beginning of a element symbol
            if char_2.isalpha():
                if char_2.islower():
                    # char_1 + char_2 is a symbol of an element, get its subscirpt in follow-up loops
                    element = char_1 + char_2
                    composition[element] = num

                elif char_2.isupper():
                    # char_2 is another elemnt, and its subscript is 1
                    element = char_1
                    composition[element] = 1

                elif char_2.isdigit():
                    # char_2 is a subscript
                    index_of_last_num = i
                    for j in range(i, len(formula)):
                        # Get all subscript of the element parsed before
                        next_char = get_next_num(j, formula)
                        if next_char is None:
                            break
                        else:
                            index_of_last_num = j
                    num = formula[i : index_of_last_num + 1]
                    last_key = list(composition)
                    composition[last_key] = num

                else:
                    raise Exception("Invalid chemical formula, please recheck.")

        elif char_1.islower():
            # char_1 is part of a element symbol, it should be parsed in the last loop
            continue
        elif char_1.isdigit():
            # char_1 is part of a subscript, it should be parsed in loops before
            continue
        else:
            raise Exception("Invalid chemical formula, please recheck.")

    return composition


def get_next_num(i: int, string: str) -> int | None:
    """Get the next number according to the index given of the string

    @param: i: index of the string
    @param: string: target string to be analysed
    """
    if len(string) == 0 or len(string) == i:
        return None

    if string[i + 1].isdigit():
        return int(string[i + 1])
    else:
        return None


if __name__ == "__main__":
    main()
