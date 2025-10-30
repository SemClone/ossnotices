# OSS Notices

A simplified CLI wrapper for generating open source legal notices using the powerful [purl2notices](https://github.com/SemClone/purl2notices) library.

## Features

- **Simple Interface**: Streamlined CLI for common use cases
- **Multiple Input Types**: Process directories, archives, PURL lists, or single PURLs
- **Format Options**: Generate notices in text, HTML, or JSON formats
- **Smart Caching**: Automatic caching for faster subsequent runs
- **Progress Feedback**: Visual progress indicators with rich terminal output

## Installation

```bash
pip install ossnotices
```

For development:
```bash
git clone <repository>
cd ossnotices
pip install -e .
```

## Quick Start

### Scan current directory
```bash
ossnotices .
```

### Scan directory recursively and save to file
```bash
ossnotices ./src --recursive -o NOTICE.txt
```

### Generate HTML format
```bash
ossnotices ./project -f html -o notices.html
```

### Process a JAR file
```bash
ossnotices library.jar
```

### Process a list of PURLs
Create a file with PURLs (one per line):
```
pkg:npm/express@4.0.0
pkg:pypi/django@4.2.0
pkg:maven/org.apache.commons/commons-lang3@3.12.0
```

Then process it:
```bash
ossnotices packages.txt -o NOTICE.txt
```

## Command Line Options

```
Usage: ossnotices [OPTIONS] INPUT_PATH

Arguments:
  INPUT_PATH  Directory, archive, PURL list file, or single PURL

Options:
  --version              Show version and exit
  -o, --output PATH      Output file path (default: NOTICE.txt)
  -f, --format TYPE      Output format: text, html, json (default: text)
  -r, --recursive        Scan directories recursively
  --cache/--no-cache     Enable/disable caching (default: enabled)
  -v, --verbose          Enable verbose output
  -q, --quiet           Suppress all output except errors
  --help                Show help and exit
```

## Input Types

**ossnotices** automatically detects the input type:

- **Directory**: Scans for packages in source code
- **Archive**: Processes JAR, WAR, WHL, ZIP, TAR files
- **PURL List**: Text file with Package URLs (one per line)
- **Single PURL**: Direct package URL string

## Output Formats

### Text Format (default)
Plain text notices suitable for inclusion in distributions:
```
ossnotices ./project -o NOTICE.txt
```

### HTML Format
Web-friendly format with styling:
```bash
ossnotices ./project -f html -o notices.html
```

### JSON Format
Structured data for further processing:
```bash
ossnotices ./project -f json -o notices.json
```

## Examples

### Generate notices for a Python project
```bash
ossnotices ./my-python-app --recursive -o NOTICE.txt
```

### Process a Java application (JAR file)
```bash
ossnotices app.jar -o NOTICE.txt
```

### Generate HTML notices for documentation
```bash
ossnotices ./src -f html -o docs/licenses.html
```

### Quiet mode for CI/CD pipelines
```bash
ossnotices . -q -o NOTICE.txt
```

### Verbose mode for debugging
```bash
ossnotices . -v -o NOTICE.txt
```

## Caching

By default, ossnotices caches package information to speed up subsequent runs. The cache is stored in `.ossnotices.cache.json` in the current directory.

To disable caching:
```bash
ossnotices . --no-cache
```

## Under the Hood

This tool leverages the powerful [purl2notices](https://github.com/SemClone/purl2notices) library, which provides:

- Support for 12+ package ecosystems (npm, PyPI, Maven, Cargo, Go, NuGet, Conda, etc.)
- Smart license extraction using multiple detection engines
- CycloneDX cache format
- Customizable templates and overrides

For advanced use cases, consider using purl2notices directly.

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please use the GitHub issue tracker.