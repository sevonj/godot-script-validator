# godot-script-validator

This Python script will validate GDScript files in your project. It can be a very usefult CI check.

## Limitations

- This is not compatible with autoloads, because Godot doesn't load them when checking scripts.

## Usage

- Set `GODOT_PATH` env variable to the path of your Godot editor: `export GODOT_PATH=/path/to/editor`
- Run `python validate_gdscript.py`

The script expects to find the project from `./project/project.godot`. Customize as needed.

Relevant parts from my own github workflow:

```yml
# main.yml
name: CI

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  validate-gdscript:
    name: Nonstatic Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download Godot
        working-directory: ./project
        run: |
          wget https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_linux.x86_64.zip
          unzip Godot_v4.3-stable_linux.x86_64.zip

      - name: Generate project cache
        working-directory: ./project
        run: ./Godot_v4.3-stable_linux.x86_64 ./project.godot --headless --import

      - name: Validate GDScript
        run: python validate_gdscript.py
        env:
          GODOT_PATH: "./Godot_v4.3-stable_linux.x86_64"

```
