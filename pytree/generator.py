import os
from pathlib import Path
import shutil

def parse_line_depth(line):
    """Calculate the depth of a line based on tree characters."""
    depth = 0
    for char in line:
        if char in ['│', '├', '└', ' ']:
            depth += 1
        else:
            break
    return depth // 4  # Adjust this based on your indentation style

def clean_name(line):
    """Clean the name from tree characters."""
    return line.strip().replace('│', '').replace('├──', '').replace('└──', '').replace('─', '').strip()

def parse_tree(tree_content):
    """Parse the tree-like structure from the content."""
    lines = [line.rstrip() for line in tree_content.split('\n') if line.strip()]
    structure = {}
    
    # Get root directory name
    root_name = clean_name(lines[0])
    current = structure[root_name] = {}
    path_stack = [root_name]
    depth_stack = [0]
    
    # Process remaining lines
    for line in lines[1:]:
        depth = parse_line_depth(line)
        name = clean_name(line)
        
        # Safeguard: Ensure there is something to pop
        while depth_stack and depth <= depth_stack[-1]:
            depth_stack.pop()
            path_stack.pop()
            
        # Add the current name to the stack
        path_stack.append(name)
        depth_stack.append(depth)
        
        # Navigate to current position in structure
        current = structure[root_name]
        for path_item in path_stack[1:-1]:
            if path_item not in current:
                current[path_item] = {}
            current = current[path_item]
        current[name] = {}
    
    return structure

def create_structure(base_path, structure):
    """Create the directory structure."""
    # First, clean up any existing structure
    for name in structure:
        full_path = os.path.join(base_path, name)
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
    
    # Create the new structure
    for root_name, contents in structure.items():
        root_path = os.path.join(base_path, root_name)
        os.makedirs(root_path, exist_ok=True)
        
        def create_recursively(current_path, current_structure):
            for name, substructure in current_structure.items():
                path = os.path.join(current_path, name)
                
                if name.endswith(('.py', '.txt', '.html', '.md')):
                    # Create parent directories if needed
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    # Create the file
                    Path(path).touch()
                else:
                    # Create directory
                    os.makedirs(path, exist_ok=True)
                    # Recursively create the substructure
                    create_recursively(path, substructure)
        
        create_recursively(root_path, contents)

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
