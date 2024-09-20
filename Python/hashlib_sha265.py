import hashlib
m = hashlib.sha256()
m.update(b"Nobody inspects")
m.update(b" the spannish repetition")
# i'm (not that) hilarious
m.digest()
m.hexdigest()
