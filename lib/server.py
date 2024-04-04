from dataclasses import dataclass, field
from typing import Optional

from lib.types import QUERY, QUERY_RESULT


@dataclass
class Server:
    data: list[Optional[tuple[int, int]]] = field(default_factory=list)

    def fetch_data(self, query: QUERY) -> QUERY_RESULT:
        return [
            (seq_id * enc_id, content * enc_id)
            for (seq_id, content), enc_id in zip(self.data, query)
        ]
