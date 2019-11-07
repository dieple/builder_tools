import base64

import json
import boto3


class SecretException(Exception):
    pass


def get_secret(namespace, group, key, region_name="eu-west-1"):
    # Create a Secrets Manager client
    session = boto3.session.Session()

    client = session.client(
        service_name="secretsmanager", region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId="{}/{}".format(namespace, group)
        )
    except Exception as e:
        raise SecretException(e)

    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these
        # fields will be populated.
        if "SecretString" in get_secret_value_response:
            val = json.loads(get_secret_value_response["SecretString"])

            if val[key] is not None:
                return val[key]
            return None
        else:
            return base64.b64decode(get_secret_value_response["SecretBinary"])
