PRICES = {
    "12345": 7.25,
    "23456": 12.50,
}


def scan(barcode):
    if barcode == "":
        return "Error: empty barcode"

    if barcode not in PRICES:
        return "Error: barcode not found"

    return _format_price(PRICES[barcode])


def total(barcodes):
    total_amount = 0
    for barcode in barcodes:
        scanned = scan(barcode)
        if scanned.startswith("Error:"):
            return scanned

        total_amount += PRICES[barcode]

    return _format_price(total_amount)


def _format_price(amount):
    return f"${amount:.2f}"
