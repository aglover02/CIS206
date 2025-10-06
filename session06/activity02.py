"""
A small command-line utility that either:
  • Encodes an alphabetic string using run-length encoding (RLE) in
    compressed form (omit count of 1; e.g., 'AAABCC' -> 'A3BC2')
OR
  • Decodes an RLE string back to its expanded form (e.g., 'A3BC2' -> 'AAABCC').

Behavior:
    - If the user-entered string contains any digits, the program treats it as
      an RLE string and attempts to decode it.
    - Otherwise, it is treated as a plain alphabetic string and encoded.

Validation:
    - For encoding: input must be a non-empty string of alphabetic characters [A-Za-z].
    - For decoding: input must match valid compressed RLE:
        One or more runs of: a single alphabetic char followed by an optional
        positive integer count (no leading zeros). Examples: "A3BC2", "x12Y".
        Invalid: "3A", "A0", "A01", "A-2", "A 2", "AB3C0".
    - Case is preserved (e.g., 'A' and 'a' are distinct).
"""

from typing import Final
import re


# Precompiled patterns (constants; no mutable global state).
_ALPHA_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z]+$")
# A valid compressed RLE string is one or more (letter, optional positive int) runs.
# Count, when present, must be a positive integer without leading zeros.
_RLE_VALID_RE: Final[re.Pattern[str]] = re.compile(r"^(?:[A-Za-z](?:[1-9]\d*)?)+$")
# For decoding: capture (letter)(digits?) runs across the whole string.
_RLE_RUN_RE: Final[re.Pattern[str]] = re.compile(r"([A-Za-z])(\d*)")


def rle_encode(text: str) -> str:
    """
    Encode a string using compressed run-length encoding (RLE).

    Compressed form omits the count for runs of length 1:
        "AAABCC" -> "A3BC2"
        "abc"    -> "abc"

    Parameter validation:
        - `text` must be a non-empty `str`.
        - Only alphabetic characters [A-Za-z] allowed.
        - Case is preserved.

    Args:
        text: Plain alphabetic string to encode.

    Returns:
        The compressed RLE string.

    Raises:
        TypeError:  If `text` is not a `str`.
        ValueError: If `text` is empty or contains non-alphabetic characters.

    Examples:
        >>> rle_encode("AAABCC")
        'A3BC2'
        >>> rle_encode("AaaBBB")
        'A2aB3'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not text:
        raise ValueError("text must be non-empty")
    if _ALPHA_RE.fullmatch(text) is None:
        raise ValueError("text must contain alphabetic characters only (A–Z or a–z)")

    out: list[str] = []
    cur = text[0]
    cnt = 1

    for ch in text[1:]:
        if ch == cur:
            cnt += 1
        else:
            out.append(cur)
            if cnt > 1:
                out.append(str(cnt))
            cur, cnt = ch, 1

    # Final run
    out.append(cur)
    if cnt > 1:
        out.append(str(cnt))

    return "".join(out)


def rle_decode(text: str) -> str:
    """
    Decode a compressed RLE string to its expanded alphabetic form.

    Valid compressed RLE:
        A sequence of runs where each run is a single letter followed by an
        optional positive integer count (no leading zeros). If count is omitted,
        it implies 1. Example: "A3BC2" -> "AAABCC"; "x12Y" -> "xxxxxxxxxxxxY".

    Parameter validation:
        - `text` must be a non-empty `str`.
        - Must match compressed-RLE syntax (no spaces, no zero/leading-zero counts).

    Args:
        text: The compressed RLE string.

    Returns:
        The expanded alphabetic string.

    Raises:
        TypeError:  If `text` is not a `str`.
        ValueError: If `text` is empty or not valid compressed RLE.

    Examples:
        >>> rle_decode("A3BC2")
        'AAABCC'
        >>> rle_decode("Z")
        'Z'
        >>> rle_decode("a10B2")
        'aaaaaaaaaaBB'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not text:
        raise ValueError("text must be non-empty")
    if _RLE_VALID_RE.fullmatch(text) is None:
        raise ValueError(
            "Invalid compressed RLE. Expected runs like Letter or Letter+Count "
            "(Count is a positive integer without leading zeros)."
        )

    out: list[str] = []
    for letter, digits in _RLE_RUN_RE.findall(text):
        count = int(digits) if digits else 1
        # Though the regex prevents zero, keep a defensive check:
        if count <= 0:
            raise ValueError("RLE counts must be positive integers")
        out.append(letter * count)
    return "".join(out)


def is_rle_string(text: str) -> bool:
    """
    Heuristic to decide whether to decode or encode:
    If the string contains any digit, treat it as RLE (to be decoded).
    This does not guarantee validity; `rle_decode` will still validate strictly.

    Args:
        text: The user-provided string.

    Returns:
        True if any character is a digit; False otherwise.
    """
    return any(ch.isdigit() for ch in text)


def _prompt_string() -> str:
    """
    Prompt the user for a string and return it as-is (leading/trailing
    whitespace stripped). Validation occurs in encode/decode functions.
    """
    while True:
        s = input("Enter a string (alphabetic to encode, or RLE to decode): ").strip()
        if not s:
            print("Invalid input: Input cannot be empty.")
            continue
        # Early-screen spaces/illegal chars for clarity (optional user help).
        if not re.fullmatch(r"[A-Za-z0-9]+", s):
            print("Invalid input: Use only letters A–Z/a–z and digits 0–9 (no spaces).")
            continue
        return s


def main() -> None:
    """
    Program entry point: detect, encode or decode, and display results.

    - If input has digits: attempt to decode as compressed RLE.
    - Else: encode the alphabetic input.
    """
    raw = _prompt_string()
    try:
        if is_rle_string(raw):
            decoded = rle_decode(raw)
            print(f"Decoded => {decoded}")
        else:
            encoded = rle_encode(raw)
            print(f"Encoded (compressed) => {encoded}")
    except (TypeError, ValueError) as ex:
        # This should cover invalid RLE patterns or non-alphabetic input for encoding.
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
