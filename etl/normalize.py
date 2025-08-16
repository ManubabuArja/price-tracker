import re


def parse_inr(text: str) -> float:
    """
    Normalize Indian price strings like:
    "₹1,499", "Rs. 2,099.00", "1,999" -> 1499.0 / 2099.0 / 1999.0
    Returns 0.0 if not parseable.
    """
    if text is None:
        return 0.0

    t = str(text)
    # Remove currency markers and spaces
    t = (
        t.replace("\u20b9", "")
         .replace("₹", "")
         .replace("Rs.", "")
         .replace("Rs", "")
         .replace("INR", "")
         .strip()
    )

    # Keep digits, comma, dot
    t = re.sub(r"[^0-9,\.]", "", t)

    # Common India format: 1,23,456.78 or 1,234
    # Remove commas and parse as float
    t = t.replace(",", "")

    try:
        return float(t)
    except ValueError:
        return 0.0
