import decimal

def twodp(num):
    return decimal.Decimal(str(num)).quantize(decimal.Decimal('0.00'))