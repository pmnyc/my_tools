# Tools
Python, R and other small handy tools

# Remark

- To import/export Visual Studio Code extensions installed, first install extension **VSC Extension Export & Import**, then in the `Command Palette`, type in `VSC Export` or `VSC Import` the `vsc-extensions.txt` file.
- .gitignore file can help specify which files will be ignored by git when adding or commiting files in git or GitHub
- Create the environment from the .yaml files `conda env create --file=myfile.yaml`. Export existing environment by `conda env export > myfile.yml`.

# How to freeze Python program into an .exe executable
- Try to make the virtual environment as small as possible.
- In the folder for hosting the virtual environment, run `$ python -m venv .` --> `$ cd Scripts` --> `$ activate` . Here the python environment can be an Anaconda one.
- After activating the virutal environment, use pip to install few necessary pacakes such as numpy, pandas, requests, pyinstaller, xlwings, etc.
- To create an Excel file macro that uses stand-alone Python exe program, in VBA import `xlwings.bas` from where the xlwings is installed. More examples refer to ![xlwings-demo](https://github.com/xlwings/xlwings-demo)'s frozen folder.
- Use `$ pyinstaller <file>.py --clean` to create the stand-alone .exe for Excel. Add option `--onefile` to make single file exe, either specify the packages to exclude in the .spec file or use option `--exclude pandas` alike to exclude pandas to be wrapped in the exe file. The VBA code of running frozen python can be found in the demo.xlsm file in the ![xlwings-demo](https://github.com/xlwings/xlwings-demo)'s frozen folder.
