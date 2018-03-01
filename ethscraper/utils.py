def hex_to_dec(str):
    if str is None:
        return None
    try:
        return int(str, 16)
    except ValueError:
        print "Not a hex string %s" % str
        return str


def without_key(dictionary, key):
    return {k: dictionary[k] for k in dictionary if k != key}
