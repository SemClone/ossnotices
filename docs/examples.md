# OSS Notices Generator - Examples

## Table of Contents
- [Basic Examples](#basic-examples)
- [Real-World Scenarios](#real-world-scenarios)
- [Integration Examples](#integration-examples)
- [Advanced Workflows](#advanced-workflows)

## Basic Examples

### Example 1: Simple Project Scan

Scanning a Python project and generating notices:

```bash
# Navigate to your project
cd ~/my-python-project

# Generate notices (creates NOTICE.txt)
ossnotices

# View the generated file
cat NOTICE.txt
```

### Example 2: Scanning with Custom Output

```bash
# Generate notices in a specific location
ossnotices ./src -o legal/THIRD-PARTY-NOTICES.txt

# Generate HTML for documentation
ossnotices ./src -f html -o docs/licenses.html
```

### Example 3: Processing Java Archives

```bash
# Process a single JAR file
ossnotices application.jar -o NOTICE.txt

# Process multiple archives
for jar in lib/*.jar; do
    ossnotices "$jar" -o "notices/$(basename $jar .jar)-NOTICE.txt"
done
```

## Real-World Scenarios

### Scenario 1: Multi-Language Project

For a project with Python, JavaScript, and Java components:

```bash
#!/bin/bash

# Create combined notices
echo "Generating notices for multi-language project..."

# Python components
ossnotices ./python-src --recursive -f json -o python-notices.json

# JavaScript components
ossnotices ./node_modules --recursive -f json -o js-notices.json

# Java components
ossnotices ./lib --recursive -f json -o java-notices.json

# Combine all notices (requires jq)
jq -s '.[0].packages + .[1].packages + .[2].packages' \
    python-notices.json js-notices.json java-notices.json | \
    jq '{packages: .}' > combined-notices.json

# Convert to final text format
ossnotices --from-json combined-notices.json -f text -o NOTICE.txt
```

### Scenario 2: Docker Container Compliance

Creating notices for a Docker container:

```dockerfile
# Dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Generate notices during build
RUN pip install ossnotices && \
    ossnotices /usr/local/lib/python3.9/site-packages -o /app/NOTICE.txt

COPY . .

# Include notices in final image
COPY NOTICE.txt /app/legal/
```

### Scenario 3: Monorepo with Multiple Services

```bash
#!/bin/bash

# Process each service in a monorepo
SERVICES="auth-service api-service web-frontend"

for service in $SERVICES; do
    echo "Processing $service..."

    # Generate service-specific notices
    ossnotices "./services/$service" \
        --recursive \
        -o "./services/$service/NOTICE.txt"

    # Also create HTML version for documentation
    ossnotices "./services/$service" \
        --recursive \
        -f html \
        -o "./docs/licenses/$service.html"
done

# Create master notice file
cat ./services/*/NOTICE.txt > ./NOTICE-COMBINED.txt
```

## Integration Examples

### GitHub Actions Workflow

```yaml
name: Generate OSS Notices

on:
  push:
    paths:
      - 'requirements.txt'
      - 'package.json'
      - 'pom.xml'

jobs:
  generate-notices:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install ossnotices
      run: pip install ossnotices

    - name: Generate notices
      run: |
        ossnotices . --recursive -o NOTICE.txt
        ossnotices . --recursive -f html -o docs/licenses.html

    - name: Commit notices
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add NOTICE.txt docs/licenses.html
        git diff --staged --quiet || git commit -m "Update OSS notices"

    - name: Push changes
      uses: ad-m/github-push-action@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
```

### Pre-commit Hook

`.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Generate notices before each commit
echo "Updating OSS notices..."

# Check if dependencies changed
if git diff --cached --name-only | grep -E "(requirements\.txt|package\.json|pom\.xml)"; then
    ossnotices . --recursive -q -o NOTICE.txt
    git add NOTICE.txt
    echo "NOTICE.txt updated"
fi
```

### Makefile Integration

```makefile
# Makefile
.PHONY: notices notices-html notices-json clean-notices

# Generate all notice formats
notices: notices-text notices-html notices-json

notices-text:
	@echo "Generating text notices..."
	@ossnotices . --recursive -o NOTICE.txt

notices-html:
	@echo "Generating HTML notices..."
	@ossnotices . --recursive -f html -o docs/licenses.html

notices-json:
	@echo "Generating JSON notices..."
	@ossnotices . --recursive -f json -o notices.json

clean-notices:
	@rm -f NOTICE.txt docs/licenses.html notices.json

# Include in build process
build: clean test notices
	@echo "Building application..."
	# Build commands here
```

## Advanced Workflows

### Custom Python Script

```python
#!/usr/bin/env python3
"""
generate_notices.py - Advanced notice generation with filtering
"""

import os
import json
from ossnotices import NoticesGenerator

def main():
    generator = NoticesGenerator()

    # Scan multiple directories
    directories = ['src', 'lib', 'vendor']
    all_packages = []

    for directory in directories:
        if os.path.exists(directory):
            packages = generator.scan_directory(directory, recursive=True)
            all_packages.extend(packages)

    # Filter out certain licenses
    excluded_licenses = ['Public Domain', 'Unlicense']
    filtered_packages = [
        p for p in all_packages
        if p.license not in excluded_licenses
    ]

    # Group by license type
    by_license = {}
    for package in filtered_packages:
        if package.license not in by_license:
            by_license[package.license] = []
        by_license[package.license].append(package)

    # Generate grouped notices
    output = []
    for license_type, packages in sorted(by_license.items()):
        output.append(f"\n{'='*60}")
        output.append(f"LICENSE TYPE: {license_type}")
        output.append(f"PACKAGES: {len(packages)}")
        output.append('='*60)

        for package in sorted(packages, key=lambda p: p.name):
            output.append(f"\n{package.name} ({package.version})")
            output.append(package.notice_text)

    # Save custom formatted notices
    with open('NOTICE-GROUPED.txt', 'w') as f:
        f.write('\n'.join(output))

    print(f"Generated grouped notices for {len(filtered_packages)} packages")
    print(f"License types found: {', '.join(by_license.keys())}")

if __name__ == '__main__':
    main()
```

### Validation Script

```bash
#!/bin/bash
# validate_notices.sh - Ensure all dependencies have notices

echo "Validating OSS notices..."

# Generate fresh notices
ossnotices . --recursive -f json -o temp_notices.json

# Extract package count
PACKAGE_COUNT=$(jq '.metadata.total_packages' temp_notices.json)

# Count actual dependencies (example for Python)
PIP_COUNT=$(pip list --format=json | jq '. | length')

# Compare counts
if [ "$PACKAGE_COUNT" -lt "$PIP_COUNT" ]; then
    echo "WARNING: Not all packages have notices!"
    echo "  Packages with notices: $PACKAGE_COUNT"
    echo "  Total dependencies: $PIP_COUNT"
    exit 1
else
    echo "✓ All packages have notices"
fi

# Check for high-risk licenses
HIGH_RISK_LICENSES="GPL-3.0 AGPL-3.0"

for license in $HIGH_RISK_LICENSES; do
    if grep -q "$license" temp_notices.json; then
        echo "WARNING: Found high-risk license: $license"
        jq ".packages[] | select(.license == \"$license\") | .name" temp_notices.json
    fi
done

rm temp_notices.json
echo "Validation complete"
```

### Release Automation

```bash
#!/bin/bash
# prepare_release.sh - Prepare notices for release

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: ./prepare_release.sh <version>"
    exit 1
fi

echo "Preparing release $VERSION..."

# Create release directory
mkdir -p "releases/$VERSION"

# Generate notices in multiple formats
ossnotices . --recursive -o "releases/$VERSION/NOTICE.txt"
ossnotices . --recursive -f html -o "releases/$VERSION/licenses.html"
ossnotices . --recursive -f json -o "releases/$VERSION/licenses.json"

# Create tarball with notices
tar czf "releases/$VERSION/licenses.tar.gz" \
    -C "releases/$VERSION" \
    NOTICE.txt licenses.html licenses.json

echo "Release notices prepared in releases/$VERSION/"
```

## SEMCL.ONE Ecosystem Integration

### Combining with Other Tools

```bash
#!/bin/bash
# Full SEMCL.ONE compliance workflow

# 1. Identify packages from source
src2purl ./src > packages.txt

# 2. Generate notices for identified packages
purl2notices -i packages.txt -o detailed-notices.txt

# 3. Simplified notices with ossnotices
ossnotices . --recursive -o simple-notices.txt

# 4. License detection with osslili
osslili ./src -o license-report.json

# 5. Extract metadata with upmex
for pkg in *.whl; do
    upmex extract "$pkg" >> metadata.json
done

echo "Complete compliance documentation generated"
```

## See Also

- [User Guide](user-guide.md) - Complete usage documentation
- [API Reference](api.md) - Python API documentation
- [purl2notices Examples](https://github.com/SemClone/purl2notices/docs/examples.md)