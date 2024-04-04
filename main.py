import random
import timeit

from phe import paillier

from lib.client import Client
from lib.data import make_dataset
from lib.server import Server


def sample():
    """Sample code snippet to prove that homomorphic addition and homomorphic scalar multiplication."""

    public_key, private_key = paillier.generate_paillier_keypair()

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Decrypted sum: {sum(nums)}")

    num_a = 30
    num_b = 390
    print(f"Decrypted multiplication: {num_a * num_b}")

    encrypted_nums = [public_key.encrypt(num) for num in nums]

    encrypted_num_a = public_key.encrypt(num_a)
    encrypted_num_b = public_key.encrypt(num_b)
    encrypted_multiplication_a = encrypted_num_a * num_b
    encrypted_multiplication_b = num_a * encrypted_num_b

    print(f"Encrypted sum: {private_key.decrypt(sum(encrypted_nums))}")
    print(
        f"Encrypted multiplication: {private_key.decrypt(encrypted_multiplication_a)}"
    )
    print(
        f"Encrypted multiplication: {private_key.decrypt(encrypted_multiplication_b)}"
    )


def main():

    DATASET_SIZE = 10
    random_instance = random.Random(x=10)

    # Create server
    server = Server(
        data=make_dataset(
            size=DATASET_SIZE,
            range_min=1,
            range_max=50,
            random_instance=random_instance,
        )
    )

    # Create client
    client = Client()

    # Create query and send it to the server
    query = client.create_query(dataset_size=DATASET_SIZE, queried_id=4)

    result = server.fetch_data(query)

    print(server.data)
    print(client.decrypt_query(result))


if __name__ == "__main__":

    start = timeit.default_timer()
    print("The start time is :", start)
    main()
    print("The difference of time is :", timeit.default_timer() - start)
