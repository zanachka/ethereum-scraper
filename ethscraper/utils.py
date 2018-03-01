def hex_to_dec(str):
    if str is None:
        return None
    try:
        return int(str, 16)
    except ValueError:
        print "Not a hex string %s" % str
        return str
