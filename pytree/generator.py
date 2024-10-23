import os
from pathlib import Path

def parse_line_depth(line):
    """Calculate the depth of a line based on tree characters."""
    depth = 0
    for char in line:
        if char in ['│', ' ']:
            depth += 1
        else:
            break
    return depth // 4  # Normalize by dividing by 4 (standard tree indentation)

def clean_name(line):
    """Clean the name from tree characters."""
    return line.strip().replace('│', '').replace('├──', '').replace('└──', '').replace('─', '').strip()

def parse_tree(tree_content):
    """Parse the tree-like structure from the content."""
    lines = [line.rstrip() for line in tree_content.split('\n') if line.strip()]
    root = {}
    path_stack = []
    depth_stack = [-1]
    
    for line in lines:
        depth = parse_line_depth(line)
        name = clean_name(line)
        
        # Pop from stacks until we find the parent depth
        while depth <= depth_stack[-1]:
            depth_stack.pop()
            path_stack.pop()
            
        # Add current item to stacks
        depth_stack.append(depth)
        path_stack.append(name)
        
        # Build the structure
        current = root
        for path_item in path_stack[:-1]:
            if path_item not in current:
                current[path_item] = {}
            current = current[path_item]
        current[path_stack[-1]] = {}
    
    return root

def create_structure(base_path, structure):
    """Create the directory structure."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if name.endswith(('.py', '.txt', '.html', '.md')):  # It's a file
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # Create empty file
            Path(path).touch()
        else:  # It's a directory
            # Create directory
            os.makedirs(path, exist_ok=True)
            # Recursively create contents
            create_structure(path, content)

def generate_structure(tree_file, output_dir="."):
    """Main function to generate directory structure from tree file."""
    try:
        # Read the tree file
        with open(tree_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse and create structure
        structure = parse_tree(content)
        create_structure(output_dir, structure)
        
        print(f"Successfully created directory structure in {output_dir}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

def print_structure(structure, level=0):
    """Debug function to print the parsed structure."""
    for name, content in structure.items():
        print("  " * level + name)
        if content:
            print_structure(content, level + 1)
