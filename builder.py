#!/usr/bin/env python

# Use the passed arguments to build and run the cloudops docker image for local development environment
# This is also included aws-vault
import argparse
import logging
# import sys
import os
# from pathlib import Path
from os.path import expanduser

# import subprocess
# import stat

LOGLEVEL = os.getenv('LOG_LEVEL', 'INFO').strip()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL.upper())
log_handler = logging.StreamHandler()
log_handler.setLevel(LOGLEVEL.upper())
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

output_dockerfile = "Dockerfile"
input_dockerfile = "./templates/Dockerfile.template"
docker_entry_file = "./entry.sh"
input_pip_packages_file = "./templates/pip_packages.template"
output_pip_packages_file = "./pip_packages"
terraform_text = "###INSTALL_TERRAFORM###"
aws_vault_text = "###INSTALL_AWS_VAULT###"

home_dir = expanduser("~")


def process_arguments():
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('--githubUsername', help='Github username', required=True)
    required.add_argument('--githubEmail', help='Github email', required=True)
    required.add_argument('--profile', help='Profile to use with aws-vault', required=True)
    required.add_argument('--shareHostVolume',
                          help='Path where all development github repos are checked out. /home/<username>/repos',
                          required=True)
    optional.add_argument('--imageName', help='Docker image name', default='cloudops')
    optional.add_argument('--ansibleVersion', help='Ansible version', default='2.8.3')
    optional.add_argument('--dockerAppUser', help='Docker OS App user', default='cloudops')
    optional.add_argument("--installAnsible", type=str2bool, nargs='?', const=True, default=True,
                          help="Install ansible?")
    optional.add_argument('--terraformVersion', help='Terraform version', default='0.11.14')
    optional.add_argument("--installTerraform", type=str2bool, nargs='?', const=True, default=True,
                          help="Install Terraform?")
    optional.add_argument("--sshKeyDir", default="{0}/.ssh".format(home_dir), help="Host ssh directory")
    optional.add_argument("--awsConfigDir", default="{0}/.aws".format(home_dir), help="AWS config directory")
    optional.add_argument("--kubeConfigDir", default="{0}/.kube".format(home_dir), help="Kubectl config directory")
    optional.add_argument("--sshKeyPassphrase", default="", help="ssh pass phrase")
    # optional.add_argument("--installFlyCLI", type=str2bool, nargs='?', const=True, default=True, help="Install
    # Concourse Fly CLI?")
    optional.add_argument('--flyCLIVersion', help='Concourse FLY CLI version', default='v3.14.1')
    parser._action_groups.append(optional)
    # logger.info("args {0}".format(parser.parse_args()))
    return parser.parse_args()


def str2bool(val):
    if val.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif val.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


def create_docker_entry_file(entry_filename, args):
    with open(entry_filename, 'w', newline='\n') as f:
        gh_email = 'git config --global user.email "{0}"\n'.format(args.githubEmail)
        gh_user = 'git config --global user.name "{0}"\n'.format(args.githubUsername)
        vault_add = "aws-vault add {0}\n".format(args.profile)
        vault_exec = "aws-vault exec --assume-role-ttl=1h --session-ttl=12h {0} -- bash\n".format(args.profile)
        # assume_role = "set -x && . /scripts/assume-role.sh {0} reassume-role\n".format(args.profile)
        # vault_add_mngmt = "aws-vault add {0}\n".format(args.profile.split('-')[0] + "-management")

        if "0.12" in args.terraformVersion:
            clone_repo = 'cd /tmp && git clone https://github.com/mjuenema/python-terrascript.git\n'
            install_terrascript = 'cd /tmp/python-terrascript && git checkout develop && make install && cd /repos\n'

        f.write('#!/bin/bash\n\n')
        f.write('# Please do not modify this file manually as it generate by builder.py\n\n')
        f.write(gh_email)
        f.write(gh_user)

        if "0.12" in args.terraformVersion:
            f.write(clone_repo)
            f.write(install_terrascript)

        f.write(vault_add)
        f.write(vault_exec)

        # f.write(assume_role)
        # f.write("\nhelm init\n")
        # f.write("helm repo update\n")
        # f.write("eval `ssh-agent -s`")
        # f.write("printf '${sshKeyPassphrase}\n' | ssh-add /home/${dockerAppUser}/.ssh/id_rsa")
    # make the entrypoint executable so that the docker image can run on startup
    make_executable(entry_filename)


def create_pip_packages_file(args, input_pip_packages_file, output_pip_packages_file):

    # required development packages to install during docker build image
    with open(input_pip_packages_file) as f:
        with open(output_pip_packages_file, "w", newline='\n') as f1:
            for line in f:
                f1.write(line)

    # add ansible==${version}
    if args.installAnsible == True:
        with open(output_pip_packages_file, "a") as f:
            f.write("ansible=={0}\n".format(args.ansibleVersion))

    if "0.11" in args.terraformVersion:
        # terraform module 0.11.x is used
				# version 0.12.x is dealt with entry.sh file
        with open(output_pip_packages_file, "a") as f:
            f.write("terrascript==0.6.1\n")

def create_dockerfile_from_template(args, dockerfile_template, output_dockerfile):
    with open(dockerfile_template) as fin:
        with open(output_dockerfile, "w", newline='\n') as fout:
            for line in fin:
                if (args.installTerraform):
                    # terraform is required
                    if (line.startswith(terraform_text)):
                        lout = line.replace(terraform_text, '')
                        fout.write(lout)
                    # is also aws-vault required too
                    elif args.profile is not None:
                        # aws-vault is required
                        if (line.startswith(aws_vault_text)):
                            lout = line.replace(aws_vault_text, '')
                            fout.write(lout)
                        else:
                            fout.write(line)
                    else:
                        fout.write(line)

                elif args.profile is not None:
                    # aws-vault is required
                    if (line.startswith(aws_vault_text)):
                        lout = line.replace(aws_vault_text, '')
                        fout.write(lout)
                    else:
                        fout.write(line)
                else:
                    fout.write(line)


def build_docker_image(args, dockerfile):
    # you need to use os.system module to execute shell command
    # build_command = 'docker build --build-arg profile={0} --build-arg terraformVersion={1} --build-arg
    # dockerAppUser={2} --build-arg sshKeyPassphrase={3} --rm -f {4} -t {5}:latest .'.format(args.profile,
    # args.terraformVersion, args.dockerAppUser, args.sshKeyPassphrase, dockerfile, args.imageName)
    build_command = 'docker build --build-arg profile={0} --build-arg terraformVersion={1} --build-arg ' \
                    'dockerAppUser={2} --build-arg sshKey="$(cat {7}/id_rsa)" --build-arg sshKeyPub="$(cat ' \
                    '{7}/id_rsa.pub)" --build-arg sshKeyPassphrase={3} --build-arg flyCLIVersion={4} --rm -f {5} ' \
                    '-t {6}:latest .'.format(
        args.profile, args.terraformVersion, args.dockerAppUser, args.sshKeyPassphrase, args.flyCLIVersion, dockerfile,
        args.imageName, args.sshKeyDir,)

    logger.info("build_command: {0}".format(build_command))
    os.system(build_command)

    # if you want to save the output for later use, you need to use subprocess module
    # child = subprocess.Popen(build_command, stdout=subprocess.PIPE, shell=True)
    # output = child.communicate()[0]
    # logger.info("build output: {0}".format(output))


def run_docker_image(args, dockerfile):
    # for dir in [".ssh", ".aws", ".kube" ]:
    #     os.system("mkdir -p {0}".format(dir))

    tf_cache_plugins_dir = "{0}/.terraform.d/plugin-cache".format(home_dir)

    run_command = 'docker run -e "SET_CONTAINER_TIMEZONE=true" -e "CONTAINER_TIMEZONE=Europe/London" --interactive --tty -u {0} --rm --volume "{1}:/home/{0}/.kube" --volume "{2}:/home/{' \
                  '0}/.ssh" --volume "{3}:/home/{0}/.aws" --volume "{4}:/repos" --volume "{5}:/home/{0}/.terraform.d/plugin-cache" {6} /bin/bash'.format(
        args.dockerAppUser, args.kubeConfigDir, args.sshKeyDir, args.awsConfigDir, args.shareHostVolume, tf_cache_plugins_dir, args.imageName)

    logger.info("run_command: {0}".format(run_command))
    os.system(run_command)


def main():
    args = process_arguments()

    if args.profile is not None:
        # create entry.sh for docker entrypoint (to use with aws-vault)
        create_docker_entry_file("entry.sh", args)

    create_pip_packages_file(args, input_pip_packages_file, output_pip_packages_file)
    create_dockerfile_from_template(args, input_dockerfile, output_dockerfile)
    build_docker_image(args, output_dockerfile)
    run_docker_image(args, output_dockerfile)


if __name__ == '__main__':
    main()
