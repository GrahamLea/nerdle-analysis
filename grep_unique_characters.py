import sys

"""
Greps from a list of Nerdle words only those words which contain no repeated characters.

Usage: python3 grep_unique_characters.py < all-nerdles.txt | tee unique-char-nerdles.txt
"""

for line in sys.stdin.readlines():
    line = line.replace(" ", "").strip()
    has_repeats = False
    for c in line:
        if line.count(c) > 1:
            has_repeats = True
            break
    if not has_repeats:
        print(line)
