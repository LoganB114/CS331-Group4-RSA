import rsaKey as rsa
import KeyGenerator as keygen

pub, pri = keygen.generate_keypair(1024 )
print("pub:", pub.e, pub.n)
print("pri:", pri.e, pri.n)
text = "HELLO I AM ZACHARY PETERSON AND I AM MAKEING THIS A VERY LONG TEXT STRING"
print(bytearray(text, "utf-8"))
text = pub.encrypt(text)
print(text)
text = pri.decrypt(text)
print(text)