from model import Grid


def grid_to_str(g: Grid) -> list[str]:
    grid = [["." for _ in range(g.width)] for _ in range(g.height)]
    for p in g.planets:
        grid[p.pos.y][p.pos.x] = p.get_abbreviation()
    return ["".join(row) for row in grid]



