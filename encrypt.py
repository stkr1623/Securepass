def encrypt_aes(key, plaintext):
    ep=""
    for i in plaintext:
        ch=chr(ord(i)+key)
        ep+=ch
    return ep