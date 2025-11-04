# OSS Notices Generator - User Guide

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Output Formats](#output-formats)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

OSS Notices Generator is a streamlined tool for generating legal notices from open source dependencies. It simplifies the process of creating attribution documentation required for OSS compliance.

## Installation

### From PyPI

```bash
pip install ossnotices
```

### From Source

```bash
git clone https://github.com/SemClone/ossnotices.git
cd ossnotices
pip install -e .
```

### Verify Installation

```bash
ossnotices --version
```

## Basic Usage

### Scanning Current Directory

The simplest way to use ossnotices is to run it in your project directory:

```bash
ossnotices
```

This will:
1. Scan the current directory for dependencies
2. Generate a `NOTICE.txt` file with attribution information

### Scanning Specific Directories

To scan a specific directory:

```bash
ossnotices ./src
```

### Processing Archive Files

ossnotices can directly process archive files:

```bash
ossnotices library.jar -o NOTICE.txt
```

Supported archive formats:
- JAR (Java)
- WAR (Java web applications)
- WHL (Python wheels)
- ZIP
- TAR, GZ, BZ2
- EGG (Python eggs)

## Advanced Features

### Recursive Scanning

To scan directories recursively:

```bash
ossnotices ./project --recursive
```

### Custom Output Location

Specify where to save the notices:

```bash
ossnotices ./src -o licenses/NOTICE.txt
```

### Different Output Formats

#### HTML Format

Generate HTML notices for web documentation:

```bash
ossnotices ./project -f html -o notices.html
```

#### JSON Format

Generate structured JSON for further processing:

```bash
ossnotices ./project -f json -o notices.json
```

### Verbose and Quiet Modes

#### Verbose Mode (Debugging)

```bash
ossnotices ./project -v
```

Shows detailed progress and debugging information.

#### Quiet Mode (CI/CD)

```bash
ossnotices ./project -q
```

Suppresses all output except errors.

## Output Formats

### Text Format (Default)

Plain text format suitable for inclusion in distributions:

```
===============================================
Package: express
Version: 4.17.1
License: MIT
===============================================

MIT License

Copyright (c) 2009-2014 TJ Holowaychuk <tj@vision-media.ca>
Copyright (c) 2013-2014 Roman Shtylman <shtylman+expressjs@gmail.com>
Copyright (c) 2014-2015 Douglas Christopher Wilson <doug@somethingdoug.com>

[Full license text...]
```

### HTML Format

Styled HTML output with navigation:
- Collapsible sections for each package
- Hyperlinked package names
- Formatted license text
- Table of contents

### JSON Format

Structured data format:
```json
{
  "packages": [
    {
      "name": "express",
      "version": "4.17.1",
      "license": "MIT",
      "notice_text": "...",
      "copyright_holders": ["TJ Holowaychuk", "..."]
    }
  ],
  "metadata": {
    "scan_date": "2024-01-15",
    "total_packages": 42
  }
}
```

## Configuration

### Caching

By default, ossnotices caches package information to speed up subsequent runs.

#### Disable Caching

```bash
ossnotices . --no-cache
```

#### Cache Location

Cache is stored in `.ossnotices.cache.json` in the current directory.

### Environment Variables

You can configure ossnotices using environment variables:

```bash
export OSSNOTICES_OUTPUT_FORMAT=html
export OSSNOTICES_CACHE_ENABLED=false
```

## Troubleshooting

### Common Issues

#### No Packages Found

**Problem**: Running ossnotices returns no results.

**Solutions**:
1. Ensure you're in the right directory
2. Use `--recursive` flag for nested projects
3. Check if dependencies are in a supported format

#### Cache Issues

**Problem**: Outdated or corrupted cache.

**Solution**:
```bash
rm .ossnotices.cache.json
ossnotices . --no-cache
```

#### Permission Errors

**Problem**: Cannot write output file.

**Solution**: Ensure you have write permissions in the output directory.

### Debug Mode

For detailed troubleshooting, use verbose mode:

```bash
ossnotices . -v 2>&1 | tee debug.log
```

## Integration with CI/CD

### GitHub Actions

```yaml
- name: Generate OSS Notices
  run: |
    pip install ossnotices
    ossnotices . -q -o NOTICE.txt
```

### GitLab CI

```yaml
generate_notices:
  script:
    - pip install ossnotices
    - ossnotices . -q -o NOTICE.txt
  artifacts:
    paths:
      - NOTICE.txt
```

### Jenkins

```groovy
stage('Generate Notices') {
    steps {
        sh 'pip install ossnotices'
        sh 'ossnotices . -q -o NOTICE.txt'
    }
}
```

## Best Practices

1. **Regular Updates**: Regenerate notices when dependencies change
2. **Version Control**: Include NOTICE files in your repository
3. **Automation**: Integrate into CI/CD pipelines
4. **Review**: Manually review generated notices for accuracy
5. **Format Choice**: Use HTML for documentation, text for distributions

## See Also

- [API Reference](api.md) - Python API documentation
- [Examples](examples.md) - Common use cases and workflows
- [purl2notices](https://github.com/SemClone/purl2notices) - Underlying library