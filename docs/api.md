# OSS Notices Generator - API Reference

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Core Classes](#core-classes)
- [Functions](#functions)
- [Data Types](#data-types)
- [Examples](#examples)

## Overview

The ossnotices Python API provides programmatic access to notice generation functionality. While ossnotices is primarily a CLI tool, it can be imported and used as a library in Python applications.

## Installation

```python
pip install ossnotices
```

## Core Classes

### NoticesGenerator

The main class for generating OSS notices programmatically.

```python
from ossnotices import NoticesGenerator

generator = NoticesGenerator()
```

#### Methods

##### `scan_directory(path, recursive=False)`

Scans a directory for package dependencies.

**Parameters:**
- `path` (str): Directory path to scan
- `recursive` (bool): Whether to scan subdirectories recursively

**Returns:**
- `List[Package]`: List of discovered packages

**Example:**
```python
packages = generator.scan_directory("./src", recursive=True)
```

##### `scan_archive(file_path)`

Processes an archive file for package information.

**Parameters:**
- `file_path` (str): Path to archive file (JAR, WAR, WHL, ZIP, etc.)

**Returns:**
- `List[Package]`: List of packages found in archive

**Example:**
```python
packages = generator.scan_archive("library.jar")
```

##### `generate_notices(packages, format='text')`

Generates notice content from a list of packages.

**Parameters:**
- `packages` (List[Package]): List of packages
- `format` (str): Output format ('text', 'html', 'json')

**Returns:**
- `str`: Generated notices content

**Example:**
```python
notices = generator.generate_notices(packages, format='html')
```

##### `save_notices(content, output_path)`

Saves notice content to a file.

**Parameters:**
- `content` (str): Notice content to save
- `output_path` (str): File path for output

**Example:**
```python
generator.save_notices(notices, "NOTICE.txt")
```

## Functions

### `scan_and_generate(path, **options)`

Convenience function for scanning and generating notices in one call.

**Parameters:**
- `path` (str): Path to scan (directory or archive)
- `**options`: Additional options
  - `recursive` (bool): Recursive scanning for directories
  - `format` (str): Output format ('text', 'html', 'json')
  - `output` (str): Output file path
  - `cache` (bool): Enable caching (default: True)

**Returns:**
- `str`: Generated notices content

**Example:**
```python
from ossnotices import scan_and_generate

notices = scan_and_generate(
    "./project",
    recursive=True,
    format='json',
    output='notices.json'
)
```

## Data Types

### Package

Represents a discovered package.

**Attributes:**
- `name` (str): Package name
- `version` (str): Package version
- `license` (str): License identifier
- `copyright` (str): Copyright information
- `notice_text` (str): Full notice text
- `source` (str): Where the package was found

**Example:**
```python
package = Package(
    name="express",
    version="4.17.1",
    license="MIT",
    copyright="Copyright (c) 2009-2014 TJ Holowaychuk",
    notice_text="Full license text...",
    source="package.json"
)
```

### NoticeFormat

Enum for output formats.

```python
from ossnotices import NoticeFormat

NoticeFormat.TEXT   # Plain text format
NoticeFormat.HTML   # HTML format
NoticeFormat.JSON   # JSON format
```

## Examples

### Basic Usage

```python
from ossnotices import NoticesGenerator

# Create generator
generator = NoticesGenerator()

# Scan a directory
packages = generator.scan_directory("./src", recursive=True)

# Generate notices
notices = generator.generate_notices(packages, format='text')

# Save to file
generator.save_notices(notices, "NOTICE.txt")

print(f"Generated notices for {len(packages)} packages")
```

### With Caching

```python
from ossnotices import NoticesGenerator

generator = NoticesGenerator(cache_enabled=True)

# First run - will cache results
packages = generator.scan_directory("./large-project", recursive=True)

# Subsequent run - uses cache
packages = generator.scan_directory("./large-project", recursive=True)
```

### Custom Processing

```python
from ossnotices import NoticesGenerator

generator = NoticesGenerator()
packages = generator.scan_directory("./project")

# Filter packages
filtered = [p for p in packages if p.license != "MIT"]

# Custom formatting
for package in filtered:
    print(f"{package.name} ({package.version}): {package.license}")

# Generate notices only for filtered packages
notices = generator.generate_notices(filtered)
```

### Archive Processing

```python
from ossnotices import NoticesGenerator

generator = NoticesGenerator()

# Process multiple archives
archives = ["lib1.jar", "lib2.war", "package.whl"]
all_packages = []

for archive in archives:
    packages = generator.scan_archive(archive)
    all_packages.extend(packages)

# Generate combined notices
notices = generator.generate_notices(all_packages, format='html')
generator.save_notices(notices, "combined-notices.html")
```

### JSON Output Processing

```python
import json
from ossnotices import NoticesGenerator

generator = NoticesGenerator()
packages = generator.scan_directory("./project")

# Generate JSON
json_notices = generator.generate_notices(packages, format='json')

# Parse and process
data = json.loads(json_notices)
print(f"Total packages: {data['metadata']['total_packages']}")

# Extract specific information
licenses = {}
for package in data['packages']:
    license_type = package['license']
    if license_type not in licenses:
        licenses[license_type] = []
    licenses[license_type].append(package['name'])

print("Packages by license:")
for license_type, names in licenses.items():
    print(f"  {license_type}: {', '.join(names)}")
```

### Integration with purl2notices

Since ossnotices is built on purl2notices, you can also use the underlying library directly:

```python
from purl2notices import Purl2Notices
import asyncio

async def advanced_processing():
    processor = Purl2Notices()

    # Process specific PURLs
    package = await processor.process_single_purl("pkg:npm/express@4.0.0")

    # Generate notices
    notices = processor.generate_notices([package])

    return notices

# Run async function
notices = asyncio.run(advanced_processing())
print(notices)
```

## Error Handling

```python
from ossnotices import NoticesGenerator, NoticesError

generator = NoticesGenerator()

try:
    packages = generator.scan_directory("/invalid/path")
except NoticesError as e:
    print(f"Error generating notices: {e}")
except FileNotFoundError:
    print("Directory not found")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration

```python
from ossnotices import NoticesGenerator

# Configure generator
generator = NoticesGenerator(
    cache_enabled=True,
    cache_file=".custom-cache.json",
    verbose=True,
    timeout=30  # Network timeout in seconds
)
```

## See Also

- [User Guide](user-guide.md) - Comprehensive usage guide
- [Examples](examples.md) - Common use cases and workflows
- [purl2notices API](https://github.com/SemClone/purl2notices) - Underlying library documentation