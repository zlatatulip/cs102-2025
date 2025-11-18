def encrypt_affine(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    s = [
        range(ord("A"), ord("Z") + 1),
        range(ord("a"), ord("z") + 1),
        range(ord("А"), ord("Я") + 1),
        range(ord("а"), ord("я") + 1),
    ]
    for n, i in enumerate(plaintext):
        shift = ord(keyword[n % len(keyword)].upper()) - ord("A")
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


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    s = [
        range(ord("A"), ord("Z") + 1),
        range(ord("a"), ord("z") + 1),
        range(ord("А"), ord("Я") + 1),
        range(ord("а"), ord("я") + 1),
    ]
    for n, i in enumerate(ciphertext):
        shift = ord(keyword[n % len(keyword)].upper()) - ord("A")
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
