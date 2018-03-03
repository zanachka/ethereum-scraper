from ethscraper.domain.trace.transaction_trace import EthTransactionTrace
from ethscraper.mapper.trace.transaction_trace_struct_log_mapper import EthTransactionTraceStructLogMapper


class EthTransactionTraceMapper(object):
    transaction_trace_struct_log_mapper = EthTransactionTraceStructLogMapper()

    def json_dict_to_transaction_trace(self, json_dict):
        # type: ({}) -> EthTransactionTrace

        trace = EthTransactionTrace()

        trace.gas = json_dict.get('gas', None)
        trace.failed = json_dict.get('failed', None)
        trace.return_value = json_dict.get('returnValue', None)

        if 'structLogs' in json_dict:
            trace.struct_logs = map(
                lambda struct_log: self.transaction_trace_struct_log_mapper.json_dict_to_transaction_trace(struct_log),
                json_dict['structLogs'])
        return trace

