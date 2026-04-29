import rsaKey as rsa
import KeyGenerator as keygen

pub, pri = keygen.generate_keypair(1024 )
print("pub:", pub.e, pub.n)
print("pri:", pri.e, pri.n)

text = pub.encrypt("HELLO I AM ZACHARY PETERSON AND I AM MAKEING THIS A VERY LONG TEXT STRING")
print(text)
text = pri.decrypt(text)
print(text)