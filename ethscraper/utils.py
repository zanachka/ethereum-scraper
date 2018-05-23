from builtins import str


def hex_to_dec(str):
    if str is None:
        return None
    try:
        return int(str, 16)
    except ValueError:
        print("Not a hex string %s" % str)
        return str


def str_to_bool(obj):
    if isinstance(obj, str):
        return obj.lower() in ("yes", "true", "t", "1")
    else:
        return obj


def without_key(dictionary, key):
    return {k: dictionary[k] for k in dictionary if k != key}


def chunk_string(string, length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def split_to_batches(start, end, batch_size):
    for batch_start in range(start, end + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end)
        yield batch_start, batch_end


def generate_get_block_by_number_json_rpc(start_block, end_block, include_transactions):
    for block_number in range(start_block, end_block + 1):
        yield {
            'jsonrpc': '2.0',
            'method': 'eth_getBlockByNumber',
            'params': [hex(block_number), include_transactions],
            'id': 1,
        }