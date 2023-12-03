# Recursive File Renamer

## Description
Recursive File Renamer is a Python script designed to rename files and directories within a specified directory recursively. It improves naming consistency by replacing spaces and underscores with hyphens and converting all characters to lowercase. The script includes a dry run option to preview changes without making actual modifications and provides an undo feature to revert changes if needed.

## Features
- **Recursive Renaming**: Renames files and directories within a given directory.
- **Custom Naming Convention**: Replaces spaces and underscores with hyphens and converts names to lowercase.
- **Dry Run Option**: Simulates renaming to preview changes without applying them.
- **Undo Functionality**: Allows reverting the last set of changes made by the script.
- **Logging**: Logs all operations, which can be useful for tracking changes and debugging.

## Requirements
- Python 3.x

## Installation
To install the Recursive File Renamer, clone the repository to your local machine:
```bash
git clone https://github.com/collincollins/recursive-file-renamer.git
cd recursive-file-renamer
```

## Usage
Run the script from the command line by providing the target directory. For example:
```bash
python file-and-directory-rename.py ./example_directory --dry-run
```
Options:
- `--dry-run`: Preview changes without applying them.
- `--undo`: Revert the last renaming operation.

## Contributing
Your contributions are welcome! If you have a suggestion that would improve this project, please fork the repository and create a pull request. You can also open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks!

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/collincollins/recursive-file-renamer/blob/main/LICENSE) file for details.

## Contact
If you have any questions or feedback, feel free to reach out to me at [cc269020@ohio.edu](mailto:cc269020@ohio.edu).
