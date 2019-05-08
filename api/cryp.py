from cryptography.fernet import Fernet


# key = base64.urlsafe_b64encode(os.urandom(32))  生成key


# 密码加密
def encrypt_p(password):
    f = Fernet('fgii9RoEIvoJ1oPKdbFsMCbIybe94qeQM1_dWkuMtwQ=')
    p1 = password.encode()
    token = f.encrypt(p1)
    p2 = token.decode()
    return p2


# 密码解密
def decrypt_p(password):
    f = Fernet('fgii9RoEIvoJ1oPKdbFsMCbIybe94qeQM1_dWkuMtwQ=')
    p1 = password.encode()
    token = f.decrypt(p1)
    p2 = token.decode()
    return p2
