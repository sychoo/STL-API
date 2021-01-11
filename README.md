# STL API
## Motivation
STL API is used to evaluate STL specification with respect to
an arbitrary signal.

## Project Structure
- API-level interfaces (high-level)
    - They are designed to be simple to use with minimal overhead for training and learning.
    - API-level interfaces include stl.obj as well as programs in stl.api.
- Low-level interfaces
    - Low-level interfaces are designed to support lower-level operations like lexing and parsing
      of the strings passed in from the API level. It is not intended to interact with the user directly.
    - It includes all modules in stl.parsing

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

  Then, execute the following command on the command line (for .zshrc)

  ```bash
  source ~/.zshrc
  ```
  

### Configure STL PATH (for unit testing and other repository referential operations)
```bash
export STLPATH="/path/to/STL-API/"
```

### required Platform
- Python3.9+

### required Python packages
- rply (for parser and lexer)
- termcolor (for color printing tools)

## Usage

## File Structure

## Special Notes
- example folder is in stl folder for unit-test purpose, a symbolic link for example folder is created in the 
  project root directory
