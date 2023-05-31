import typing as t

from pymunk.vec2d import Vec2d


def round_vec2d(pos: Vec2d) -> t.List[float]:
    return list(map(lambda x: round(x, 2), pos))
