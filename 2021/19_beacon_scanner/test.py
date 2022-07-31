def orientations(v: tuple[int, int, int] = (0, 1, 2)) -> list[tuple[int, int, int]]:
    def roll(v):
        return (v[0], v[2], -v[1])

    def turn(v):
        return (-v[1], v[0], v[2])

    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield (v)  #    Yield R
            for i in range(3):  #    Yield TTT
                v = turn(v)
                yield (v)
        v = roll(turn(roll(v)))  # Do RTR


print(list(orientations()), type(orientations()))
