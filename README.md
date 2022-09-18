# Temp Table remover

Adds corresponding `DROP TABLE IF EXISTS` statements for all created temp tables at the end of all the scripts inside a target folder.

## 💬 Prerequisites

- Python

## 👷 Usage

- Change `base_path` variable to path of folder you want in `program.py`
  - Use forward slashes in the path (Backwards slash is used in windows paths by default. Change them to forward slashes)
- Save the file
- Run `python program.py`
- Use git to view changes made to scripts

## ✨ Features

- Adds `DROP` statements to all scripts (which have temp tables) in a folder
  - recursive traversal of folders also works
- Avoids adding duplicate `DROP` statements if the program has already been run on a folder.
- Maintains correct indendation for the newly created `DROP` statements in the script.

## 🏗️ In the works

- Add `DROP` statments for newly created temp tables (created after the program has been run on a script)
  - Currently program doesn't monitor for changes in a script it has modified in the past
