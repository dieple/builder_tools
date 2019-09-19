## Introduction

A python script to create, build and run the docker image. Once the docker image is up and running you'll get a bash shell as a local development environment on your host PC.
Within this repo you can perform Infrastructure as Code (IaC) using 
* [terrascript](https://github.com/mjuenema/python-terrascript)
* Ansible
* Kubernetes
* Helm
* Terraform
* AWS CLI
* aws-vault

## Why would I wanna use this?

* Quick, easy and repeatable method to setup your local development environment.
* Isolated from your host PC. Don't have to worry about software version conflicts with your host environment. 
* Every developer using this tool will have the same version of software

## Software installed
* Python3
* python-terraform --> provides a wrapper of `terraform` command line tool
* python-terrascript --> generates terraform code using python.
* Terraform binary (defaults to v0.11.7 for enactor development but can be overidden)
* Ansible  (defaults to v2.5.0 but can be overidden)
* AWS CLI
* AWS Vault --> Profiles, MFA and roles switching capability
* Kubectl
* Helm

The packages are build using pip install if possible, further addons can be included during docker image build stage.

## Prerequisites

* Install docker on the host machine
* Python3 on host machine
* Create developer AWS IAM account, setup MFA on AWS console and noted down the MFA ARN.
* A note of your MFA ARN for use below
* A note of your AWS access keys which you created above for your IAM user in the AWS root account
* AWS client on your host machine
* aws-vault on your host machine
* Manually create file `$HOME/.aws/config` on your host machine with entries for the 
AWS accounts you want to access - see below
* Manually create `$HOME/.kube` directory for Kubernetes
* Personal SSH keys created on your host machine and added to your GitHub settings (the ability to clone repos using SSH)  

__`$HOME/.aws/config`__ 

To get started with this file, either take the entries shown below 
or use the sample file [here](./samples/aws-config.txt)
and edit to match your IAM user, MFA and account IDs  

The sample file contains entries for DataOps AWS accounts.
All you need to do is replace text, 'dieple', with your IAM user name.

```
[default]
region=eu-west-1

[profile dev]
mfa_serial=arn:aws:iam::<mfa-aws-account-id>:mfa/aws_iam_account
role_arn=arn:aws:iam::<switch-role-aws-account-id>:role/developers

[profile staging]
mfa_serial=arn:aws:iam::<mfa-aws-account-id>:mfa/aws_iam_account
role_arn=arn:aws:iam::<switch-role-aws-account-id>:role/developers
```


### Steps

First, clone this repo:

```bash
$> mkdir $HOME/repos
$> cd $HOME/repos
$> git clone https://github.com/dieple/builder_tools.git
$> cd builder_tools
```

Now there are two options to get going. Choose one of these:

1) Create your own launch script  __<<< recommended__
1) Execute the `builder.py` and supply a bunch of parameters


#### Option 1 - Create Your Own Launch Script
 
```bash
$> # Duplicate an existing script as follows...
$> cp users/relloyd-run_builder.sh users/<your name>-run_builder.sh
```

Customise the contents of your new script to include your GitHub username 
and path to your source code:

```bash
$> vi users/<your name>-run_builder.sh

# Find these lines in the script and set them to 
# match your name and path to your source code:

# --githubUsername=dieple          <<< change this to your GitHub user name
# --githubEmail=dieple1@gmail.com   <<< set this to the email address used with your GitHub account
# --shareHostVolume=$HOME/repos     <<< set this to match the path to your repos (not the builder-tools directory; 
# use the parent of builder_tools so you can cd into other repos from withing the docker image
# this path will be mounted into the Docker image that you build below...)
```

Execute the following script to build & run the Docker image.
The aws-vault profile name that you supply should be one matching an entry in 
the `~/.aws/config` file above.
 
```bash
$> chmod +x users/<your name>-run_builder.sh  # <<< add execute privs if they're not there already
$> users/<your name>-run_builder.sh <aws-vault-profile-name>
    
... snip
Successfully built 4f84992ea3d1
Successfully tagged cloudops:latest
2019-02-20 16:58:52,107 - root - INFO - run_command: docker run --interactive --tty -u devops --rm --volume "$HOME/.aws:/home/devops/.aws" --volume "$HOME/repos:/repos" cloudops /bin/bash

Enter Access Key ID:                                      <<< Enter your AWS root account IAM user access key ID
Enter Secret Access Key:                                  <<< Enter your AWS root account IAM user secret key
Enter passphrase to unlock /home/devops/.awsvault/keys/:  <<< Optionally supply a password - normally blank for your personal machine
Added credentials to profile "dev" in vault
Enter passphrase to unlock /home/devops/.awsvault/keys/:                  <<< Ditto
Enter token for arn:aws:iam:::<aws-account-number-mfa>/<github-user-id>:  <<< Supply your one-time MFA code  
Enter passphrase to unlock /home/devops/.awsvault/keys/:                  <<< Optionally supply a password - normally blank for your personal machine
devops@67fb998d20da:/repos$  
```

Voila you now have a development environment (built within a few minutes) on your host PC or Mac!

Note that `$HOME/repos` is where I checked out the git repos and can be seen in `/repos` in the docker image, where you can run terraform plan, etc. 


#### Option 2 - Execute builder.py

After executing the below, follow instructions

```bash
$ cd builder_tools   
$ python3 builder.py -h

usage: setup.py [-h] --githubUsername GITHUBUSERNAME --githubEmail GITHUBEMAIL
              --profile PROFILE [--imageName IMAGENAME]
              [--terraformVersion TERRAFORMVERSION]
              [--ansibleVersion ANSIBLEVERSION]
              [--dockerAppUser DOCKERAPPUSER]
              [--installAnsible [INSTALLANSIBLE]]
              [--installTerraform [INSTALLTERRAFORM]]

Required arguments:
  --githubUsername GITHUBUSERNAME
                        Github username
  --githubEmail GITHUBEMAIL
                        Github email
  --profile PROFILE     Profile to use with aws-vault

optional arguments:
  -h, --help            show this help message and exit
  --imageName IMAGENAME
                        Docker image name
  --terraformVersion TERRAFORMVERSION
                        Terraform version
  --ansibleVersion ANSIBLEVERSION
                        Ansible version
  --dockerAppUser DOCKERAPPUSER
                        Docker OS App user
  --installAnsible [INSTALLANSIBLE]
                        Install ansible?
  --installTerraform [INSTALLTERRAFORM]
                        Install Terraform?
```

## What Next?

### DataOps Deployments

Voila you now have a development environment (built within a few minutes) on your host PC!

Note that $HOME/repos is where I checked out the git repos and can be seen in /repos in the docker image, where you can run terraform plan, etc. 
```    


## Tidy up...
```bash
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
cloudops            latest              397f27ce6b84        17 seconds ago      787MB
<none>              <none>              11035dde5ea5        18 hours ago        787MB
ubuntu              16.04               7e87e2b3bf7a        5 weeks ago         117MB

$ docker rmi 397f27ce6b84
Untagged: cloudops:latest
Deleted: sha256:397f27ce6b84e3950f4c88a70993d0e511cd6716baa704e669d56c0e7a0de4fb
Deleted: sha256:abddd2e59479a25ae85aa11fe86774872df23a482bf3600e19a711117dedde60
Deleted: sha256:698fc7e394eda565582d71fe908fee4c7b2429df9cd4bac2fd574ac545b6cce2
```


## WARNING

DO NOT push or save the developer image back to docker registry as it's got the developer sensitive keys.

# Terraform Development using Terrascript

#### To create the initial bucket to hold terraform statefile
 
Make sure this line is enable in build.py: "generate_s3(inargs, True, False)"
```bash
$ cd $HOME/repos/
$ git clone git@github.com:dieple/terrascript_011x.git (terraform 0.11.x development)
$ cd terrascript_011x
$ Modify vars/<module>.yaml to meet your environment
$ # Modify run_build.sh to meet your environment
$ run_build.sh
```


#### To create a new VPC
```bash
$ # Make sure this line is in build.py: generate_vpc(inargs)
$ python build.py -a dataops_staging -c false -e staging - p dataops-staging -t true

```
