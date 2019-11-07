#! /usr/bin/env python3

import argparse
import json
import os
import sys
import copy
import re

from jinja2 import Template

debug = False

def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def print_bad_args_and_exit_1(parser, msg):
    print_err(msg)
    parser.print_help()
    sys.exit(1)

def print_debug(msg):
    if debug:
        print(msg)

def get_rsync_source_and_target_dir(source_dir, target_dir):
    """
    :param source_dir:
    :param target_dir:
    :return: source_dir, target_dir where:
    source_dir has a trailing '/'
    target_dir is "<target_dir>/rendered/<basename of source_dir>" without trailing slash '/'
    """
    source_dir = str.rstrip(source_dir, '/') + '/'  # ensure trailing slash in return value
    source_dir_name = str.rstrip(os.path.basename(source_dir), '/')
    target_dir = str.rstrip(target_dir, '/')
    target_dir = "{target_dir}/rendered/{source_dir_name}".format(target_dir=target_dir,
                                                                  source_dir_name=source_dir_name)
    return source_dir, target_dir

def find_template_files(dir_name):
    """
    Walk directory supplied to find .template files.
    Return the list of .template files found.
    """
    list_files = []
    for dirName, subdirList, fileList in os.walk(dir_name):
        # Construct file path relative to the dir_name.
        for file_name in fileList:
            fp = os.path.join(dirName, file_name)
            r = re.compile(".+\.template$")
            if r.match(fp):  # if the file is a .template...
                # Save the template file for later.
                print_debug("Found template file {}".format(fp))
                list_files.append(fp)
    return list_files

def get_template_render_metadata(template_file_list, values_dict, subdir_to_trim):
    files_and_values_list = []
    for f in template_file_list:  # for each template file full relative path...
        # Build a dict of template global values.
        template_values_dict = {}
        if "globals" in values_dict:  # if there are global template values...
            template_values_dict = copy.deepcopy(values_dict["globals"])
        # Update the dict with template-specific values.
        # Remove the rsync target directory from the file path to find the key.
        key = str.replace(f, subdir_to_trim, "")
        if key in values_dict["templates"]:  # if there are values for this template file...
            template_values_dict.update(values_dict["templates"][key])
        else:
            sys.exit("Missing entry in values JSON for template '{}'.\n"
                     "Add an empty entry if no values are required for this template.".format(key))

        # Save the target file name for rendered output.
        rendered_file = str.replace(f, ".template", "")
        # Save all require metadata as a dict in a list.
        files_and_values_list.append({"templateFile": f,
                                      "renderedFile": rendered_file,
                                      "values": template_values_dict})
    return files_and_values_list

def render_templates(files_and_values_list):
    for d in files_and_values_list:  # for each template file...
        # Render the template using values.
        str = render_template(d["templateFile"], d["values"])
        # Save the rendered template to the supplied renderedFile.
        f = open(d["renderedFile"], 'w')
        f.write(str)
        f.close()


def render_template(template, values):
    with open(template, 'r') as f:
        t = Template(f.read())
        return t.render(**values)

def main():
    global debug
    # Get args.
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Render .template files found in source directory by making a copy "
                                                 "into the supplied target directory, before rendering them using the "
                                                 "supplied values file (JSON)")
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument("-s", "--source", action="store", help="The source directory containing templates to render",
                        default=argparse.SUPPRESS)
    parser.add_argument("-t", "--target", action="store", help="The target directory to create rendered template in",
                        default=argparse.SUPPRESS)
    parser.add_argument("-f", "--values-file", action="store", help="The JSON values file to populate templates",
                        default=argparse.SUPPRESS)
    args = parser.parse_args()


    if args.debug:
        debug = args.debug
    # Validate args.
    if not hasattr(args, "source") or not os.path.isdir(args.source):
        print_bad_args_and_exit_1(parser, "Invalid source directory")
    if not hasattr(args, "target") or not os.path.isdir(args.target):
        print_bad_args_and_exit_1(parser, "Invalid target directory")
    if not hasattr(args, "values_file") or not os.path.isfile(args.values_file):
        print_bad_args_and_exit_1(parser, "Invalid values file")
    # Load the values file to validate its format.
    with open(args.values_file, 'r') as f:
        values_dict = json.load(f)
    rsync_source, rsync_target = get_rsync_source_and_target_dir(args.source, args.target)
    rsync_cmd = "rsync -au --delete-after {rsync_source} {rsync_target}".format(rsync_source=rsync_source, rsync_target=rsync_target)
    # Dump values
    print_debug("Source template dir = {}".format(rsync_source))
    print_debug("Target template dir = {}".format(rsync_target))
    print_debug("Values file = {}".format(args.values_file))
    print_debug("Rsync command = {}".format(rsync_cmd))
    print_debug("Values = {}".format(values_dict))
    # Rsync the source templates into the target directory.
    os.system(rsync_cmd)
    # List the templates.
    template_file_list = find_template_files(rsync_target)
    # Get the template file keys found in values json file.
    files_and_values_list = get_template_render_metadata(template_file_list, values_dict, rsync_target)
    # Process each template file.
    print_debug("File and values for replacement = {}".format(json.dumps(files_and_values_list, indent="  ")))
    render_templates(files_and_values_list)


