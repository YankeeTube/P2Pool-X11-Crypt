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

  soomcoin=math.Object(
        P2P_PREFIX='d0b5862d'.decode('hex'),
        P2P_PORT=14800,
        ADDRESS_VERSION=63,
        RPC_PORT=14801,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'Soomcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda bitcoind, target: get_subsidy(bitcoind, target),
        # POW_FUNC = lambda bitcoind: pack.IntType(256).unpack(__import__('xcoin_hash').getPoWHash(bitcoind)),
        BLOCK_PERIOD=90, # s
        SYMBOL='SUM',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'soomcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/cryptcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.soomcoin4'), 'soomcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/block.dws?',
        ADDRESS_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/address.dws?',
        TX_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/tx.dws?',
        SANE_TARGET_RANGE=(2**256//2**20//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),




)
for net_name, net in nets.iteritems():
    net.NAME = net_name
