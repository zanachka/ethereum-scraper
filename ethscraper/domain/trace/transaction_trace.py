from ethscraper.domain.trace.transaction_trace_struct_log import EthTransactionTraceStructLog


class EthTransactionTrace(object):
    gas = None  # type: int
    failed = None  # type: bool
    return_value = None  # type: str
    struct_logs = []  # type: [EthTransactionTraceStructLog]
