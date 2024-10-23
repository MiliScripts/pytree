import os
from pathlib import Path

def parse_tree(tree_content):
    """Parse the tree-like structure from the content."""
    structure = {}
    current_path = []
    current_indent = 0
    
    lines = [line for line in tree_content.split('\n') if line.strip()]
    
    for line in lines:
        # Calculate indent level
        indent = 0
        for char in line:
            if char in ['│', ' ']:
                indent += 1
            else:
                break
        indent = indent // 2  # Normalize indent level
        
        # Clean the name (remove tree characters)
        name = line.strip().replace('│', '').replace('├──', '').replace('└──', '').replace('─', '').strip()
        
        # Adjust the current path based on indent
        if indent > current_indent:
            current_path.append(current_path[-1])
        elif indent < current_indent:
            current_path = current_path[:indent+1]
        else:
            current_path = current_path[:-1]
        current_path.append(name)
        current_indent = indent
        
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
            if content:  # If there are subdirectories/files
                create_structure(path, content)

def generate_structure(tree_file, output_dir="."):
    """Main function to generate directory structure from tree file."""
    try:
        with open(tree_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        structure = parse_tree(content)
        create_structure(output_dir, structure)
        print(f"Successfully created directory structure in {output_dir}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

def debug_structure(structure, level=0):
    """Helper function to debug the parsed structure."""
    for name, content in structure.items():
        print("  " * level + name)
        if content:
            debug_structure(content, level + 1)
