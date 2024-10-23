import argparse
import sys
from .generator import generate_structure

def main():
    parser = argparse.ArgumentParser(description="Generate directory structure from tree file")
    parser.add_argument('tree_file', help='Path to the tree.txt file')
    parser.add_argument('--output', '-o', default=".", help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    try:
        generate_structure(args.tree_file, args.output)
        print(f"Successfully generated directory structure in {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
