# STL API

## Motivation
STL API is used to evaluate **Signal Temporal Logic** specification with respect to
an arbitrary signal.

## Installation
### Configure system PATH
  
```bash
export PATH="/path/to/STL-API/bin/directory:$PATH"
```

### Configure PYTHON PATH (for invoking STL API from other modules)

- Temporary Solution:
    ```bash
    import sys
    sys.path.append("/path/to/STL-API/directory/")
    import stl.api
    ```
- Permanent Solution:

  Adding the following line to your shell configuration file (in Unix-based OS). For Mac users, the default shell configuration file is ~/.zshrc
  
  ```bash
  export PYTHONPATH="/path/to/STL-API/directory:$PYTHONPATH"
  ```


### Configure STL PATH (for unit testing and other repository referential operations)
```bash
export STLPATH="/path/to/STL-API/"
```

### Reload `.zshrc` file
  finally, execute the following command on the command line to reload `.zshrc` zsh configuration file

  ```bash
  source ~/.zshrc
  ```

  
### required Platform
- Python3.9+

### required Python packages
- rply (for parser and lexer)
- termcolor (for color printing tools)

## Usage
Below we will be showing a simple example demonstrating the usage of the STL API by evaluating a simple STL expression `G[0, 1](x > y)` with respect to a signal

To begin, we have to import the essential libraries from the STL API
```python
from stl.api import Signal, STL
```

Then, we define a (global) start time in `int` type, as well as defining an arbitrary signal
```python
time_begin = 0
signal = Signal(py_dict={"0": {"content": {"x": 1, "y": 2}},
                         "1": {"content": {"x": 2, "y": 1}}})  
```

Next, we define the STL expression we would like to evaluate
```python
stl_spec = STL("G[0, 1](x > y)")
```
There are often two parameters that we can obtain from the evaluation of STL expressions, namely, the satisfaction value,
in `bool` type (True/False), and the robustness value and the robustness value, in `float` type. There are two ways
of accessing these values:

The first approach is a fairly straightforward one:
```python
satisfy    : bool  = stl_spec.satisfy(time_begin, signal)     # obtain the satisfaction value
robustness : float = stl_spec.robustness(time_begin, signal)  # obtain the robustness value
```

The second approach is a bit less straightforward, but it allows the evaluation results to be cached for future access
within an object called `Eval_Result`
```python
stl_eval: Eval_Result = stl_spec.eval(time_begin, signal)

satisfy    : bool  = stl_eval.satisfy
robustness : float = stl_eval.robustness
```
### 

### Usage (REPL)
We can simply the usage procedure above into a simply REPL interface. Users can start the REPL by typing `stlinterp` on
the command line

```bash
$ stlinterp
Time Start: 0
Signal:
{
    "0": {
        "content": {
            "x": 1,
            "y": 2
        }
    },
    "1": {
        "content": {
            "x": 2,
            "y": 1
        }
    }
}
Please enter STL expressions to be interpreted.
>>>
```

Once the REPL is started, it will prompt you to enter the STL expression. Users can simply type the expression
`G[0, 1](x > y)` after the `>>> `, click `Enter` to evaluate the expression.
```bash
>>> G[0, 1](x > y)
satisfy     : False
robustness  : -1.0
```


## Project Structure
- API-level interfaces (high-level)
    - They are designed to be simple to use with minimal overhead for training and learning.
    - API-level interfaces include `stl.obj` as well as programs in `stl.api`.
- Low-level interfaces
    - Low-level interfaces are designed to support lower-level operations like lexing and parsing
      of the strings passed in from the API level. It is not intended to interact with the user directly.
    - It includes all modules in `stl.parsing`

## File Structure
`bin/`: consists of bash scripts. must be added to system `PATH` variable to be executed on the command line.
  - `stllex`: start the REPL for the lexical analyzer
  - `stlparse`: start the REPL for the parser
  - `stlinterp`: start the REPL for the interpreter
  - `stltest`: initiate unit test
  - `stlsize`: show the size of the codebase

`code-style/`: consists of code-writing guidelines excerpted from Google for code consistency purposes (for developers of the repository)

`example/` -> `stl/example/`: demonstrate example usage of the internal helper functions, low-level structures (lexer and parser level) as well as high-level objects (api level)

`stl/`: main code repository
  - `api.py`: main entry point for importing high-level (api level) objects and functions
  - `tool.py`: foundational tools for code repository
  - `unit_test.py`: handle unit testing of objects and tools, can be invoked using `stltest` command on the command line
  - `obj/`: imported by `api.py`, intended to be used by the users of the API. consists of API level objects
  - `parsing/`: not intended to be used directly by the user. low-level (parser and lexer level objects, i.e. AST (abstract syntax tree), type signatures)
  - `error.py`: main entry point for importing errors
  - `err/`: all definition/implementation of errors
## Special Notes
- example folder is in stl folder for unit-test purpose, a symbolic link for example folder is created in the 
  project root directory

## Common Issues
- Vscode PyLint "Unable to Import" Error
  - See [Stackoverflow](https://stackoverflow.com/questions/1899436/pylint-unable-to-import-error-how-to-set-pythonpath)
  - create `~/.pylintrc` with the following content
    ```bash
    [MASTER]
    init-hook='import sys; sys.path.append("/path/to/STL-API")'
    ```
    Note that please replace `/path/to/STL-API` with the actual __absolute path__ to the location of the respository
    
## Future Features
- syntax for absolute value
  - `G[0, 1](|y| > 1)` means that the absolute value of y must be greater than 1 between time 0 and 1 of the signal
  
- support for nested STL expression
  - `F G[0, 10](y > 1)` means that between time 0 and time 10, the y parameter of the signal will eventually always be greater than 1
  
- allow passing in external function/objects to evaluation
  ```python
  class Coord:
    def __init__(self, x, y):
        ...
  
  def distance_between_points(p1, p2) -> float:
      ...
      return result
    
  stl_spec = STL("G[0, 1](distance_between_points(Coord(a, b), Coord(c, d)) > 3)")
  stl_spec.add_extern_func(distance_between)
  stl_spec.add_extern_obj(Coord)
  
  stl_spec.eval(...)
  ```

- improved the signal so that it can handle more continuous times
  - signal = Signal(py_dict={"0": {"content": {"timestamp": 0.1, "x": 1}}, "1": {"content": {"timestamp": 0.2, "x": 2}}})
  - when the signal has "timestamp" as a quantifiable key, the STL expressions will evaluate based upon the timestamp instead of the timeindex
  - backward compatibility