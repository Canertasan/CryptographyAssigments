import hashlib
import random

def PoW(PoWLen,TxCnt,block_candidate, pow_pre):
    blockLines  = block_candidate
    lenblocklines = len(blockLines)
    numLines1block = lenblocklines // TxCnt

    # Calculate root-hash
    hashTree = []
    j = 0
    for i in range(0,TxCnt):
        transaction = "".join(blockLines[j:j + numLines1block])
        j += numLines1block
        hashTree.append(hashlib.sha3_256(transaction.encode("UTF-8")).digest())

    temp = TxCnt
    k = 0
    while (temp!=1):
        for i in range(k,k+temp,2):
            sumOfHash = hashTree[i]+hashTree[i+1]
            hashTree.append(hashlib.sha3_256(sumOfHash).digest())
        k += temp
        temp /= 2
        temp = int(temp)
    rootHash = hashTree[2*TxCnt-2]
    #print(type(rootHash))
    #print(type(pow_pre))
    powCurr = "."
    while (powCurr[0:PoWLen] != "0" * PoWLen):
        nonce = random.getrandbits(128)
        #print(type(nonce.to_bytes((nonce.bit_length()+7)//8, byteorder = 'big')))
        new_Pow = rootHash + pow_pre + nonce.to_bytes((nonce.bit_length()+7)//8, byteorder = 'big')
        powCurr = hashlib.sha3_256(new_Pow).hexdigest()
    
    blockLines.append("Previous PoW: " + pow_pre.decode("UTF-8") + '\n')
    blockLines.append("Nonce: " + str(nonce) + '\n')
    blockStr = "".join(blockLines)
    return blockStr, pow_pre.decode("UTF-8") 

def RootHash(TxCnt,block_candidate):
    blockLines  = block_candidate
    lenblocklines = len(blockLines)
    numLines1block = lenblocklines // TxCnt

    # Calculate root-hash
    hashTree = []
    j = 0
    for i in range(0,TxCnt):
        transaction = "".join(blockLines[j:j + numLines1block])
        j += numLines1block
        hashTree.append(hashlib.sha3_256(transaction.encode("UTF-8")).digest())

    temp = TxCnt
    k = 0
    while (temp!=1):
        for i in range(k,k+temp,2):
            sumOfHash = hashTree[i]+hashTree[i+1]
            hashTree.append(hashlib.sha3_256(sumOfHash).digest())
        k += temp
        temp /= 2
        temp = int(temp)
    rootHash = hashTree[2*TxCnt-2]
    return rootHash

def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):
    if PrevBlock != "":
        pre_rootHash = RootHash(TxCnt,PrevBlock)
        nonce_pre = PrevBlock[-1][7:].strip('\n')
        # print("Pre nonce :::",nonce_pre)
        nonce_pre = int(nonce_pre)
        pre_pre_pow =  bytes(PrevBlock[-2][14:].strip('\n'), encoding = 'UTF-8')
        # print("PREV BLOCK:::::::.::",PrevBlock[-2][14:].strip('\n'))
        # print(pre_pre_pow)
        pow_pre = pre_rootHash + pre_pre_pow + nonce_pre.to_bytes((nonce_pre.bit_length()+7)//8, byteorder = 'big')
        # print(type(pow_pre))
        #h_pow_pre = hashlib.sha3_256(pow_pre.decode('UTF-8')).hexdigest()
        h_pow_pre = hashlib.sha3_256(pow_pre).hexdigest()
        h_pow_pre = h_pow_pre.encode('UTF-8')
        # print("H_pow_pre:::.   ",h_pow_pre)
        # pow_pre = hashlib.sha3_256(pow_pre).hexdigest()  hashlib.sha3_256(text).hexdigest()
    else:
        # pow_pre =  bytes("00000000000000000000", encoding = 'UTF-8')
        h_pow_pre = "00000000000000000000".encode('UTF-8')
        #print("ELSEIN ICINDEKI HPOW_PERE",h_pow_pre)
    NewBlock, pre_poow  = PoW(PoWLen,TxCnt,block_candidate, h_pow_pre)
    return NewBlock, pre_poow



"""
def PoW(PoWLen, q, p, g, TxCnt, filename):
    with open(filename,'r') as file : 
        blockLines  = file.readlines()
        lenblocklines = len(blockLines)
        numLines1block = lenblocklines // TxCnt

    # Calculate root-hash
    hashTree = []
    j = 0
    for i in range(0,TxCnt):
        transaction = "".join(blockLines[j:j + numLines1block])
        j += numLines1block
        hashTree.append(hashlib.sha3_256(transaction.encode("UTF-8")).digest())

    temp = TxCnt
    k = 0
    while (temp!=1):
        for i in range(k,k+temp,2):
            sumOfHash = hashTree[i]+hashTree[i+1]
            hashTree.append(hashlib.sha3_256(sumOfHash).digest())
        k += temp
        temp /= 2
        temp = int(temp)
    rootHash = hashTree[2*TxCnt-2]

    powCurr = "."
    nonce = ""
    while (powCurr[0:PoWLen] != "0" * PoWLen):
        nonce = str(random.getrandbits(128))+'\n'
        text = rootHash + nonce.encode('UTF-8') 
        powCurr = hashlib.sha3_256(text).hexdigest()

    blockLines.append("Nonce: " + nonce)
    blockStr = "".join(blockLines)
    return blockStr
"""