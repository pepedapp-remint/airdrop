SELECT block_number, transaction_index, `hash`, from_address, input FROM `bigquery-public-data.crypto_ethereum.transactions`
WHERE to_address = "0xe4bd56cbf537074e3836a1721983107cce9e689f" AND block_number < 10980000 AND receipt_status = 1
ORDER BY block_number, transaction_index
