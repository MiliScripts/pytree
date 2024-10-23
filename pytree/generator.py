
import os
from pathlib import Path

def parse_tree(tree_content):
    """Parse the tree-like structure from the content."""
    structure = {}
    current_path = []
    prev_indent = 0
    
    for line in tree_content.split('\n'):
        if not line.strip():
            continue
            
        # Count leading spaces/symbols to determine depth
        indent = len(line) - len(line.lstrip('│ ├──└──'))
        clean_name = line.strip('│ ├──└──').strip()
        
        # Adjust current path based on indent
        if indent < prev_indent:
            current_path = current_path[:indent//2]
        elif indent == prev_indent:
            if current_path:
                current_path.pop()
                
        current_path.append(clean_name)
        
        # Add to structure
        temp = structure
        for part in current_path[:-1]:
            if part not in temp:
                temp[part] = {}
            temp = temp[part]
        temp[current_path[-1]] = {}
        
        prev_indent = indent
    
    return structure

def create_structure(base_path, structure):
    """Create the directory structure."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if not content:  # It's a file
            Path(path).touch()
        else:  # It's a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)

def generate_structure(tree_file, output_dir="."):
    """Main function to generate directory structure from tree file."""
    with open(tree_file, 'r') as f:
        content = f.read()
    
    structure = parse_tree(content)
    create_structure(output_dir, structure)
