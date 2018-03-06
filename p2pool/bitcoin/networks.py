import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

@defer.inlineCallbacks
def get_subsidy(bitcoind, target):
    res = yield bitcoind.rpc_getblock(target)

    defer.returnValue(res)

nets = dict(

  cryptcoin=math.Object(
        P2P_PREFIX='f1aff2a3'.decode('hex'),
        P2P_PORT=27114,
        ADDRESS_VERSION=34,
        RPC_PORT=27115,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'cryptcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda bitcoind, target: get_subsidy(bitcoind, target),
        BLOCK_PERIOD=90, # s
        SYMBOL='CRYPT',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'cryptcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/cryptcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.cryptcoin'), 'cryptcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/block.dws?',
        ADDRESS_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/address.dws?',
        TX_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/tx.dws?',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),




)
for net_name, net in nets.iteritems():
    net.NAME = net_name
