# PyTree

PyTree is a Python package that generates directory structures from tree-like text files. It's perfect for quickly setting up project scaffolding or recreating directory structures.

## Installation

```bash
pip install git+https://github.com/MiliScripts/pytree.git
```

## Usage

1. Create a text file (e.g., `tree.txt`) with your desired structure using tree-like syntax:

```
project/
├── web/
│   ├── app.py
│   ├── models.py
│   └── templates/
│       └── index.html
└── README.md
```

2. Run the command:

```bash
pytree tree.txt
```

Or from Python:

```python
from pytree import generate_structure

generate_structure("tree.txt", "output_directory")
```

## Features

- Supports nested directory structures
- Handles both files and directories
- Preserves directory hierarchy
- Simple and intuitive syntax
- Command-line interface
- Python API

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
