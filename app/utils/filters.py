def format_currency(value):
    try:
        return "${:,.2f}".format(float(value))
    except (TypeError, ValueError):
        return "$0.00"
