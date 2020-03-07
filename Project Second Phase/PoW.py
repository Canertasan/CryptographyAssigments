import hashlib
import random

def CheckPow(p, q, g, PoWLen, TxCnt, filename):
    nonce = ""
    with open(filename,'r') as file : 
        blockLines  = file.readlines()
        nonce = blockLines[-1][7:-1]
        lenblocklines = len(blockLines)
        numLines1block = lenblocklines // TxCnt


    # Calculate root-hash
    hashTree = []
    j = 0
    for i in range(0,TxCnt):
        transaction = "".join(blockLines[j:j + numLines1block])
        j += numLines1block
        #print("hash type", type(hashlib.sha3_256(transaction.encode("UTF-8")).digest()))
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
    text = rootHash + (str(nonce)+'\n').encode('UTF-8') 
    return  hashlib.sha3_256(text).hexdigest()


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
    