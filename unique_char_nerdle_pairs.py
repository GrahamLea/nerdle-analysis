import sys
from collections import defaultdict
from typing import Dict, Set, List

"""
Finds pairs of Nerdle words that have no shared characters.

Usage: python3 unique_char_nerdle_pairs.py < unique-char-nerdles.txt | tee unique-char-pairs.txt
"""

all_nerdles: List[str] = []
nerdles_sets_by_char: Dict[str, Set[str]] = defaultdict(set)

# Categorise Nerdles by contained characters
for line in sys.stdin.readlines():
    nerdle = line.strip()
    all_nerdles.append(nerdle)
    for c in nerdle:
        if c != "=":
            nerdles_sets_by_char[c].add(nerdle)

for nerdle in all_nerdles:
    chars = set(nerdle.replace("=", ""))
    non_pair_sets: List[Set[str]] = [nset for c, nset in nerdles_sets_by_char.items() if c in chars]
    pairs = set()
    for c in [c for c in nerdles_sets_by_char if c not in chars]:
        possible_pairs = nerdles_sets_by_char[c]
        # A possible pair is a pair if it doesn't appear in any of the sets of non-pairs...
        for pair in possible_pairs:
            if not any((pair in s for s in non_pair_sets)):
                pairs.add(pair)
    for pair in pairs:
        print(f"{nerdle} & {pair}")
