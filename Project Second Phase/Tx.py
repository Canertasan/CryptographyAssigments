import random
import DS

# This homework did by caghankoksal - 20588 and canertasan - 21224

def gen_random_tx(q, p, g):
    transaction = "**** Bitcoin transaction ****\n"
    serial_number = random.getrandbits(128)
    transaction +="Serial number: " + str(serial_number)+ "\n"

    payerAlpha, payerBeta = DS.KeyGen(q,p,g)
    payeeAlpha, payeeBeta = DS.KeyGen(q,p,g)

    transaction += "Payer Public Key (beta): " + str(payerBeta) + "\n"
    transaction += "Payee Public Key (beta): " + str(payeeBeta) + "\n"

    amount = random.randint(1,1000001)
    transaction += "Amount: " + str(amount) + "\n"
    (s, r) = DS.SignGen(transaction.encode('UTF-8'), q, p, g, payerAlpha)
    transaction += "Signature (s): " + str(s) + "\n" 
    transaction += "Signature (r): " + str(r) + "\n"
    

    return transaction

def gen_random_txblock(q, p, g, TxCnt, filename):
    with open(filename, "w", newline='') as out_file:
        for i in range(TxCnt):
            tx = gen_random_tx(q,p,g)
            out_file.write(tx)
    out_file.close()
