#!/usr/bin/env python
"""Re-indent a Python source file to use consistent 4-space indentation."""

import sys

def reindent_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    
    # Track the expected indent level
    indent_stack = [0]
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Preserve empty lines
        if not stripped:
            result.append('')
            i += 1
            continue
        
        # Count current indentation
        current_indent = len(line) - len(line.lstrip())
        
        # Determine the correct indent level
        # Should be a multiple of 4 (one tab = 4 spaces typically)
        # Convert tabs to spaces first
        line_with_spaces = line.expandtabs(4)
        correct_indent = len(line_with_spaces) - len(line_with_spaces.lstrip())
        
        # Round to nearest multiple of 4
        if correct_indent % 4 != 0:
            # Find nearest multiple of 4
            lower = (correct_indent // 4) * 4
            upper = lower + 4
            if abs(correct_indent - lower) <= abs(correct_indent - upper):
                correct_indent = lower
            else:
                correct_indent = upper
        
        # Re-indent the line
        result.append(' ' * correct_indent + stripped)
        i += 1
    
    # Write back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    
    print(f"Re-indented {filename}")

if __name__ == '__main__':
    reindent_file('app.py')
