import re
from typing import List, Tuple, Optional, Iterable


def _require_str(value: str, name: str) -> None:
    """Validate that a value is a non-empty string (whitespace-only allowed if test requires)."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")


def contains_only_alnum(s: str) -> bool:
    """
    Return True if the string contains only a–z, A–Z, or 0–9.
    """
    _require_str(s, "s")
    return re.fullmatch(r"[A-Za-z0-9]*", s) is not None


def match_a_followed_by_b_star(s: str) -> bool:
    """
    Return True if the string matches: 'a' followed by zero or more 'b's (entire string).
    Examples: 'a', 'ab', 'abb', but not 'abc'.
    """
    _require_str(s, "s")
    return re.fullmatch(r"ab*", s) is not None


def match_a_followed_by_b_plus(s: str) -> bool:
    """
    Return True if the string matches: 'a' followed by one or more 'b's (entire string).
    Examples: 'ab', 'abb', but not 'a' or 'abc'.
    """
    _require_str(s, "s")
    return re.fullmatch(r"ab+", s) is not None


def find_lowercase_sequences_joined_by_underscore(s: str) -> List[str]:
    """
    Find sequences of lowercase letters joined by a single underscore.
    Example match: 'aab_cbbbc'; no match if any side has uppercase.
    """
    _require_str(s, "s")
    return re.findall(r"\b[a-z]+_[a-z]+\b", s)


def word_at_beginning(s: str) -> Optional[str]:
    """
    Match a word at the beginning of the string (no leading spaces).
    Returns the word or None if there isn't one.
    """
    _require_str(s, "s")
    m = re.match(r"^\w+", s)
    return m.group(0) if m else None


def words_containing_z(s: str) -> List[str]:
    """
    Return all words that contain the letter 'z' (case-insensitive).
    """
    _require_str(s, "s")
    return re.findall(r"\b\w*z\w*\b", s, flags=re.IGNORECASE)


def remove_leading_zeros_ip(ip: str) -> str:
    """
    Remove leading zeros from each octet in an IPv4 address, preserving single zero.
    Uses regex lookaheads to strip only leading zeros.
    """
    _require_str(ip, "ip")
    return re.sub(r"\b0+(?=\d)", "", ip)


def search_literals(text: str, needles: Iterable[str]) -> List[Tuple[str, bool]]:
    """
    For each literal needle, report whether it occurs in text (True/False).
    """
    _require_str(text, "text")
    results = []
    for n in needles:
        _require_str(n, "needle")
        # Use re.escape to ensure literal search
        found = re.search(re.escape(n), text) is not None
        results.append((n, found))
    return results


def find_literal_positions(text: str, needle: str) -> List[Tuple[int, int]]:
    """
    Find all (start, end) positions where a literal substring occurs in text.
    """
    _require_str(text, "text")
    _require_str(needle, "needle")
    return [(m.start(), m.end()) for m in re.finditer(re.escape(needle), text)]


def spaces_to_underscores(s: str) -> str:
    """
    Replace runs of whitespace with a single underscore.
    """
    _require_str(s, "s")
    return re.sub(r"\s+", "_", s)


def underscores_to_spaces(s: str) -> str:
    """
    Replace underscores with single spaces.
    """
    _require_str(s, "s")
    return re.sub(r"_", " ", s)


def extract_ymd_from_url(url: str) -> Optional[Tuple[str, str, str]]:
    """
    Extract (year, month, day) from a URL path like /YYYY/MM/DD/.
    Returns None if not found.
    """
    _require_str(url, "url")
    m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
    return (m.group(1), m.group(2), m.group(3)) if m else None


def words_starting_with_a_or_e(s: str) -> List[str]:
    """
    Find words that start with 'a' or 'e' (case-insensitive).
    """
    _require_str(s, "s")
    return re.findall(r"\b[aeAE]\w*\b", s)


def replace_space_comma_dot_with_colon(s: str) -> str:
    """
    Replace every occurrence of space, comma, or dot (including runs) with a single colon.
    """
    _require_str(s, "s")
    return re.sub(r"[ ,.]+", ":", s)


def remove_multiple_spaces(s: str) -> str:
    """
    Collapse multiple spaces into a single space (tabs/newlines left intact).
    """
    _require_str(s, "s")
    return re.sub(r" {2,}", " ", s)


def main() -> None:
    # 1
    print("1) Only a-zA-Z0-9:")
    for t in ["ABCDEFabcdef123450", "*&%@#!}{"]:
        print(t, "->", contains_only_alnum(t))
    print()

    # 2
    print("2) a followed by zero or more b's:")
    for t in ["ab", "abc", "a", "ab", "abb"]:
        print(t, "->", match_a_followed_by_b_star(t))
    print()

    # 3
    print("3) a followed by one or more b's:")
    for t in ["ab", "abc", "a", "ab", "abb"]:
        print(t, "->", match_a_followed_by_b_plus(t))
    print()

    # 4
    print("4) lowercase sequences joined by underscore:")
    for t in ["aab_cbbbc", "aab_Abbbc", "Aaab_abbbc"]:
        print(t, "->", find_lowercase_sequences_joined_by_underscore(t))
    print()

    # 5
    print("5) word at beginning:")
    for t in ["The quick brown fox jumps over the lazy dog.",
              " The quick brown fox jumps over the lazy dog."]:
        print(repr(t), "->", word_at_beginning(t))
    print()

    # 6
    print("6) words containing 'z':")
    for t in ["The quick brown fox jumps over the lazy dog.", "Python Exercises."]:
        print(repr(t), "->", words_containing_z(t))
    print()

    # 7
    print("7) remove leading zeros from IP:")
    print("216.08.094.196 ->", remove_leading_zeros_ip("216.08.094.196"))
    print()

    # 8
    print("8) search for literal strings:")
    text8 = "The quick brown fox jumps over the lazy dog."
    for word, found in search_literals(text8, ["fox", "dog", "horse"]):
        print(f"{word!r} -> {found}")
    print()

    # 9
    print("9) literal positions:")
    text9 = "The quick brown fox jumps over the lazy dog."
    print("Positions for 'fox':", find_literal_positions(text9, "fox"))
    print()

    # 10
    print("10) replace spaces<->underscores:")
    print("spaces->underscores:", spaces_to_underscores("Regular Expressions"))
    print("underscores->spaces:", underscores_to_spaces("Code_Examples"))
    print()

    # 11
    print("11) extract Y-M-D from URL:")
    url = ("https://www.washingtonpost.com/news/football-insider/wp/"
           "2016/09/02/odell-beckhams-fame-rests-on-one-stupid-little-ball-"
           "josh-norman-tells-author/")
    print("URL ->", extract_ymd_from_url(url))
    print()

    # 12 & 14
    print("12/14) words starting with 'a' or 'e':")
    t12 = ("The following example creates an ArrayList with a capacity of 50 elements. "
           "Four elements are then added to the ArrayList and the ArrayList is trimmed accordingly.")
    print(words_starting_with_a_or_e(t12))
    print()

    # 13
    print("13) replace space/comma/dot with colon:")
    print(replace_space_comma_dot_with_colon("Python Exercises, PHP exercises."))
    print()

    # 15
    print("15) remove multiple spaces:")
    print(remove_multiple_spaces("Python      Exercises"))
    print()


if __name__ == "__main__":
    main()
