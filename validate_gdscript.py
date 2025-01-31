"""
    This script uses Godot to validate every GDScript file in the project.
    You need to set GODOT_PATH env variable to the Godot exe.
"""

import os
from pathlib import Path
import subprocess
import fnmatch
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

# Treat this like gitignore
IGNORE_PATHS = [
    "addons/gdUnit4/**",
]


def matches_ignore(path: str, ignore_paths: list[str]) -> bool:
    for ignore in ignore_paths:
        if fnmatch.fnmatch(path, ignore):
            return True
    return False


def gather_scripts(path: str, ignore_paths: list[str] = []) -> list:
    script_files = []
    for path in Path(".").rglob("*.gd", case_sensitive=False):
        if matches_ignore(path, ignore_paths):
            continue
        script_files.append(path)
    return script_files


def validate_paths(script_files: list[str]) -> list[str]:
    failed_scripts = []

    godot = os.environ.get("GODOT_PATH")
    if not godot:
        raise Exception("GODOT_PATH env var not set.")

    num_scripts = len(script_files)
    for i, filepath in enumerate(script_files):
        print(f"{i+1}/{num_scripts} {filepath} ... ", end="")
        output = subprocess.run(
            [
                godot,
                "./project.godot",
                "--check-only",
                "--headless",
                "--quiet",
                "-s",
                f"{filepath}",
            ],
            capture_output=True,
            text=True,
        )
        if output.returncode == 0:
            print(f"{Fore.GREEN}OK{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}ERR{Style.RESET_ALL}")
            failed_scripts.append(output)
    return failed_scripts


colorama_init()

os.chdir("project")
script_files = gather_scripts(".", IGNORE_PATHS)
failed_scripts = validate_paths(script_files)
num_fails = len(failed_scripts)
print("")
if num_fails == 0:
    print("All scripts passed validation!")
    exit(0)
else:
    for output in failed_scripts:
        print(f"{Fore.RED}Failed:{Style.RESET_ALL} {output.args[-1]}")
        print(f"{Fore.WHITE}{output.stderr}{Style.RESET_ALL}")
    print(
        f"{Fore.RED}{num_fails} {"file" if num_fails == 1 else "files"} failed script validation{Style.RESET_ALL}"
    )
    print("stderr output from failed scripts have been gathered above.")
    exit(1)
