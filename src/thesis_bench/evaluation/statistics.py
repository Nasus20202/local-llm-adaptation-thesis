from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from collections.abc import Callable, Sequence
from typing import Literal


def exact_agreement(pairs: Sequence[tuple[object, object]]) -> float:
    if not pairs:
        raise ValueError("agreement requires pairs")
    return sum(left == right for left, right in pairs) / len(pairs)


def adjacent_agreement(pairs: Sequence[tuple[int, int]]) -> float:
    if not pairs:
        raise ValueError("agreement requires pairs")
    return sum(abs(left - right) <= 1 for left, right in pairs) / len(pairs)


def _distance(
    left: object,
    right: object,
    level: Literal["nominal", "ordinal"],
    frequencies: Counter[object],
) -> float:
    if level == "nominal":
        return 0.0 if left == right else 1.0
    if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
        raise ValueError("ordinal alpha requires numeric levels")
    lower, upper = sorted((left, right))
    cumulative = sum(
        frequency
        for category, frequency in frequencies.items()
        if isinstance(category, (int, float)) and lower <= category <= upper
    )
    difference = cumulative - (frequencies[left] + frequencies[right]) / 2
    return difference**2


def krippendorff_alpha(
    units: Sequence[Sequence[object | None]],
    *,
    level: Literal["nominal", "ordinal"] = "nominal",
) -> float:
    pairs: list[tuple[object, object]] = []
    all_values: list[object] = []
    for unit in units:
        values = [value for value in unit if value is not None]
        all_values.extend(values)
        pairs.extend(
            (values[index], values[other])
            for index in range(len(values))
            for other in range(index + 1, len(values))
        )
    if not pairs:
        raise ValueError("alpha requires at least one rated pair")
    frequencies = Counter(all_values)
    observed = sum(_distance(left, right, level, frequencies) for left, right in pairs) / len(pairs)
    marginal_pairs = sum(
        _distance(left, right, level, frequencies)
        for index, left in enumerate(all_values)
        for right in all_values[index + 1 :]
    )
    expected_denominator = len(all_values) * (len(all_values) - 1) / 2
    expected = marginal_pairs / expected_denominator if expected_denominator else 0.0
    if expected == 0:
        return 1.0 if observed == 0 else 0.0
    return 1.0 - observed / expected


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def family_clustered_interval[T](
    observations: Sequence[tuple[str, T]],
    statistic: Callable[[Sequence[tuple[str, T]]], float],
    *,
    seed: int,
    draws: int = 10_000,
) -> tuple[float, float]:
    if not observations or draws < 1:
        raise ValueError("cluster interval requires observations and draws")
    groups: dict[str, list[tuple[str, T]]] = defaultdict(list)
    for observation in observations:
        groups[observation[0]].append(observation)
    family_ids = tuple(groups)
    generator = random.Random(seed)
    estimates: list[float] = []
    for _ in range(draws):
        selected = generator.choices(family_ids, k=len(family_ids))
        sample = tuple(row for family_id in selected for row in groups[family_id])
        estimates.append(statistic(sample))
    return _percentile(estimates, 0.025), _percentile(estimates, 0.975)
