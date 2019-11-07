import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ri-secrets",
    version="0.0.1",
    author="RI Tech",
    scripts=["search-and-replace-secrets-from-asm"],
    author_email="ritech@river-island.com",
    description="Populate templates with secrets from AWS Secrets Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/river-island/builder-tools",
    packages=setuptools.find_packages(),
    install_requires=["boto3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
