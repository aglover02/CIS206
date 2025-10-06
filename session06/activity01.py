"""
A simple command-line program that asks the user for a string of alphabetic
characters and outputs its run-length encoded (RLE) form using a "compressed"
format (i.e., singletons have no count: 'AAABCC' -> 'A3BC2').
"""

from typing import Final
import re


_ALPHA_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z]+$")


def rle_encode(text: str) -> str:
    """
    Encode a string using run-length encoding (compressed form).

    The compressed form omits the count for runs of length 1. For example:
        "AAABCC" -> "A3BC2"
        "aabbA"  -> "a2b2A"

    Parameter validation:
        - `text` must be a non-empty `str`.
        - Only alphabetic characters [A-Za-z] are allowed.
        - Case is preserved: 'A' and 'a' are distinct.

    Args:
        text: The input string to encode.

    Returns:
        The RLE-encoded string in compressed form.

    Raises:
        TypeError: If `text` is not a `str`.
        ValueError: If `text` is empty or contains non-alphabetic characters.

    Examples:
        >>> rle_encode("AAABCC")
        'A3BC2'
        >>> rle_encode("abc")
        'abc'
        >>> rle_encode("AaaBBB")
        'A2aB3'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not text:
        raise ValueError("text must be non-empty")
    if _ALPHA_RE.fullmatch(text) is None:
        raise ValueError("text must contain alphabetic characters only (A–Z or a–z)")

    # Run aggregation
    out_parts: list[str] = []
    current = text[0]
    count = 1

    for ch in text[1:]:
        if ch == current:
            count += 1
        else:
            # Emit previous run: character + count (omit count if 1)
            out_parts.append(current)
            if count > 1:
                out_parts.append(str(count))
            current = ch
            count = 1

    # Emit final run
    out_parts.append(current)
    if count > 1:
        out_parts.append(str(count))

    return "".join(out_parts)


def _prompt_for_alpha_string() -> str:
    """
    Prompt the user for an alphabetic string; re-prompt until valid.

    Returns:
        A validated, non-empty alphabetic string.
    """
    while True:
        user_input = input("Enter an alphabetic string to RLE-encode: ").strip()
        try:
            # Validate via the same logic used by rle_encode to keep behavior consistent.
            if not user_input:
                raise ValueError("Input cannot be empty.")
            if _ALPHA_RE.fullmatch(user_input) is None:
                raise ValueError("Use alphabetic characters only (A–Z or a–z).")
            return user_input
        except ValueError as ex:
            print(f"Invalid input: {ex}")


def main() -> None:
    """
    Program entry point: prompt, encode, and display the result.
    """
    s = _prompt_for_alpha_string()
    try:
        encoded = rle_encode(s)
    except (TypeError, ValueError) as ex:
        # Defensive: this shouldn't occur because we validated in the prompt function,
        # but we handle it to demonstrate robust parameter validation.
        print(f"Error: {ex}")
        return
    print(f"RLE (compressed) => {encoded}")


if __name__ == "__main__":
    main()
