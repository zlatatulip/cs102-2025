def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    s = [range(ord('A'), ord('Z') + 1), range(ord('a'), ord('z') + 1), range(ord('А'), ord('Я') + 1), range(ord('а'), ord('я') + 1)]
    for i in plaintext:
        t1 = ord(i)
        t2 = ord(i) + shift
        flag = 0
        for j in s:
            if t1 in j:
                while t2 not in j:
                    t2 -= len(j)
                flag = 1
                break
        if flag:
            ciphertext += chr(t2)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    s = [range(ord('A'), ord('Z') + 1), range(ord('a'), ord('z') + 1), range(ord('А'), ord('Я') + 1), range(ord('а'), ord('я') + 1)]
    for i in ciphertext:
        t1 = ord(i)
        t2 = ord(i) - shift
        flag = 0
        for j in s:
            if t1 in j:
                while t2 not in j:
                    t2 += len(j)
                flag = 1
                break
        if flag:
            plaintext += chr(t2)
        else:
            plaintext += i
    return plaintext
