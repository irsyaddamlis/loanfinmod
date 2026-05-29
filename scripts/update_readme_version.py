import os
import re

# Get project root
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
toml_path = os.path.join(root_dir, 'pyproject.toml')
readme_path = os.path.join(root_dir, 'README.md')

# 1. Extract version from pyproject.toml
with open(toml_path, 'r') as f:
    content = f.read()
    # Matches version = "X.X.X"
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    version = match.group(1) if match else "0.0.0"

# 2. Update README.md
with open(readme_path, 'r') as f:
    readme_content = f.read()

# NEW PATTERN: Matches "Make sure the version is **AnyNumber**."
# [0-9\.]+ allows for 1.0.0, 1.0.1, etc.
pattern = r'Make sure the version is \*\*[0-9\.]+\*\*.'
replacement = f'Make sure the version is **{version}**.'

new_content = re.sub(pattern, replacement, readme_content)

with open(readme_path, 'w') as f:
    f.write(new_content)

print(f"Successfully updated README to version {version}")