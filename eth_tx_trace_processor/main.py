from ethjsonrpc import EthJsonRpc
c = EthJsonRpc('infuranet.infura.io/eQq8vdX3vS511ulZw8fr', 443, tls=True)
bn = c.eth_getBlockByNumber(block=0)
print bn