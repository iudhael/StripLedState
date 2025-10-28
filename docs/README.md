# StripLedState Documentation

This directory contains the source files for the StripLedState documentation, built with MkDocs and Material theme. API documentation is automatically generated from code docstrings.

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   uv sync --group docs
   ```

2. **Serve locally:**
   ```bash
   uv run mkdocs serve
   ```
   
   Open http://127.0.0.1:8000 in your browser.

3. **Build for production:**
   ```bash
   uv run mkdocs build
   ```

### GitHub Pages Deployment

The documentation is automatically built and deployed to GitHub Pages via GitHub Actions:

1. **Push changes** to the main branch
2. **GitHub Actions** builds the site automatically using uv
3. **Documentation** is available at: https://iudhael.github.io/StripLedStatel/

## Documentation Structure

```
docs/
├── index.md                    # Home page
├── installation.md             # Installation guide  
├── getting-started.md          # Quick start tutorial
├── user-guide/
│   ├── basic-usage.md          # Core concepts and basic operations
│   └── cli.md                  # Command-line interface
├── api-reference/              # Auto-generated from docstrings
│   ├── StripLedStatel/              # Main package docs
│   │   ├── index.md            # Package overview
│   │   ├── core/               # Core module docs
│   │   │   ├── AddrStripLedSignalisation.md       # first version led signalisation
│   │   │   └── AddrStripLedSignalisationNonBloquant.md     # second version led signalisation
│   │   │   └── AddrStripLedSignalisationNonBloquant2.md     # Third version led signalisation
│   │   └── logging.md          # Logging system (auto-generated)
│   └── cli.md                  # CLI module (auto-generated)
├── troubleshooting.md          # Common issues and solutions
├── gen_ref_pages.py            # Auto-generation script
└── stylesheets/
    └── extra.css               # Custom styling
```

## Auto-Generated API Documentation

The API reference is automatically generated from your code's docstrings using:

- **mkdocstrings**: Extracts and formats Python docstrings
- **mkdocs-gen-files**: Generates markdown files from code structure  
- **mkdocs-literate-nav**: Creates navigation from generated content

This ensures the documentation stays in sync with your code and leverages your excellent existing docstrings.

## Configuration

The documentation is configured in `mkdocs.yml`:

- **Theme**: Material Design with auto-generation plugins
- **Features**: Navigation tabs, search, code copying, dark/light mode
- **Extensions**: Code highlighting, admonitions, tables, etc.
- **Plugins**: Auto-generation, mkdocstrings, search, git revision dates

## Contributing to Documentation

### Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add it to the `nav` section in `mkdocs.yml`
3. Follow the existing style and structure

### Writing Style

- Use clear, concise language
- Include code examples for all concepts
- Use admonitions for important notes/warnings
- Add cross-references between related pages

### Code Examples

````markdown
```python
from StripLedStatel import AddrStripLedSignalisationNonBloquant2



def main():

    leds = AddrStripLedSignalisationNonBloquant2()

    

    while(1):


        leds.ready()
        #leds.turn_off_all_stripled()


    
    
if __name__ == "__main__":
    main()

```
````


## Custom Styling

Custom CSS is in `docs/stylesheets/extra.css`:

- Brand colors and theme customization
- Enhanced code blocks and tables
- Protocol frame visualization
- Responsive improvements
- Dark theme support

## TODO Items

The following pages need to be created:

- [ ] `user-guide/advanced-usage.md` - Complex scenarios, multiple servos, calibration
- [ ] `user-guide/raspberry-pi.md` - Pi-specific setup and examples
- [ ] `api-reference/protocol.md` - Detailed protocol documentation
- [ ] `examples/basic-servo-control.md` - Step-by-step examples
- [ ] `examples/raspberry-pi-setup.md` - Pi project examples
- [ ] `examples/advanced-scenarios.md` - Complex use cases
- [ ] `development/contributing.md` - Development setup and guidelines
- [ ] `development/testing.md` - Testing framework and guidelines
- [ ] `development/protocol-details.md` - Low-level protocol implementation

## Dependencies

Documentation dependencies (in `pyproject.toml` docs group):

- `mkdocs>=1.5.0` - Static site generator
- `mkdocs-material>=9.0.0` - Material Design theme  
- `mkdocstrings[python]>=0.24.0` - Auto-generation from docstrings
- `mkdocs-gen-files>=0.5.0` - File generation utilities
- `mkdocs-literate-nav>=0.6.0` - Navigation from generated content
- `mkdocs-git-revision-date-localized-plugin>=1.2.0` - Last updated dates

## Maintenance

- Update version numbers when releasing
- Review and update examples for accuracy
- Check all links periodically
- Update screenshots if UI changes
- Keep dependencies up to date

## GitHub Pages Setup

1. **Enable GitHub Pages** in repository settings
2. **Source**: GitHub Actions
3. **Custom domain** (optional): Configure in repository settings
4. **HTTPS**: Automatically enabled by GitHub

The `.github/workflows/docs.yml` file handles the build and deployment process.
