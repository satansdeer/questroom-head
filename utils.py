def colorTo12Bit(color):
    COLOR_MULT = 16.058
    to16Bit = lambda byte: int(byte * COLOR_MULT)
    return map(to16Bit, color)
