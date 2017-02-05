def colorTo12Bit(color):
    """Convert color values from
    RGB string, int, or array of int
    into array of RGB in device format,
    where for each color channel reserve 12 bit

    Example:
        String:
            "AABBCC" => [2729, 3002, 3275]

        Integer:
            0xAABBCC => [2729, 3002, 3275]

        Array of Interger:
            [0xAA, 0xBB, 0xCC] => [2729, 3002, 3275]

    """
    COLOR_MULT = 16.058

    rgb_color = color

    if isinstance(color, str):
        rgb_color = (
                int(char_h + char_l, 16)
                for char_h, char_l in
                zip(color[0::2], color[1::2])
            )

    elif isinstance(color, int):
        rgb_color = (
                (color & 0xFF0000) >> 16,
                (color & 0xFF00) >> 8,
                (color & 0xFF)
            )

    to16Bit = lambda byte: int(byte * COLOR_MULT)
    return map(to16Bit, rgb_color)
