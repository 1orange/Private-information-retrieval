import random
import sys
from dataclasses import dataclass
from typing import Optional

import phe


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


@dataclass
class Node:
    value: phe.EncryptedNumber
    next: Optional[phe.EncryptedNumber] = None


@dataclass
class LinkedList:
    __head: Optional[Node] = None
    __tail: Optional[Node] = None

    def add(self, value):
        node = Node(value)

        if self.__head is None:
            self.__head = node

        prev = self.__tail

        if prev:
            prev.next = node

        self.__tail = node

    def __iter__(self):
        node = self.__head
        while node:
            yield node.value
            node = node.next
