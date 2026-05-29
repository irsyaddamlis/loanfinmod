import os

# 1. Get the version from pyproject.toml
with open('pyproject.toml', 'r') as f:
    for line in f:
        if line.startswith("version ="):
            version = line.split('"')[1] # Extracts the version number
            break

# 2. Update README.md
with open('README.md', 'r') as f:
    content = f.read()

# Replace the old version line with the new one
new_content = content.replace("Make sure the version is **1.0.4**.", f"Make sure the version is **{version}**.")

with open('README.md', 'w') as f:
    f.write(new_content)

print(f"Updated README to version {version}")