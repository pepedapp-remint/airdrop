-- Select all `CardsTransferred` event logs
SELECT * FROM `bigquery-public-data.crypto_ethereum.logs`
WHERE ARRAY_LENGTH(topics) > 0 AND topics[OFFSET(0)] = '0xca854e9a512debe5ebf4a5228b275f9d8c3c005f95ba3660d7a6a66fdc72b112' AND block_number < 10980000
ORDER by block_number, transaction_index, log_index
