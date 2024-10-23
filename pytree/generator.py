import os
from pathlib import Path

def parse_tree(tree_content):
    """Parse the tree-like structure from the content."""
    structure = {}
    current_path = []
    
    lines = [line for line in tree_content.split('\n') if line.strip()]
    
    for line in lines:
        # Count the depth based on the position of the last '|' or '└' or '├'
        depth = 0
        for i, char in enumerate(line):
            if char in ['│', '└', '├', '─']:
                depth = i // 4  # Assuming 4 spaces per level
        
        # Clean the name (remove tree characters)
        name = line.strip().replace('│', '').replace('├──', '').replace('└──', '').replace('─', '').strip()
        
        # Adjust the current path based on depth
        current_path = current_path[:depth]
        current_path.append(name)
        
        # Build the structure
        temp = structure
        for i, part in enumerate(current_path[:-1]):
            if part not in temp:
                temp[part] = {}
            temp = temp[part]
        
        # Add the final item
        if current_path[-1]:  # Only add if name is not empty
            temp[current_path[-1]] = {}
    
    return structure

def create_structure(base_path, structure):
    """Create the directory structure."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if name.endswith(('.py', '.txt', '.html', '.md')):  # It's a file
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # Create the file
            Path(path).touch()
        else:  # It's a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)

def generate_structure(tree_file, output_dir="."):
    """Main function to generate directory structure from tree file."""
    with open(tree_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    structure = parse_tree(content)
    create_structure(output_dir, structure)
