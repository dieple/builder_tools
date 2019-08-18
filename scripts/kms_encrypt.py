import boto3
import base64
import argparse


def process_arguments():
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('--keyId', help='Kms key Id or alias', required=True)
    required.add_argument('--plainText', help='Plaintext password to encrypt', required=True)
    #parser._action_groups.append(optional)
    return parser.parse_args()


if __name__ == '__main__':

    args = process_arguments()

    session = boto3.session.Session()

    kms = session.client('kms')

    stuff = kms.encrypt(KeyId=args.keyId, Plaintext=args.plainText)
    binary_encrypted = stuff[u'CiphertextBlob']
    encrypted_password = base64.b64encode(binary_encrypted)
    print(encrypted_password.decode())