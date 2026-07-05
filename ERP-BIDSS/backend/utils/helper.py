import hashlib

def generate_surrogate_key(value):
    return hashlib.md5(str(value).encode()).hexdigest()
