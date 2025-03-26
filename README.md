# pytools-litho-design

Pytools litho design is an extension for `gdsfactory` that provides a set of usefull designs. Some `gdsactory` examples edited to work without klayout can be found in the `gds_examples` folder, examples of the code that this repository provides can be found in the `examples` folder.

## Installation

The project can be used in 2 ways:

- Standalone: You can clone the repository and run the scripts directly from the repository.
- As a package: You can install the package using pip (not cloning the repository).

### Standalone

1. Clone the repository:

    ```bash
    git clone https://github.com/Nynra/pytools-litho-design.git
    # Or if you need a specific version (x.x.x is the version number)
    # git clone https://github.com/Nynra/pytools-litho-design.git@x.x.x
    ```

2. Create a virtual environment and install the package as editable:

    ```bash
    cd pytools-litho-design
    python3 -m venv venv

    # For linux
    source venv/bin/activate

    # For windows
    #venv\Scripts\activate

    pip install --editable .
    ```

### As a package

The following command will install the package globally in your python environment:

```bash
pip install pytools_litho_design @ https://github.com/Nynra/pytools-litho-design.git
# Or if you need a specific version (x.x.x is the version number)
pip install pytools_litho_design @ https://github.com/Nynra/pytools-litho-design.git@x.x.x
```
