from dataclasses import dataclass, field
from threading import Thread
from typing import Optional

import phe

from lib.types import QUERY, QUERY_RESULT


@dataclass
class Server:
    data: list[Optional[tuple[int, int]]] = field(default_factory=list)

    def fetch_data(self, query: QUERY) -> QUERY_RESULT:
        fetched_id = 0
        fetched_content = 0

        for (seq_id, content), enc_id in zip(self.data, query):
            fetched_id += seq_id * enc_id
            fetched_content += content * enc_id

        return fetched_id, fetched_content
