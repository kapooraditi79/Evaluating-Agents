"""OTel explicit-bound bins: (previous, upper], underflow [0, first], overflow (last, inf)."""

from bisect import bisect_left
from math import ceil, isfinite


def validate_bounds(bounds: list[float]) -> None:
    if (
        not bounds
        or any(not isfinite(x) or x <= 0 for x in bounds)
        or any(b <= a for a, b in zip(bounds, bounds[1:], strict=False))
    ):
        raise ValueError("bounds must be finite, positive and strictly increasing")


def histogram(values: list[float], bounds: list[float]) -> list[int]:
    validate_bounds(bounds)
    counts = [0] * (len(bounds) + 1)
    for value in values:
        if not isfinite(value) or value < 0:
            raise ValueError("durations must be finite and nonnegative")
        counts[bisect_left(bounds, value)] += 1
    return counts


def percentile(
    counts: list[int], bounds: list[float], q: float
) -> tuple[float | None, float | None]:
    """Estimate nearest-rank percentile by bin midpoint; return its absolute error bound."""
    validate_bounds(bounds)
    if not isfinite(q) or not 0 < q <= 1:
        raise ValueError("quantile must lie in (0,1]")
    if len(counts) != len(bounds) + 1 or any(
        type(count) is not int or count < 0 for count in counts
    ):
        raise ValueError("histogram counts must be nonnegative integers with len(bounds)+1 entries")
    if not sum(counts):
        return None, None
    rank = ceil(q * sum(counts))
    cumulative = 0
    for i, count in enumerate(counts):
        cumulative += count
        if cumulative >= rank:
            if i == len(bounds):
                return None, None  # overflow has no finite bound
            lower = bounds[i - 1] if i else 0
            upper = bounds[i]
            return (lower + upper) / 2, (upper - lower) / 2
    raise ValueError("invalid histogram")
