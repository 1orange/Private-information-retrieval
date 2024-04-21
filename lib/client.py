from dataclasses import dataclass
from typing import Optional

import phe
from phe import paillier

from lib.types import QUERY_RESULT, ROW


@dataclass
class Client:
    public_key: Optional[phe.PaillierPublicKey] = None
    __private_key: Optional[phe.PaillierPrivateKey] = None

    def __post_init__(self) -> None:
        if self.public_key and self.__private_key:
            return

        self.public_key, self.__private_key = paillier.generate_paillier_keypair()

    def create_query(self, queried_id: int, dataset_size: int = 10) -> QUERY_RESULT:
        """
        Create a list of encrypted numbers, where queried_id is marked as 1 and others are 0s.
        Such a list is sent in to the server to digest.
        """

        query = list()

        for index in range(1, dataset_size + 1):
            if index == queried_id:
                query.append(self.public_key.encrypt(1))
                continue

            query.append(self.public_key.encrypt(0))

        return query

    def decrypt_query(self, query_result: QUERY_RESULT) -> ROW:
        seq_id, content = query_result
        return self.__private_key.decrypt(seq_id), self.__private_key.decrypt(content)
