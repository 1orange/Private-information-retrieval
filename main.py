import asyncio
import concurrent.futures
import random
from logging import Logger

import logging
from lib.client import Client
from lib.data import make_dataset
from lib.measure import measure_function
from lib.server import Server


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

async def _simulate(
    logger: Logger,
    random_: random.Random,
    DATASET_SIZE: int = 10,
):
    # Dataset creation
    dataset_exec_time, dataset_size, dataset = measure_function(
        make_dataset,
        size=DATASET_SIZE,
        range_min=1,
        range_max=500,
        random_instance=random_,
    )
    logger.debug(
        f"Dataset created in: {dataset_exec_time:.10f} sec. [{dataset_size} bytes]"
    )

    server = Server(dataset)
    client = Client()

    encrypt_query_time, encrypt_query_size, query = measure_function(
        client.create_query,
        dataset_size=DATASET_SIZE,
        queried_id=random_.randint(1, DATASET_SIZE),
    )

    logger.debug(
        f"Client_query created in: {encrypt_query_time:.10f} sec. [{encrypt_query_size} bytes]"
    )

    server_query_time, server_query_size, result = measure_function(
        server.fetch_data,
        query=query,
    )

    logger.debug(
        f"Server returned result in: {server_query_time:.10f} sec. [{server_query_size} bytes]"
    )

    decrypt_time, decrypt_size, decrypted_data = measure_function(
        client.decrypt_query,
        query_result=result,
    )

    logger.debug(
        f"Client decrypted result in: {decrypt_time:.10f} sec. [{decrypt_size} bytes]"
    )

    return (
        (encrypt_query_time, encrypt_query_size),
        (server_query_time, server_query_size),
        (decrypt_time, decrypt_size),
    )


async def _run_test(logger: Logger, DATASET_SIZE: int = 10, RANDOM_SEED: int = 1, number_of_tries: int = 1):
    random_ = random.Random(RANDOM_SEED)

    total_encrypt_query_time = 0
    total_encrypt_query_size = 0
    total_server_query_time = 0
    total_server_query_size = 0
    total_decrypt_time = 0
    total_decrypt_size = 0

    tasks = []
    for _ in range(number_of_tries):
        tasks.append(_simulate(logger, random_, DATASET_SIZE))

    results = await asyncio.gather(*tasks)

    for ((encrypt_query_time, encrypt_query_size),
         (server_query_time, server_query_size),
         (decrypt_time, decrypt_size)) in results:
        total_encrypt_query_time += encrypt_query_time
        total_encrypt_query_size += encrypt_query_size
        total_server_query_time += server_query_time
        total_server_query_size += server_query_size
        total_decrypt_time += decrypt_time
        total_decrypt_size += decrypt_size

    logger.info(
        f"Average encrypt query time: {total_encrypt_query_time / number_of_tries:.10f} sec"
    )
    logger.info(
        f"Average server query time: {total_server_query_time / number_of_tries:.10f} sec"
    )
    logger.info(
        f"Average decrypt time: {total_decrypt_time / number_of_tries:.10f} sec"
    )

async def main():
    logger = logging.getLogger(__name__)

    logger.info("dataset of 1_000; 10 tries")
    await _run_test(logger=logger, DATASET_SIZE = 1_000, RANDOM_SEED = 10, number_of_tries = 10)

    logger.info("dataset of 10_000; 10 tries")
    await _run_test(logger=logger, DATASET_SIZE = 10_000, RANDOM_SEED = 15, number_of_tries = 10)

    logger.info("dataset of 100_000; 10 tries")
    await _run_test(logger=logger, DATASET_SIZE = 100_000, RANDOM_SEED = 20, number_of_tries = 10)



if __name__ == "__main__":
    asyncio.run(main())