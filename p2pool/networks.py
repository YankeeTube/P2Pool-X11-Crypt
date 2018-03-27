from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(

 soomcoin=math.Object(
        PARENT=networks.nets['soomcoin'],
        SHARE_PERIOD=18, # (BLOCK PERIOD / 5)
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=5, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=20, # blocks | 600/[blockTime] = x *3 = Spread
        IDENTIFIER='1bfe41c80cb80be9'.decode('hex'), # 2017-12-20 10:57:12 13801
        PREFIX='1bfe41c80cb80fd1'.decode('hex'), # 2017-12-20 10:57:12 14801
        P2P_PORT=3334,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=3333,
        BOOTSTRAP_ADDRS='192.168.200.100'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: True,
    ),



)
for net_name, net in nets.iteritems():
    net.NAME = net_name
