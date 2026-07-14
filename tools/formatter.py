def format_money(value):

    if value >= 10000000:
        return f"₹{value/10000000:.2f} Cr"

    elif value >= 100000:
        return f"₹{value/100000:.2f} L"

    elif value >= 1000:
        return f"₹{value/1000:.2f} K"

    else:
        return f"₹{value:.2f}"