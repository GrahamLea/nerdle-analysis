import sys
from typing import List, Generator

"""
Finds all valid Nerdle words

See: https://nerdlegame.com/

Usage: python3 all_valid_nerdles.py | tee all-nerdles.txt
"""

nerdle_length = 8
include_nerdles_with_no_operator = False

max_expression_length = nerdle_length - 2
numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
numbers_sorted = sorted(numbers)
operators_sorted = ["+", "-", "*", "/"]
operators = set(operators_sorted)


def remove_leading_zeros(expression: str) -> str:
    result = []
    while len(expression):
        c = expression[0]
        expression = expression[1:]
        if c != "0":
            result.append(c)
        else:
            if len(expression) == 0:  # Last character is 0
                result.append(c)
            elif expression[0] not in numbers:  # 0 is followed by a non-number
                result.append(c)
            elif len(result) != 0 and result[-1] in numbers:  # 0 is preceded by a number
                result.append(c)

    return "".join(result)


def is_valid_nerdle(nerdle: str) -> bool:
    """
    Determine whether a given Nerdle word is valid, i.e. the result of evaluating the left side is equal to the right
    side.

    :param nerdle: A syntactically-correct Nerdle word (syntax is not checked in this fn, aside from '=' being expected)

    :return: True if the Nerdle word is valid, otherwise False
    """

    # Get the expression (left) and the result (right)
    try:
        expression, result = nerdle.split("=")
    except ValueError:
        print(f"Bad nerdle: {nerdle}", file=sys.stderr)
        raise

    # Because we use eval(), and Python 3 doesn't allow leading 0s, we have to remove them first

    # Remove leading zeros and evaluate the expression
    try:
        expression_value = eval(remove_leading_zeros(expression))
    except ZeroDivisionError:
        return False

    # Trim leading zeros from the right and evaluate it
    while result[0] == "0" and len(result) > 1:
        result = result[1:]
    result_value = int(result)

    # Valid if the value of the two sides are equal
    return expression_value == result_value


def all_valid_nerdles(partial_nerdle: List[str]) -> Generator[str, None, None]:
    """
    Takes a partial Nerdle word and (recursively) generates all valid Nerdle words that start with the given characters.

    Rather than using a simplistic, brute-force approach of trying all characters in all positions, this function
    contains sufficient rules to only create Nerdle strings which are syntactically correct, with the exception that it
    may create words that divide by zero.
    It then uses :func:`is_valid_nerdle` to determine if the Nerdle word is actually valid (i.e. the left side equals
    the right side, and doesn't divide by zero).

    :param partial_nerdle: a list of characters from which to generate valid Nerdle words

    :return: a generator that yields all valid Nerdle words
    """

    if len(partial_nerdle) == nerdle_length - 1:
        for n in numbers:
            nerdle = "".join(partial_nerdle) + n
            if is_valid_nerdle(nerdle):
                yield nerdle

    else:
        next_possible_chars: List[str]
        in_expression = "=" not in partial_nerdle
        if not in_expression:
            next_possible_chars = numbers_sorted
        else:
            operator_present = any([c in operators for c in partial_nerdle])

            # Must start with a number
            if len(partial_nerdle) == 0:
                next_possible_chars = numbers_sorted

            # Operator must be followed by a number
            elif partial_nerdle[-1] in operators:
                next_possible_chars = numbers_sorted

            # If there's two spaces left and no equals yet, it MUST be =
            elif len(partial_nerdle) == max_expression_length:
                next_possible_chars = ["="]

            # Must have operator as 4th last char if there's no others yet
            elif len(partial_nerdle) == (max_expression_length - 2) and not operator_present:
                next_possible_chars = operators_sorted

            # Last char in expression cannot be an operator
            elif len(partial_nerdle) == max_expression_length - 1:
                next_possible_chars = numbers_sorted + ["="]

            # At this point, we know we are following a number, and aren't forced to insert = or an operator
            else:
                # Only allow '=' if we've already used an operator
                if operator_present or include_nerdles_with_no_operator:
                    next_possible_chars = numbers_sorted + operators_sorted + ["="]
                else:
                    next_possible_chars = numbers_sorted + operators_sorted

        for c in next_possible_chars:
            for n in all_valid_nerdles(partial_nerdle + [c]):
                yield n


for valid_nerdle in all_valid_nerdles([]):
    print(valid_nerdle)
