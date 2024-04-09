from typing import Any, Optional

import phe


QUERY = list[Optional[phe.EncryptedNumber]]
QUERY_RESULT = tuple[phe.EncryptedNumber | Any]
ROW = tuple[int | Any]
