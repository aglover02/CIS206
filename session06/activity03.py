"""
A command-line utility that either:
  • Encodes ANY input string using run-length encoding (RLE) with escaping
OR
  • Decodes a previously encoded string.

NEW FORMAT (supports any characters):
  - Escape rules in the ENCODED form:
      • Literal '#' → '##'
      • Literal digit d (0–9) → '#d'
      • Any other character c is written as-is
    Then, if a run length > 1, append the positive integer count after the
    character token (no leading zeros allowed). Examples:
        'A'   → 'A'
        'AAAA'→ 'A4'
        '#'   → '##'
        '###' → '##3'  (escaped '#' token followed by count 3)
        '5'   → '#5'
        '555' → '#53'  (literal '5' escaped, then count 3)
        'B12' → 'B#1#2'  (both digits are escaped as literals)

  - ENCODED STRINGS START WITH THE HEADER '##00'.
    The header indicates the string is already encoded (so the program should decode).
    Therefore:
        If input starts with '##00' → DECODE per the rules above.
        Otherwise → ENCODE the input and add '##00' at the front.

Validation (decoding):
  - After the '##00' header, the body must be a sequence of tokens:
      • Normal token: a single char c ≠ '#' followed by optional COUNT
      • Escaped-literal token: '##' (literal '#') or '#d' (literal digit),
        each optionally followed by COUNT
    COUNT, when present, must be a positive integer with no leading zeros.
  - On failure, a ValueError is raised with a clear message.
"""

from typing import Final
import re


# Patterns are immutable constants (no mutable global state).
# A COUNT is a positive integer without leading zeros.
_COUNT_RE: Final[re.Pattern[str]] = re.compile(r"(?:[1-9]\d*)")

def _encode_token(ch: str) -> str:
    """
    Return the token representation of a single literal character for the encoded stream,
    before adding any run count.

    '#' -> '##'
    digit d -> '#d'
    other -> ch
    """
    if ch == "#":
        return "##"
    if ch.isdigit():
        return "#" + ch
    return ch


def rle_encode(text: str) -> str:
    """
    Encode any input string using RLE with escaping and prepend the '##00' header.

    Escaping ensures that digits in the *data* are never confused with run counts and
    that literal '#" is representable. Run counts are only the (unescaped) digits that
    immediately follow a character token.

    Args:
        text: Any non-empty string.

    Returns:
        Encoded string starting with '##00'.

    Raises:
        TypeError:  if `text` is not a str.
        ValueError: if `text` is empty.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if text == "":
        raise ValueError("text must be non-empty")

    # Aggregate runs
    out_parts: list[str] = ["##00"]  # header
    cur = text[0]
    cnt = 1

    for ch in text[1:]:
        if ch == cur:
            cnt += 1
        else:
            # emit previous run
            tok = _encode_token(cur)
            out_parts.append(tok)
            if cnt > 1:
                out_parts.append(str(cnt))
            cur, cnt = ch, 1

    # final run
    tok = _encode_token(cur)
    out_parts.append(tok)
    if cnt > 1:
        out_parts.append(str(cnt))

    return "".join(out_parts)


def rle_decode(encoded: str) -> str:
    """
    Decode a string produced by `rle_encode`.

    Requirements:
        - The input must start with the exact header '##00'.
        - After the header, the body is a sequence of tokens:
            * NORMAL: a single char c != '#', optionally followed by COUNT
            * ESCAPED: '##' (literal '#') or '#d' (literal digit), optionally
              followed by COUNT
          COUNT, if present, must be a positive integer with no leading zeros.

    Examples:
        '##00A4'        -> 'AAAA'
        '##00##3'       -> '###'
        '##00#53'       -> '555'
        '##00B#1#2'     -> 'B12'
        '##00Z#10##2A'  -> 'Z0##A'

    Args:
        encoded: The encoded string beginning with '##00'.

    Returns:
        The decoded (original) string.

    Raises:
        TypeError:  if `encoded` is not a str.
        ValueError: if the header is missing/incorrect or the body is invalid.
    """
    if not isinstance(encoded, str):
        raise TypeError("encoded must be a str")
    if not encoded.startswith("##00"):
        raise ValueError("Encoded input must begin with the '##00' header")

    s = encoded[4:]  # strip header
    i = 0
    n = len(s)
    out: list[str] = []

    def _read_count(start: int) -> tuple[int, int]:
        """Read an optional COUNT at s[start:], returning (count, next_index)."""
        m = _COUNT_RE.match(s, start)
        if not m:
            return 1, start  # no explicit count => 1
        # leading zero already prevented by regex
        return int(m.group(0)), m.end()

    while i < n:
        ch = s[i]

        if ch == "#":
            if i + 1 >= n:
                raise ValueError("Dangling escape '#' at end of encoded string")
            nxt = s[i + 1]
            if nxt == "#":
                literal = "#"
                i += 2
            elif nxt.isdigit():
                literal = nxt  # literal digit
                i += 2
            else:
                raise ValueError("Invalid escape sequence: '#' must be followed by '#' or a digit")

            count, i = _read_count(i)
            out.append(literal * count)
            continue

        # NORMAL token (single char not '#'), then optional count
        literal = ch
        i += 1
        count, i = _read_count(i)
        out.append(literal * count)

    return "".join(out)


def _prompt() -> str:
    """
    Prompt for input. If the string starts with '##00', it will be DECODED.
    Otherwise, it will be ENCODED with the header and escaping.
    """
    while True:
        s = input("Enter text (starts with '##00' to decode; otherwise encode): ").rstrip("\n")
        if not s:
            print("Invalid input: input cannot be empty.")
            continue
        return s


def main() -> None:
    """
    Program entry point:
        - If input starts with '##00' → decode and display.
        - Else → encode and display.
    """
    user_text = _prompt()
    try:
        if user_text.startswith("##00"):
            decoded = rle_decode(user_text)
            print(f"Decoded => {decoded}")
        else:
            encoded = rle_encode(user_text)
            print(f"Encoded => {encoded}")
    except (TypeError, ValueError) as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
