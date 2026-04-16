class rsaKey:
    n = None
    e = None
    d = None
    p = None
    q = None
    bitlength = None
    def __init__(self,e,d,p,q,bitlength):
        self.n = p*q
        self.e = e
        self.d = d
        self.p = p
        self.q = q
        self.bitlength = bitlength
        T = (p-1)(q-1)

