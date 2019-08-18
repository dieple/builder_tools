# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import base64
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "rds_automic_staging"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    print ("get_secret_value_response: {0}".format(get_secret_value_response))
    print("secret: {0}".format(secret))
    # get_secret_value_response: {'CreatedDate': datetime.datetime(2019, 6, 17, 16, 39, 59, 781000, tzinfo=tzlocal()), 'ResponseMetadata': {'RetryAttempts': 0, 'RequestId': '9f66c5dc-f01b-4db6-b5df-4b05cdb8da1a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-length': '487', 'content-type': 'application/x-amz-json-1.1', 'date': 'Mon, 17 Jun 2019 16:45:50 GMT', 'x-amzn-requestid': '9f66c5dc-f01b-4db6-b5df-4b05cdb8da1a', 'connection': 'keep-alive'}}, 'Name': 'rds_automic_staging', 'VersionStages': ['AWSCURRENT'], 'SecretString': '{"username":"postgres","password":"TpzDXopaqNmXbQ","engine":"postgres","host":"rds.cluster-cluedkbzvjvw.eu-west-1.rds.amazonaws.com","port":5432,"dbname":"automic_staging_rds_cluster","dbClusterIdentifier":"rds"}', 'VersionId': '262b1f04-ce7e-4b3a-b0f1-7b96be63caf2', 'ARN': 'arn:aws:secretsmanager:eu-west-1:558469419837:secret:rds_automic_staging-PDs6wr'}

# Your code goes here.
if __name__ == '__main__':
    get_secret()

