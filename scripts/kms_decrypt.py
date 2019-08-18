import boto3
import base64
import argparse

def process_arguments():
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('--encryptedText', help='Encrypted text to decrypt', required=True)
    #parser._action_groups.append(optional)
    return parser.parse_args()

if __name__ == '__main__':

    args = process_arguments()

    session = boto3.session.Session()

    kms = session.client('kms')

    encrypted_password = args.encryptedText
    binary_data = base64.b64decode(encrypted_password)
    meta = kms.decrypt(CiphertextBlob=binary_data)
    plaintext = meta[u'Plaintext']
    print(plaintext.decode())