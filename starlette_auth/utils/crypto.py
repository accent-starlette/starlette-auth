import hashlib
import hmac
import secrets


def salted_hmac(key_salt, value, secret):
    """
    Return the HMAC-SHA1 of 'value', using a key generated from key_salt and a
    secret. A different key_salt should be passed in for every application of HMAC.
    """

    assert secret, f"secret must be provided."

    key_salt = bytes(key_salt, encoding="utf-8")
    secret = bytes(secret, encoding="utf-8")

    # We need to generate a derived key from our base key.  We can do this by
    # passing the key_salt and our base key through a pseudo-random function and
    # SHA1 works nicely.
    key = hashlib.sha1(key_salt + secret).digest()

    # If len(key_salt + secret) > sha_constructor().block_size, the above
    # line is redundant and could be replaced by key = key_salt + secret, since
    # the hmac module does the same thing for keys longer than the block size.
    # However, we need to ensure that we *always* do this.
    return hmac.new(key, msg=bytes(value, encoding="utf-8"), digestmod=hashlib.sha1)


def constant_time_compare(val1, val2):
    """Return True if the two strings are equal, False otherwise."""

    return secrets.compare_digest(
        bytes(val1, encoding="utf-8"), bytes(val2, encoding="utf-8")
    )
