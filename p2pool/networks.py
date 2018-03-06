from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(

 cryptcoin=math.Object(
        PARENT=networks.nets['cryptcoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=50, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=30, # blocks
        IDENTIFIER='496247d4aa471124'.decode('hex'),
        PREFIX='5685a273ddee4458'.decode('hex'),
        P2P_PORT=8170,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=8171,
        BOOTSTRAP_ADDRS='crypto.office-on-the.net'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-cry',
        VERSION_CHECK=lambda v: True,
    ),



)
for net_name, net in nets.iteritems():
    net.NAME = net_name
