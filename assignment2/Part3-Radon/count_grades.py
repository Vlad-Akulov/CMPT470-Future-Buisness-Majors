#!/usr/bin/env python3
"""
Script to count and output the number of each letter grade from radon analysis files.
"""

import re
from collections import defaultdict
from pathlib import Path

def count_grades_from_radon_mi(filepath):
    """
    Count letter grades from radon maintainability index file.
    
    Args:
        filepath: Path to the radon_mi.txt file
    
    Returns:
        Dictionary with grade counts
    """
    grades = defaultdict(int)
    
    with open(filepath, 'r') as f:
        for line in f:
            # Pattern: filename - GRADE (score)
            match = re.search(r' - ([A-F]) \(', line.strip())
            if match:
                grade = match.group(1)
                grades[grade] += 1
    
    return grades

def count_grades_from_radon_cc(filepath):
    """
    Count letter grades from radon cyclomatic complexity file.
    
    Args:
        filepath: Path to the radon_cc.txt file
    
    Returns:
        Dictionary with per-file grade counts
    """
    file_grades = {}
    current_file = None
    
    with open(filepath, 'r') as f:
        for line in f:
            # Check if this is a file header (no leading whitespace and ends with .py)
            if line.startswith('httpx') and line.strip().endswith('.py'):
                current_file = line.strip()
                file_grades[current_file] = defaultdict(int)
            # Pattern: Grade appears in lines like "    F 39:0 request - A (1)"
            elif current_file:
                match = re.search(r' - ([A-F]) \(\d+\)$', line.strip())
                if match:
                    grade = match.group(1)
                    file_grades[current_file][grade] += 1
    
    return file_grades

def print_grade_summary(title, data):
    """
    Print a summary of grades in a formatted way.
    
    Args:
        title: Title for the summary
        data: Either a dict of grade counts or dict of per-file grade counts
    """
    print(f"\n{title}")
    print("=" * 60)
    
    # Check if this is per-file data (dict of dicts) or overall data (dict of ints)
    if data and isinstance(next(iter(data.values())), dict):
        # Per-file data
        for filename in sorted(data.keys()):
            grades = data[filename]
            print(f"\n  {filename}")
            for grade in sorted(grades.keys()):
                count = grades[grade]
                print(f"    Grade {grade}: {count}")
            total = sum(grades.values())
            non_a_count = total - grades.get('A', 0)
            print(f"    Total: {total} | Non-A grades: {non_a_count}")
    else:
        # Overall data
        for grade in sorted(data.keys()):
            count = data[grade]
            print(f"  Grade {grade}: {count} occurrence(s)")
        total = sum(data.values())
        print(f"  Total: {total}")

def main():
    """Main function to analyze radon output files."""
    script_dir = Path(__file__).parent
    
    # Analyze Maintainability Index
    mi_file = script_dir / 'radon_mi.txt'
    if mi_file.exists():
        mi_grades = count_grades_from_radon_mi(mi_file)
        print_grade_summary("Radon Maintainability Index (MI) - Grade Distribution", mi_grades)
    else:
        print(f"Warning: {mi_file} not found")
    
    # Analyze Cyclomatic Complexity per file
    cc_file = script_dir / 'radon_cc.txt'
    if cc_file.exists():
        cc_grades = count_grades_from_radon_cc(cc_file)
        print_grade_summary("Radon Cyclomatic Complexity (CC) - Grade Distribution by File", cc_grades)
    else:
        print(f"Warning: {cc_file} not found")

if __name__ == '__main__':
    main()
