"Main entry point module"
import argparse
import logging
import os
import subprocess
import sys
from rmux import __version__


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description="""\
The list of hosts is loaded from ${bold}HOSTS${reset} environment variable \
and when this is not defined it will fallback to using localhost, still even \
in this case it will use ssh."""
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-w", dest="url", default=None, help="Download script from url and execute it"
    )
    parser.add_argument("args", nargs="*", help="Remote commands to run (optional)")
    args = parser.parse_args()
    print(args)

    hosts_str = os.environ.get("HOSTS", None)
    if not hosts_str:
        hosts_str = "localhost"
        logging.warning(
            "Warning: using localhost fallback, define HOSTS as a space separated list"
        )
    hosts = hosts_str.split(" ")

    project_dir = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"],
        stderr=subprocess.DEVNULL,
        universal_newlines=True,
    ).splitlines()[0]

    if not project_dir:
        logging.error(
            "Unable to detect project_dir, rmux can only be run inside a git repository."
        )
        sys.exit(1)

    project_name = os.path.basename(project_dir)
    remote_dir = f".cache/.rmux/{project_name}"
    logging.info(f"Found project {project_name} in {project_dir}")

    subprocess.run(
        ["git", "ls-files", "--exclude-standard", "-oi", "--directory"],
        stdout=open(f"{project_dir}/.git/ignores.tmp", "w"),
        cwd=project_dir,
    )

    for host in hosts:
        subprocess.run(
            ["ssh", host, "mkdir", "-p", remote_dir], cwd=project_dir, check=True
        )
        subprocess.run(
            f"rsync -ah --no-o --no-g --delete-after --include .git \
            --exclude-from={project_dir}/.git/ignores.tmp --exclude '__pycache__' \
            {project_dir}/ {host}:{remote_dir}/",
            shell=True,
            cwd=project_dir,
            check=True,
        )

    xpanes_opt = "-ss"
    inject = ""
    # -l added to shell to make it act as login and load user profile (vars)
    # keep a space before the command to avoid polluting the shell history
    # cannot use $SHELL here because it may not exit on remote
    cmd = f"sh -i -l <<< ' cd ~/{remote_dir};"
    if not args.args:
        logging.info("No command specified, just starting ssh sessions")
        cmd += f"{inject}exec </dev/tty'"
    else:
        cmd += f"{inject} {' '.join(args.args)};exec </dev/tty'"

    subprocess.run(
        # "xpanes", xpanes_opt, "-t", "-c",
        f'ssh -XY -t -o StrictHostKeyChecking=no {hosts_str} "{cmd}"',
        #  hosts_str
        cwd=project_dir,
        shell=True,
        check=True,
    )
