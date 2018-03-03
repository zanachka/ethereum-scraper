class EthTransactionTraceStructLog(object):
    pc = None  # type: int
    op = None  # type: str
    gas_cost = None  # type: int
    gas = None  # type: int
    depth = None  # type: int
    error = None  # type: str
    stack = []  # type: [str]
    memory = []  # type: [str]
    storage = {}  # type: dict
