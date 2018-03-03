from ethscraper.domain.trace.transaction_trace_struct_log import EthTransactionTraceStructLog


class EthTransactionTraceStructLogMapper(object):

    @staticmethod
    def json_dict_to_transaction_trace(json_dict):
        # type: ({}) -> EthTransactionTraceStructLog

        struct_log = EthTransactionTraceStructLog()

        struct_log.pc = json_dict.get('pc', None)
        struct_log.op = json_dict.get('op', None)
        struct_log.gas_cost = json_dict.get('gasCost', None)
        struct_log.gas = json_dict.get('gas', None)
        struct_log.depth = json_dict.get('depth', None)
        struct_log.error = json_dict.get('error', None)
        struct_log.stack = json_dict.get('stack', None)
        struct_log.memory = json_dict.get('memory', None)
        struct_log.storage = json_dict.get('storage', None)

        return struct_log

