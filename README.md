## DirTree

```
usage: dirtree.py [-h] [--filters FILTERS] [--empty-directories] [--ignore IGNORE] [dir]

Directory Tree

positional arguments:
  dir                  Path to the root directory (default: current directory)

options:
  -h, --help           show this help message and exit
  --filters FILTERS    Comma separated list of file patterns (e.g. *.py,*.cpp,README.md). Use _ for files without extension
  --empty-directories  Show empty directories
  --ignore IGNORE      Comma separated list of patterns to ignore (e.g. node_modules/*,*.tmp)
 ```

### Usage

Have you ever needed to quickly display the tree structure of your project?
You project `Tetris`might for instance contain 

```
.git
.idea
README.md
main.py
requirements.txt
tetris.png
venv
```

But you don't want to show all that and still make an easy overview of everything relevant. DirTree helps you do it in no time.

Run: `./dirtree.py /home/foo/workspace/tetris/ --filters "*.py,*.md" --ignore ".git,.idea,venv"`

and you would get.

```
📁 tetris/
  📄 README.md
  📄 main.py  
```
