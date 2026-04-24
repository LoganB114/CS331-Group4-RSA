import rsaKey as rsa
import KeyGenerator as keygen

pub, pri = keygen.generate_keypair(1024, 5915587277,  1500450271 )
print("pub:", pub.e, pub.n)
print("pri:", pri.e, pri.n)

text = pub.encrypt("HELLO")
print(text)
text = pri.decrypt(text)
print(text)