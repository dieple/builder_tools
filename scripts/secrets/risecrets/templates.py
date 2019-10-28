import fileinput
import re

from .aws_secrets import SecretException, get_secret

SECRET_PATTERN = "<<secret\/(?P<namespace>\S+)\/(?P<group>\S+)\/(?P<key>\S+)>>"


# Look for the first match in every line
def find_tag(text):
    if text is None:
        return None, None
    pattern = re.compile(SECRET_PATTERN)
    match = re.findall(pattern, text)

    if len(match) == 0 or len(match[0]) != 3:
        return None, None

    return (
        {"namespace": match[0][0], "group": match[0][1], "key": match[0][2]},
        "<<secret/{}/{}/{}>>".format(match[0][0], match[0][1], match[0][2]),
    )


# Opens a file and replaces all the secret tag matches with the key retrieved
# from secrets manager
def process_file(filepath):
    counter = 0

    # works by printing stdout to the file
    with fileinput.FileInput(filepath, inplace=True, backup="") as procfile:
        for line in procfile:
            tag, full_text = find_tag(line)

            # if not tag is found skip the line
            if tag is None:
                print(line, end="")
                continue

            try:
                secret = get_secret(tag["namespace"], tag["group"], tag["key"])
                print(line.replace(full_text, secret), end="")
                counter += 1
            except SecretException:
                # if there is an error skip the line
                print(line, end="")

    return counter
