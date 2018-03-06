================
P2Pool-Crypt-X11
================  
    ilsawa/p2ppol-crypt 인용




작성한 내용을 기반으로 에러 및 한글버전으로 수정한 내용입니다.
--------------------------------------------------------------

    마지막 작성일자 : 2018.03.06    
        
           
           
           
           
    
기부하기
-------
.. code-block:: bash

    SUM : SThUc3o8hpnSyedGJi4eGjohvKu1TtA48a



파이썬 및 다른 프로그램 설치
----------------------------
.. code-block:: bash

    sudo apt install python python-pip git curl vim wget -y
    sudo apt-get install python-zope.interface python-twisted python-twisted-web -y
    sudo pip install --upgrade pip


X11 관련 모듈 설치
---------------------------------------
.. code-block:: bash

    
    git clone https://github.com/YankeeTube/P2Pool-X11-Crypt.git
    cd P2Pool-X11-Crypt/xcoin-hash-master
    sudo python setup.py install
    
    

Coin 설정 - p2pool/networks.py
------------------------------
.. code-block:: python

    cryptcoin=math.Object( # Coin 이름
        PARENT=networks.nets['cryptcoin'], # Coin 이름
        SHARE_PERIOD=15, # 공유도달시간 / 숫자가 낮을수록 체인 증가
        CHAIN_LENGTH=24*60*60//15, # Pool에서 제거 되기전까지의 유지하는 공유 길이
        REAL_CHAIN_LENGTH=24*60*60//15, # 지불금에 포함되는 이전 발견 공유수까지 포함하는 길이
        TARGET_LOOKBEHIND=50, # P2Pool의 Hash 속도를 기준으로 공유 난이도를 설정
        SPREAD=30, # 마이너가 블록 발견시 풀에게 지불할 블록 수 설정
        IDENTIFIER='496247d4aa471124'.decode('hex'), # 19자리 임의의 숫자를 16진수로 변환
        PREFIX='5685a273ddee4458'.decode('hex'), # 19자리 임의의 숫자를 16진수로 변환
        P2P_PORT=8170, # Bitcoin/networks.py의 P2P_PORT와 다른 포트 지정
        MIN_TARGET=0, # 최소연결
        MAX_TARGET=2**256//2**20 - 1, # 최대연결
        PERSIST=False, # 다른 사람이 공유체인을 BootStrap 하는 것을 방지 합니다. | False설정
        WORKER_PORT=8171, # Miner가 Pool에 연결 할 Port지정 및 Monitoring Port
        BOOTSTRAP_ADDRS='192.168.0.3'.split(' '), # Pool주소
        ANNOUNCE_CHANNEL='#p2pool-cry', # P2Pool에 발표되는 이름
        VERSION_CHECK=lambda v: True, # Version 검증안함
    ),


Coin 설정 - p2pool/bitcoin/networks.py
--------------------------------------
.. code-block:: python

    cryptcoin=math.Object( # Coin 이름
        P2P_PREFIX='f1aff2a3'.decode('hex'), # main.cpp에서 -> pchMessageStart[4] | {0x??, 0x??, 0x??, 0x??} 0x를제외한값
                                             # Altcoin  chainparams.cpp에 있거나 없으면 pchMessageStart[0],[1],[2],[3] 값
        P2P_PORT=27114, # protocol.h -> GetDefaultPort(args*) 보면 { return testnet ? 19333 : 9333 } 9333 P2P Port
                        # Altcoin | chainparams.cpp | nDefaultPort 값
        ADDRESS_VERSION=34, # base58.h -> PUBKEY_ADDRESS 값
                            # Altcoin | chainparams.cpp | base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,??); | ??값
        RPC_PORT=27115, # bitcoinrpc.cpp에서 -> Getarg("-rpcport", ????) | ????값
                        # Altcoin | chainparams.cpp | nRPCPort 값
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'cryptcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )), # cryptocoinadress를 rpcdump.cpp -> dumpprivkey 값
        SUBSIDY_FUNC=lambda bitcoind, target: get_subsidy(bitcoind, target),
        # lambda height, 일때a 높이: 보상금 * satoshies >> (height +1)//840000, | height: 
        BLOCK_PERIOD=90, # main.cpp -> nTargetSpacing = ??; | 값
        SYMBOL='CRYPT', # Crypto Currency COIN명 | ex) BTC, LTC, ETH, DRK...
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'cryptcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/cryptcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.cryptcoin'), 'cryptcoin.conf'),
        # crypcoin을 설정할 코인 이름 및 .conf 파일위치에 따른 폴더와 파일명으로변경
        BLOCK_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/block.dws?', # Block 탐색기 URL
        ADDRESS_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/address.dws?', #  주소 탐색기 URL
        TX_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/crypt/tx.dws?', # Transaction 탐색기 URL
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1), 
        # X11    : (2**256//2**32//1000 - 1, 2**256//2**20 - 1) 
        # SHA256 : (2**256//2**32//1000000 - 1, 2**256//2**32 - 1)
        # Scrypt : (2**256//1000000000 - 1, 2**256//1000 - 1)
        DUMB_SCRYPT_DIFF=1, # X11 기본값
        DUST_THRESHOLD=0.001e8,# X11 기본값


실행 및 옵션
-----------------------------
.. code-block:: bash

    python run_p2pool.py --net [코인명] --give-author [풀 수수료] -a [지갑 주소]
    ex) python run_p2pool.py --net litecoin --give-author 0.0025 -a SThUc3o8hpnSyedGJi4eGjohvKu1TtA48a



