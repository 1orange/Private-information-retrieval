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

    def create_query(
        self, queried_id: int, dataset_size: int = 10
    ) -> list[Optional[phe.EncryptedNumber]]:
        """
        Create a list of encrypted numbers, where queried_id is marked as 1 and others are 0s.
        Such a list is sent in to the server to digest.
        """

        return [
            self.public_key.encrypt(num)
            for num in [
                1 if index == queried_id else 0 for index in range(1, dataset_size + 1)
            ]
        ]

    def decrypt_query(self, query_result: QUERY_RESULT) -> ROW:
        for seq_id, content in query_result:
            if (decrypted_id := self.__private_key.decrypt(seq_id)) == 0:
                continue

            return decrypted_id, self.__private_key.decrypt(content)
