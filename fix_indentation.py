import ast
import sys

def fix_indentation(filename):
    """Fix indentation errors in Python file"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines and comments
        if line.strip() == '' or line.strip().startswith('#'):
            fixed_lines.append(line)
            i += 1
            continue
        
        # Count leading spaces
        stripped = line.lstrip()
        leading_spaces = len(line) - len(stripped)
        
        # Check if this line has excessive indentation
        # Common pattern: lines that should be at same level but have extra spaces
        if leading_spaces > 0 and leading_spaces % 4 != 0:
            # Try to deduce correct indentation
            # Look at previous non-empty line
            prev_indent = 0
            for j in range(i-1, -1, -1):
                prev_stripped = lines[j].strip()
                if prev_stripped:
                    prev_indent = len(lines[j]) - len(lines[j].lstrip())
                    break
            
            # Look at next non-empty line
            next_indent = 0
            for j in range(i+1, len(lines)):
                next_stripped = lines[j].strip()
                if next_stripped:
                    next_indent = len(lines[j]) - len(lines[j].lstrip())
                    break
            
            # Use the most common indentation
            if prev_indent == next_indent:
                correct_indent = prev_indent
            elif abs(leading_spaces - prev_indent) < abs(leading_spaces - next_indent):
                correct_indent = prev_indent
            else:
                correct_indent = next_indent
            
            # Fix the indentation
            fixed_line = ' ' * correct_indent + stripped
            fixed_lines.append(fixed_line)
            print(f"Fixed line {i+1}: {leading_spaces} -> {correct_indent} spaces")
        else:
            fixed_lines.append(line)
        
        i += 1
    
    # Write back
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"\nFixed {filename}")
    return fixed_lines

if __name__ == '__main__':
    fix_indentation('app.py')
