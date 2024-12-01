from model import Grid, Fleet


def grid_to_str(g: Grid) -> list[str]:
    grid = [["." for _ in range(g.width)] for _ in range(g.height)]
    for p in g.planets:
        grid[p.pos.y][p.pos.x] = p.get_abbreviation()
    return ["".join(row) for row in grid]



def planets_to_str(g: Grid) -> list[str]:
    txt = []
    txt.append("P Ship Prd Ownr")
    txt.append("---------------")
    for p in g.planets:
        txt.append(f"{p.get_abbreviation()} {p.ships:4d} {p.production:3d} {p.owner.name[:4] if p.owner else '-'}")
    return txt


def fleets_to_str(fleets: list[Fleet]) -> list[str]:
    return [f"{f.owner.name[:4]} {f.source.get_abbreviation()} {f.destination.get_abbreviation()} {f.turn_launched}" for f in fleets]

