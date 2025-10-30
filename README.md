# OSS Notices

A simplified CLI wrapper for generating open source legal notices from local source code using the powerful [purl2notices](https://github.com/SemClone/purl2notices) library.

## Features

- **Simple Interface**: Streamlined CLI for scanning local source code
- **Directory Scanning**: Recursively analyze directories for package dependencies
- **Archive Support**: Process JAR, WAR, WHL, ZIP, and other archive formats
- **Multiple Output Formats**: Generate notices in text, HTML, or JSON
- **Smart Caching**: Automatic caching for improved performance
- **Progress Indicators**: Visual feedback with rich terminal output

## Installation

```bash
pip install ossnotices
```

For development:
```bash
git clone https://github.com/SemClone/ossnotices.git
cd ossnotices
pip install -e .
```

## Quick Start

```bash
# Scan current directory (default)
ossnotices

# Scan specific directory
ossnotices ./src

# Scan recursively and save to file
ossnotices ./project --recursive -o NOTICE.txt

# Generate HTML format
ossnotices ./project -f html -o notices.html

# Process a JAR file
ossnotices library.jar -o NOTICE.txt
```

## Command Line Options

```
Usage: ossnotices [OPTIONS] [PATH]

Arguments:
  PATH  Directory or archive file to scan (default: current directory)

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

- **Directory**: Scans source code for package dependencies
- **Archive**: Processes JAR, WAR, WHL, ZIP, TAR, GZ, BZ2, EGG files

## Output Formats

### Text Format (default)
Plain text notices suitable for inclusion in distributions:
```bash
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

### Scan a Python project
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

### Scan current directory with default settings
```bash
ossnotices
```

### Quiet mode for CI/CD pipelines
```bash
ossnotices . -q -o NOTICE.txt
```

### Verbose mode for debugging
```bash
ossnotices . -v
```

## Caching

By default, ossnotices caches package information to speed up subsequent runs. The cache is stored in `.ossnotices.cache.json` in the current directory.

To disable caching:
```bash
ossnotices . --no-cache
```

## Supported Package Ecosystems

Through purl2notices, ossnotices supports:
- Python (PyPI)
- JavaScript/Node.js (npm)
- Java (Maven)
- Ruby (RubyGems)
- Go modules
- Rust (Cargo)
- .NET (NuGet)
- PHP (Composer)
- And many more...

## Under the Hood

This tool leverages [purl2notices](https://github.com/SemClone/purl2notices), which provides:

- Support for 12+ package ecosystems
- Multiple license detection engines
- Smart extraction from various archive formats
- CycloneDX cache format support

For advanced use cases requiring direct PURL processing or custom configurations, consider using purl2notices directly.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please use the [GitHub issue tracker](https://github.com/SemClone/ossnotices/issues).