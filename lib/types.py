from typing import Any, Optional

import phe


QUERY = list[Optional[phe.EncryptedNumber]]
QUERY_RESULT = list[tuple[phe.EncryptedNumber | Any]]
ROW = tuple[int | Any]
