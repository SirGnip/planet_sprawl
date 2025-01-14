import model


def grid_to_str(g: model.Grid) -> list[str]:
    grid = [["." for _ in range(g.width)] for _ in range(g.height)]
    for p in g.planets:
        grid[p.pos.y][p.pos.x] = p.get_abbreviation()
    return ["".join(row) for row in grid]


def planets_to_str(g: model.Grid) -> list[str]:
    txt = []
    txt.append("P Ship Prd Ownr")
    txt.append("---------------")
    for p in g.planets:
        txt.append(f"{p.get_abbreviation()} {p.ships:4d} {p.production:3d} {p.owner.name[:4] if p.owner else '-'}")
    return txt


def fleets_to_str(fleets: list[model.Fleet]) -> list[str]:
    return [f"{f.owner.name[:4]} {f.source.get_abbreviation()} {f.destination.get_abbreviation()} turn:{f.turn_launched}-{f._arrival_turn} ships:{f.ships}" for f in fleets]


def events_to_str(events: model.EventLog, current_turn: model.TURN) -> list[str]:
    events = reversed(events.events)
    lines = [f"#{turn}: {msg}" for turn, msg in events if turn == current_turn]
    lines = lines[:10]
    return lines


def game_to_str(game: model.GameModel) -> list[str]:
    txt = grid_to_str(game.grid)
    txt.append("=" * 40)
    txt.extend(planets_to_str(game.grid))
    txt.append("=" * 40)
    txt.extend(fleets_to_str(game.fleets))
    txt.extend(events_to_str(game.events, game.turn))
    txt.append("=" * 40)
    return txt