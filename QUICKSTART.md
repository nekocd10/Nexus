# Quick Start - Installation Guide

## 🚀 One-Liner Installation (Recommended)

### Using curl:
```bash
bash <(curl -sL https://github.com/nekocd10/maybe-a-custom-language/raw/main/installer.sh)
```

### Using wget:
```bash
bash <(wget -qO- https://github.com/nekocd10/maybe-a-custom-language/raw/main/installer.sh)
```

## What the Installer Does

✅ Detects your operating system (Linux, macOS, Windows)  
✅ Checks Python 3 installation  
✅ Downloads the repository (with fallback options)  
✅ Installs the Nexus package globally  
✅ Creates `nexus` command in your PATH  
✅ Verifies the installation  

## Alternative: Local Installation

If you prefer to install from the repository:

```bash
git clone https://github.com/nekocd10/maybe-a-custom-language
cd maybe-a-custom-language
bash install.sh
```

## Verify Installation

```bash
nexus --version
```

## First Program

```bash
# Create a file
echo 'println "Hello, Nexus!"' > hello.nexus

# Run it
nexus hello.nexus
```

## Next Steps

- 📖 Read [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md) for complete guide
- 📚 Check [examples/](examples/) for more examples
- 🔗 See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for project layout

---

**That's it! You're ready to start programming in Nexus!** 🎉
