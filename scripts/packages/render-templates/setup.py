import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="render-templates",
    version="0.0.1",
    author="RI Tech",
    scripts=["render-templates"],
    author_email="ritech@river-island.com",
    description="Jinja2 template to search and replace environment variables to deploy between different stages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/river-island/eks-deployments",
    packages=setuptools.find_packages(),
    install_requires=["jinja2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
