"""
Clean special characters from all CSV files in complete_output
"""
import pandas as pd
import os
import re

OUTPUT_DIR = 'complete_output'

# Characters to remove/replace
SPECIAL_CHARS_PATTERN = r'[^\x00-\x7F]'  # Non-ASCII characters
PROBLEMATIC_CHARS = ['→', '–', '—', '"', '"', ''', ''', '…', '•', '°', '±', '×', '÷', '©', '®', '™']

def clean_string(value):
    """Clean a string value of special characters"""
    if pd.isna(value):
        return value
    if not isinstance(value, str):
        return value
    
    # Replace specific problematic characters
    replacements = {
        '→': '->',
        '–': '-',
        '—': '-',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '…': '...',
        '•': '-',
        '°': ' deg',
        '±': '+/-',
        '×': 'x',
        '÷': '/',
        '©': '(c)',
        '®': '(R)',
        '™': '(TM)',
        '\n': ' ',
        '\r': ' ',
        '\t': ' '
    }
    
    for char, replacement in replacements.items():
        value = value.replace(char, replacement)
    
    # Remove any remaining non-ASCII characters
    value = re.sub(SPECIAL_CHARS_PATTERN, '', value)
    
    # Clean up multiple spaces
    value = re.sub(r'\s+', ' ', value).strip()
    
    return value

def find_special_characters(df, filename):
    """Find all special characters in a dataframe"""
    issues = []
    
    for col in df.columns:
        if df[col].dtype == 'object':  # String columns
            for idx, value in df[col].items():
                if pd.notna(value) and isinstance(value, str):
                    # Find non-ASCII characters
                    special = re.findall(SPECIAL_CHARS_PATTERN, value)
                    if special:
                        issues.append({
                            'file': filename,
                            'column': col,
                            'row': idx,
                            'value': value[:50],
                            'special_chars': list(set(special))
                        })
    
    return issues

def clean_dataframe(df):
    """Clean all string columns in a dataframe"""
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(clean_string)
    return df

def main():
    print("="*80)
    print("SPECIAL CHARACTER DETECTION AND CLEANING")
    print("="*80)
    
    all_issues = []
    files_cleaned = 0
    
    # First pass: Find all special characters
    print("\n1. SCANNING FOR SPECIAL CHARACTERS...")
    print("-"*60)
    
    for filename in sorted(os.listdir(OUTPUT_DIR)):
        if not filename.endswith('.csv'):
            continue
        
        filepath = f'{OUTPUT_DIR}/{filename}'
        df = pd.read_csv(filepath)
        
        issues = find_special_characters(df, filename)
        if issues:
            print(f"\n  ⚠️ {filename}: Found {len(issues)} cells with special characters")
            for issue in issues[:3]:  # Show first 3
                print(f"     Column: {issue['column']}, Chars: {issue['special_chars']}")
                print(f"     Value: {issue['value'][:40]}...")
            if len(issues) > 3:
                print(f"     ... and {len(issues) - 3} more")
            all_issues.extend(issues)
        else:
            print(f"  ✅ {filename}: Clean")
    
    if not all_issues:
        print("\n✅ No special characters found in any file!")
        return
    
    print(f"\n\nTotal issues found: {len(all_issues)}")
    
    # Second pass: Clean all files
    print("\n2. CLEANING ALL FILES...")
    print("-"*60)
    
    for filename in sorted(os.listdir(OUTPUT_DIR)):
        if not filename.endswith('.csv'):
            continue
        
        filepath = f'{OUTPUT_DIR}/{filename}'
        df = pd.read_csv(filepath)
        
        # Clean the dataframe
        df_cleaned = clean_dataframe(df)
        
        # Save back
        df_cleaned.to_csv(filepath, index=False)
        files_cleaned += 1
        print(f"  ✅ Cleaned: {filename}")
    
    # Third pass: Verify cleaning
    print("\n3. VERIFYING CLEANING...")
    print("-"*60)
    
    remaining_issues = []
    for filename in sorted(os.listdir(OUTPUT_DIR)):
        if not filename.endswith('.csv'):
            continue
        
        filepath = f'{OUTPUT_DIR}/{filename}'
        df = pd.read_csv(filepath)
        
        issues = find_special_characters(df, filename)
        if issues:
            print(f"  ❌ {filename}: Still has {len(issues)} issues")
            remaining_issues.extend(issues)
        else:
            print(f"  ✅ {filename}: Clean")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"  Files processed: {files_cleaned}")
    print(f"  Issues found: {len(all_issues)}")
    print(f"  Issues remaining: {len(remaining_issues)}")
    
    if remaining_issues:
        print("\n  ⚠️ Some issues could not be cleaned automatically")
    else:
        print("\n  🎉 All special characters cleaned successfully!")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.')
    main()
