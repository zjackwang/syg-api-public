import hmac
import hashlib
import argparse


def generate_hmac_signature(message, key):
    hmc = hmac.new(key=key.encode(), msg=message.encode(), digestmod=hashlib.sha256)
    message_digest = hmc.digest()

    return message_digest


def compare_hmac_signatures(a, b):
    return hmac.compare_digest(a, b)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--key",
        help="Pass in the secret key to generate a dummy hmac signature.",
        required=True,
    )
    args = parser.parse_args()

    message = "Welcome to CoderzColumn."
    key = args.key

    message_digest = generate_hmac_signature(message, key)
    print(message_digest)

    with open(".hmac_sig.txt", "wb") as f:
        f.write(message_digest)
