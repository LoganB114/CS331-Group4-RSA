import rsaKey as rsa
import KeyGenerator as keygen

pub, pri = keygen.generate_keypair(1024 )
print("pub:", pub.e, pub.n)
print("pri:", pri.e, pri.n)
print("Max Text Size:", pub.maxDataSize(), pri.maxDataSize())
text = "HELLO I AM ZACHARY PETERSON AND I AM MAKING THIS A VERY LONG TEXT STRING"
print(text)
text = pub.encrypt(bytes(text[0:pub.maxDataSize()], "utf-8"))
print(text)
text = pri.decrypt(text)
print(text)