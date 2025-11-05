# OSS Notices Generator - Simplified Legal Notices for Open Source Projects

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/ossnotices.svg)](https://pypi.org/project/ossnotices/)

A streamlined tool for generating legal notices from open source dependencies. Built on the powerful [purl2notices](https://github.com/SemClone/purl2notices) library, ossnotices provides a simple interface for scanning source code and producing attribution documentation required for OSS compliance.

## Features

- **Simple Interface**: Streamlined CLI for scanning local source code and archives
- **Multi-Format Support**: Generate notices in text, HTML, or JSON formats
- **Archive Processing**: Handle JAR, WAR, WHL, ZIP, and other archive formats
- **SEMCL.ONE Integration**: Seamlessly works with other ecosystem tools for comprehensive compliance workflows

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
# Scan current directory and generate default NOTICE.txt
ossnotices

# Process a specific project directory
ossnotices ./my-project --recursive -o NOTICE.txt
```

## Usage

### CLI Usage

```bash
# Basic directory scanning
ossnotices ./src --recursive -o NOTICE.txt

# Process archive files
ossnotices library.jar -o NOTICE.txt

# Generate HTML format for documentation
ossnotices ./project -f html -o notices.html

# JSON output for further processing
ossnotices ./project -f json -o notices.json

# Quiet mode for CI/CD pipelines
ossnotices . -q -o NOTICE.txt
```

### Command Line Options

```
Usage: ossnotices [OPTIONS] [PATH]

Arguments:
  PATH                   Directory or archive file to scan (default: current directory)

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

## Configuration

Caching is enabled by default and stores package information in `.ossnotices.cache.json` for faster subsequent runs.

```bash
# Disable caching
ossnotices . --no-cache
```

## Integration with SEMCL.ONE

OSS Notices Generator is part of the comprehensive SEMCL.ONE compliance ecosystem:

- Works with **src2purl** for package identification
- Integrates with **purl2notices** for detailed attribution generation
- Complements **osslili** for license detection
- Supports **upmex** package metadata extraction

## Supported Input Types

- **Source Directories**: Recursively scans for package dependencies
- **Archive Files**: JAR, WAR, WHL, ZIP, TAR, GZ, BZ2, EGG formats

## Supported Package Ecosystems

Through purl2notices integration:
- Python (PyPI)
- JavaScript/Node.js (npm)
- Java (Maven)
- Ruby (RubyGems)
- Go modules
- Rust (Cargo)
- .NET (NuGet)
- PHP (Composer)
- And many more...

## Documentation

- [User Guide](docs/user-guide.md) - Comprehensive usage examples
- [API Reference](docs/api.md) - Python API documentation
- [Examples](docs/examples.md) - Common workflows and integration patterns

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Code of conduct
- Development setup
- Submitting pull requests
- Reporting issues

## Support

For support and questions:
- [GitHub Issues](https://github.com/SemClone/ossnotices/issues) - Bug reports and feature requests
- [Documentation](https://github.com/SemClone/ossnotices) - Complete project documentation
- [SEMCL.ONE Community](https://semcl.one) - Ecosystem support and discussions

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Authors

See [AUTHORS.md](AUTHORS.md) for a list of contributors.

---

*Part of the [SEMCL.ONE](https://semcl.one) ecosystem for comprehensive OSS compliance and code analysis.*