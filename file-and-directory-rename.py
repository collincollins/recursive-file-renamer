import os
import argparse
import logging
import json
import re

def setup_logging():
    """
    Sets up the basic configuration for logging.
    This configures logging to output messages with the INFO level and higher.
    """
    logging.basicConfig(level=logging.INFO, format='%(message)s')

def rename_entry(old_path, new_name, dry_run, rename_log, max_name_length):
    """
    Renames a single file or directory from old_path to new_name.
    If dry_run is True, the renaming will only be logged and not executed.
    The rename_log is updated with the renaming action for potential rollback.
    """
    old_file_name = os.path.basename(old_path)
    new_file_name = os.path.basename(new_name)
    if dry_run:
        logging.info(f"[Dry Run] Would rename '{old_file_name: <{max_name_length}}' to '{new_file_name}'")
    else:
        try:
            os.rename(old_path, new_name)
            logging.info(f"Renamed '{old_file_name: <{max_name_length}}' to '{new_file_name}'")
            rename_log.append((new_name, old_path))
        except OSError as error:
            logging.error(f"Error renaming '{old_file_name}': {error}")

def should_rename(name):
    """
    Determines if a file or directory name should be renamed.
    Renaming is necessary if there are spaces, underscores, or uppercase characters.
    """
    return ' ' in name or '_' in name or name != name.lower()

def get_new_name(name):
    """
    Generates a new name for a file or directory.
    It replaces spaces and underscores with hyphens and converts all characters to lowercase.
    """
    base, ext = os.path.splitext(name)
    base = base.replace(' ', '-').replace('_', '-')
    base = re.sub(r'[^a-zA-Z0-9.]+', '-', base)
    return f"{base}{ext}".lower()

def is_hidden(file_path):
    """
    Checks if a file or directory is hidden.
    Hidden files start with a dot.
    """
    return os.path.basename(file_path).startswith('.')

def collect_renames(directory_path):
    """
    Collects a list of files and directories that need to be renamed.
    This is a recursive function that walks through all subdirectories.
    Returns a list of tuples (old_path, new_path).
    """
    file_renames = []
    dir_renames = []
    for entry in os.listdir(directory_path):
        entry_path = os.path.join(directory_path, entry)
        if is_hidden(entry_path) or os.path.islink(entry_path):
            continue

        new_name = get_new_name(entry)
        new_path = os.path.join(directory_path, new_name)

        if os.path.isdir(entry_path):
            dir_renames.append((entry_path, new_path))
            file_renames += collect_renames(entry_path)
        elif should_rename(entry):
            file_renames.append((entry_path, new_path))

    return file_renames + dir_renames  # Files first, then directories

def rename_recursively(directory_path, dry_run):
    """
    Renames files and directories in the given directory recursively.
    If dry_run is True, no actual renaming is done.
    Returns a log of renaming actions.
    """
    rename_log = []
    to_rename = collect_renames(directory_path)
    max_name_length = max(len(os.path.basename(old)) for old, new in to_rename)

    for old_path, new_path in to_rename:
        rename_entry(old_path, new_path, dry_run, rename_log, max_name_length)

    return rename_log

def undo_renames(rename_log):
    """
    Undoes the renaming actions recorded in the rename_log.
    This function renames the files/directories back to their original names.
    """
    if not rename_log:
        logging.info("No rename operations to undo.")
        return

    max_name_length = max(len(os.path.basename(new)) for new, old in rename_log)

    for new_path, old_path in reversed(rename_log):
        new_file_name = os.path.basename(new_path)
        old_file_name = os.path.basename(old_path)
        try:
            os.rename(new_path, old_path)
            logging.info(f"Undo: Renamed back '{new_file_name: <{max_name_length}}' to '{old_file_name}'")
        except OSError as error:
            logging.error(f"Error undoing rename: {error}")

def save_rename_log(rename_log, file_name='rename_log.json'):
    """
    Saves the rename log to a file.
    The log file contains the details of renaming actions for potential undo operations.
    """
    with open(file_name, 'w') as file:
        json.dump(rename_log, file, indent=4)

def load_rename_log(file_name='rename_log.json'):
    """
    Loads the rename log from a file.
    This is used for the undo functionality to revert changes.
    """
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("No rename log file found for undo operation.")
        return []

def main():
    """
    The main function handling the script execution.
    Parses command-line arguments and invokes the renaming functions.
    """
    parser = argparse.ArgumentParser(description='Rename files and directories recursively, ignoring hidden files.')
    parser.add_argument('directory', type=str, help='The directory whose contents will be renamed.')
    parser.add_argument('--dry-run', action='store_true', help='Simulate the renaming process without making changes.')
    parser.add_argument('--undo', action='store_true', help='Undo the last renaming operation.')
    args = parser.parse_args()

    setup_logging()

    if args.undo:
        rename_log = load_rename_log()
        undo_renames(rename_log)
    else:
        rename_log = rename_recursively(args.directory, args.dry_run)
        save_rename_log(rename_log)

if __name__ == "__main__":
    main()
