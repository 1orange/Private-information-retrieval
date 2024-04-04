import random
import sys


def make_dataset(
    size: int = 10,
    range_min: int = -sys.maxsize,
    range_max: int = sys.maxsize,
    random_instance: random.Random = random.Random(),
) -> list[tuple[int, int]]:
    return [
        (seq_id + 1, random_instance.randint(range_min, range_max))
        for seq_id in range(size)
    ]
