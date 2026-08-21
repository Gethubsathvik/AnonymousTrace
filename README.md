# 🕵️ AnonymousTrace
A data-driven, extensible OSINT (Open-Source Intelligence) username reconnaissance tool that checks whether usernames are registered on 100+ public platforms using only unauthenticated, publicly accessible endpoints.


<img width="1193" height="545" alt="Image" src="https://github.com/user-attachments/assets/28c62126-c64e-4b56-a656-a349abf2a6ec" />
<img width="800" height="830" alt="Image" src="https://github.com/user-attachments/assets/70ae689c-1ff6-4aca-a45b-7bb1ba15fbe3" />

## ✨ Features
- **📊 Data-Driven Architecture**: Platform definitions stored in JSON registry - add new sites without code changes
- **🔍 Multiple Detection Strategies**: Status code, message content, response URL analysis, and hybrid confidence scoring
- **⚡ High Performance**: Concurrent scanning with bounded worker pools and rate limiting
- **🛡️ Resilient**: Retry with exponential backoff, proxy support, Tor integration, error isolation
- **🎨 Rich Output**: Colorized terminal output, JSON/CSV/XLSX/TXT export options
- **🌐 Cross-Platform**: Works on Windows, macOS, Linux
- **🐳 Containerized**: Docker support for easy deployment
- **🧪 Well Tested**: Comprehensive test suite with CI/CD pipelines
- **⚖️ Ethical Use**: Built-in authorization banner and ETHICS guidelines
- **🦸 Superpowers**: Advanced scanning modes (--fast, --deep, --stealth, --super)


## Test Run Here
[![Open in Google Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=YOUR_GITHUB_REPO_URL)

[![Run on Replit](https://replit.com/badge/github/USERNAME/REPOSITORY)](https://replit.com/github/USERNAME/REPOSITORY)

## 🛠️ Complete CLI Reference

```
usage: AnonymousTrace [-h] [--site SITES] [--timeout TIMEOUT] [--proxy PROXY_URL]
                   [--tor] [--unique-tor] [--dump-response] [--json JSON_FILE]
                   [--print-all] [--print-found] [--no-color] [--browse]
                   [--local] [--nsfw] [--txt] [--ignore-exclusions]
                   [--data-file DATA_FILE] [--verbose] [--folderoutput FOLDEROUTPUT]
                   [--output OUTPUT] [--csv] [--xlsx] [--version] [-s] [--super]
                   [--fast] [--deep] [--stealth] [--list-sites] [--plain]
                   [--workers WORKERS] [--min-confidence {found,likely,unknown}]
                   [--rate-limit RATE_LIMIT] [--input-file INPUT_FILE]
                   USERNAMES [USERNAMES ...]

positional arguments:
  USERNAMES             One or more usernames to check with social networks

options:
  -h, --help            show this help message and exit
  --site SITES          Limit analysis to just the listed sites (repeatable)
  --timeout TIMEOUT     Time (in seconds) to wait for response to requests (Default: 60)
  --proxy, -p PROXY_URL
                        Make requests over a proxy. e.g. socks5://127.0.0.1:1080
  --tor                 Route through Tor SOCKS proxy
  --unique-tor          Route through Tor, requesting a new circuit per request
  --dump-response       Dump the HTTP response to stdout for targeted debugging
  --json JSON_FILE      JSON output file
  --print-all           Output sites where the username was not found
  --print-found         Output sites where the username was found (also if exported as file)
  --no-color            Don't color terminal output
  --browse, -b          Browse to all results on default browser
  --local, -l           Force the use of the local data.json file
  --nsfw                Include checking of NSFW sites from default list
  --txt                 Enable creation of a txt file
  --ignore-exclusions   Ignore upstream exclusions (may return more false positives)
  --data-file DATA_FILE
                        Load data from a JSON file or an online, valid, JSON file
  --verbose, -v, -d, --debug
                        Display extra debugging information and metrics
  --folderoutput, -fo FOLDEROUTPUT
                        If using multiple usernames, the output of the results will be saved to this folder
  --output, -o OUTPUT   If using single username, the output of the result will be saved to this file
  --input-file INPUT_FILE
                        Batch usernames from a text file (one per line)
  --csv                 Create Comma-Separated Values (CSV) File
  --xlsx                Create the standard file for the modern Microsoft Excel spreadsheet
  --version             show program's version number and exit
  -s, --scan            Quick scan mode - fast scan with default settings
  --super               Super mode - enables verbose output, print-all, and JSON export
  --fast                Fast mode - high speed scan with reduced timeout
  --deep                Deep mode - thorough scan with extended timeout and all sites
  --stealth             Stealth mode - slow scan with low profile (rate limiting + Tor)
  --list-sites          List all available platforms and exit
  --plain               Plain text output - simple list format without tables
  --workers WORKERS     Concurrent worker threads (default: 20)
  --min-confidence {found,likely,unknown}
                        Minimum confidence level to report (default: unknown)
  --rate-limit RATE_LIMIT
                        Polite throttle in seconds between requests to the same host
```


### 📝 Terminal Output (Plain Text)
```
[*] Checking username user123 on:
[+] 9GAG: https://www.9gag.com/u/user123
[+] AskFM: https://ask.fm/user123
[+] BitBucket: https://bitbucket.org/user123
[+] GitHub: https://github.com/user123
[+] GitLab: https://gitlab.com/user123
[+] Reddit: https://www.reddit.com/user/user123
[+] YouTube: https://www.youtube.com/@user123
[*] Search completed with 29 results.
```

## 🚀 Installation

### 📦 Using pipx (Recommended)
```bash
pipx install AnonymousTrace
```

### 📥 Using pip
```bash
pip install AnonymousTrace
```

### 🛠️ From Source
```bash
git clone https://github.com/yourusername/AnonymousTrace.git
cd AnonymousTrace
pip install -e .
```

### 🐳 Using Docker
```bash
docker build -t anonymoustrace .
docker run --rm anonymoustrace github gitlab --print-found
```

Or with docker-compose:
```bash
docker-compose run --rm anonymoustrace github gitlab --print-found
```

## SET Path
$env:Path = [Environment]::GetEnvironmentVariable('Path', 'User')

AnonymousTrace -h


## 🎯 Quick Start

**No PATH setup needed. Works everywhere: Windows, Linux, macOS, Claude Code, online IDEs.**

```bash
python -m anonymoustrace.main username1
```

That's it. The `-m` flag runs the tool directly from the source tree, no installation or PATH configuration required.

## 💻 Platform-Specific Launchers

If you prefer shorter commands, use the included launchers:

**Windows:**
```powershell
.\run.bat user123
```

**Linux / macOS:**
```bash
bash run.sh user123
```

## ☁️ Run in Cloud / Online IDEs

```bash
git clone https://github.com/yourusername/AnonymousTrace.git
cd AnonymousTrace
python -m anonymoustrace.main --list-sites
python -m anonymoustrace.main user123
```

## 📖 Usage

### 🔰 General Usage

**To search for only one user:**
```bash
python -m anonymoustrace.main user123
```

**To search for more than one user:**
```bash
python -m anonymoustrace.main user1 user2 user3
```

### 📋 List All Platforms
```bash
python -m anonymoustrace.main --list-sites
```

### 🎛️ Check Specific Platforms
```bash
python -m anonymoustrace.main username --site github --site twitter --site reddit
```

### 💾 Export Results
```bash
python -m anonymoustrace.main username --json results.json
python -m anonymoustrace.main username --csv results.csv
python -m anonymoustrace.main username --xlsx results.xlsx
python -m anonymoustrace.main username --txt results.txt
python -m anonymoustrace.main username --folderoutput ./results/
```

### 🌐 Load Custom Registry
```bash
# Load from local JSON file
python -m anonymoustrace.main username --data-file ./my_sites.json

# Load from online JSON
python -m anonymoustrace.main username --data-file https://example.com/registry.json
```

### ⚙️ Advanced Options
```bash
python -m anonymoustrace.main username \
  --workers 50 \
  --timeout 15 \
  --rate-limit 0.1 \
  --proxy http://proxy.example.com:8080 \
  --tor \
  --unique-tor \
  --min-confidence likely \
  --input-file usernames.txt \
  --print-all
```

## 🦸 Superpowers (Advanced Flags)

The framework comes with superpowers that give you extra control and speed:

### ⚡ `-s` / `--scan` - Quick Scan Mode
Quick scan with default settings for fast results.
```bash
python -m anonymoustrace.main -s username
```

### 🌐 `-d` / `--domain` - Domain Reconnaissance
Check domain presence across multiple platforms.
```bash
python -m anonymoustrace.main -d example.com
```

### 🦸 `--super` - Super Mode
Enables all features at once: verbose output, print-all, and JSON export.
```bash
python -m anonymoustrace.main --super username
```

### 🚀 `--fast` - Fast Mode
High speed scan with reduced timeout and more workers.
```bash
python -m anonymoustrace.main --fast username
```

### 🔬 `--deep` - Deep Scan Mode
Thorough scan with extended timeout and all sites checked.
```bash
python -m anonymoustrace.main --deep username
```

### 👻 `--stealth` - Stealth Mode
Slow scan with low profile: rate limiting + Tor routing.
```bash
python -m anonymoustrace.main --stealth username --tor
```

### 📋 `--list-sites` - List All Platforms
Show all 100+ available platforms in the registry.
```bash
python -m anonymoustrace.main --list-sites
```

### 📝 `--plain` - Plain Text Output
Simple list format output like:
```
[*] Checking username hackerman1357 on:
[+] 9GAG: https://www.9gag.com/u/hackerman1337
[+] AskFM: https://ask.fm/hackerman1337
[+] GitHub: https://github.com/hackerman1337
[+] GitLab: https://gitlab.com/hackerman1337
[+] Reddit: https://www.reddit.com/user/hackerman1337
[+] YouTube: https://www.youtube.com/@hackerman1337
[*] Search completed with 29 results.
```
```bash
python -m anonymoustrace.main --plain username
```

### 🌍 `--data-file` - Load Custom Registry
Load site definitions from a local JSON file or online URL.
```bash
# Local file
python -m anonymoustrace.main username --data-file ./custom_registry.json

# Online URL
python -m anonymoustrace.main username --data-file https://example.com/registry.json
```

## 🏗️ MVC Architecture

AnonymousTrace follows a clean **Model-View-Controller** separation for maintainability and extensibility.

```
anonymoustrace/
├── data/
│   └── registry.json          ← Model: platform definitions
├── models/
│   └── __init__.py            ← Model: Site, ScanResult, ConfidenceLevel, ErrorType
├── features/
│   ├── detection/
│   │   └── detectors.py       ← Controller: detection strategies (status_code, message, response_url, hybrid)
│   └── scanning/
│       ├── concurrent_scanner.py ← Controller: bounded thread-pool scan orchestrator
│       ├── http_client.py        ← Controller: HTTP session, retries, proxy/Tor
│       └── registry_loader.py    ← Controller: JSON registry loader with validation
├── services/
│   ├── detection_service.py   ← Controller: detection orchestration and strategy selection
│   ├── export_service.py      ← Controller: JSON/CSV/XLSX/TXT export
│   ├── proxy_service.py       ← Controller: proxy validation and Tor routing
│   ├── resilience_service.py  ← Controller: retry with exponential backoff + jitter
│   └── scan_service.py        ← Controller: top-level scan pipeline wiring
└── main.py                    ← View: CLI (argparse) + Rich terminal output
```

### 📦 Model Layer

Responsible for **data structures and state**.

| Component | File | Responsibility |
|-----------|------|----------------|
| `Site` | `models/__init__.py` | Platform definition: URL patterns, error types, headers, regex validation |
| `ScanResult` | `models/__init__.py` | Single scan outcome: detected status, confidence, HTTP code, error, metadata |
| `ConfidenceLevel` | `models/__init__.py` | Enum: `found`, `likely`, `unknown`, `not_found` |
| `ErrorType` | `models/__init__.py` | Enum: `status_code`, `message`, `response_url`, `hybrid` |
| `registry.json` | `data/registry.json` | 100+ platform definitions — add new sites here without code changes |

### 🎨 View Layer

Responsible for **user interaction and presentation**.

| Component | File | Responsibility |
|-----------|------|----------------|
| CLI parser | `main.py:build_parser()` | `argparse` setup — flags, positional args, help text |
| Banner | `main.py:BANNER` | Rich ASCII art + authorization notice |
| Terminal tables | `main.py` | Color-coded Rich tables, progress bars, live updates |
| Export triggers | `main.py` | Calls `ExportService` after scan completes |

### ⚙️ Controller Layer

Responsible for **business logic and orchestration**.

| Component | File | Responsibility |
|-----------|------|----------------|
| `ScanService` | `services/scan_service.py` | Top-level pipeline: load registry → scan → export |
| `DetectionService` | `services/detection_service.py` | Selects and runs the correct detector per site |
| `ConcurrentScanner` | `features/scanning/concurrent_scanner.py` | Bounded `ThreadPoolExecutor` scan with confidence filtering |
| `HTTPClient` | `features/scanning/http_client.py` | `requests.Session` with pooling, retries, proxy/Tor |
| `RegistryLoader` | `features/scanning/registry_loader.py` | Loads `registry.json` from disk or URL, validates entries |
| Detectors | `features/detection/detectors.py` | `StatusCodeDetector`, `MessageDetector`, `ResponseUrlDetector`, `HybridDetector` |
| `ExportService` | `services/export_service.py` | Writes results to JSON, CSV, XLSX, TXT |
| `ProxyService` / `TorService` | `services/proxy_service.py` | Proxy URL validation, Tor SOCKS routing |
| `retry_with_backoff` | `services/resilience_service.py` | Exponential backoff + jitter decorator for resilient HTTP calls |

### 🔄 Data Flow

```
User Input (CLI)
       │
       ▼
┌─────────────────┐
│   main.py       │  ← View: parse args, display banner
│  (Controller)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ScanService    │  ← Controller: orchestrate pipeline
│  RegistryLoader │  ← Load sites from data/registry.json (Model)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ConcurrentScanner│ ← Controller: spawn workers
│   HTTPClient    │ ← Controller: make requests with retry/proxy
│   Detectors     │ ← Controller: analyze response → ScanResult (Model)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ExportService  │ ← Controller: write JSON/CSV/XLSX/TXT
│  Rich Tables    │ ← View: print results to terminal
└─────────────────┘
```

### 🧩 Extending the Framework

**Add a new platform:** Edit `data/registry.json` — no code changes needed.

**Add a new detection strategy:** Create a new `BaseDetector` subclass in `features/detection/detectors.py` and register it in `build_detector()`.

**Add a new export format:** Extend `ExportService` in `services/export_service.py` and wire it into `ScanService.execute()`.

## 🔍 Detection Strategies

1. **📊 Status Code**: Determines availability based on HTTP status (200 vs 404)
2. **📝 Message**: Looks for specific error text in response body
3. **🔗 Response URL**: Compares final URL after redirects to known "not found" URL
4. **🎯 Hybrid (Original)**: Combines multiple signals (status, content, size) to produce confidence levels:
   - `✅ found`: High confidence the username exists
   - `🟡 likely`: Moderate confidence
   - `⚪ unknown`: Inconclusive results
   - `❌ not_found`: High confidence the username doesn't exist

## ⚙️ Configuration

The platform registry (`anonymoustrace/data/registry.json`) defines each site with:

```json
{
  "PlatformName": {
    "errorType": "status_code | message | response_url | hybrid",
    "url": "https://platform.example/{}",
    "urlMain": "https://platform.example/",
    "urlProbe": "https://platform.example/api/check/{}",  // optional
    "errorMsg": "User not found",
    "errorUrl": "https://platform.example/404",
    "regexCheck": "^[a-zA-Z0-9_]{3,20}$",
    "username_claimed": "validtestuser",
    "username_unclaimed": "definitelynotrealuser123",
    "headers": { "User-Agent": "AnonymousTrace/1.0" },
    "request_method": "GET",
    "request_payload": null
  }
}
```

## ⚖️ Ethics and Legal Use

This tool is designed for authorized, legitimate OSINT purposes only. See [ETHICS.md](ETHICS.md) for detailed guidelines.

**🔑 Key Principles:**
- ✅ Only query public, unauthenticated endpoints
- ✅ Respect rate limits and terms of service
- ✅ Do not use for stalking, harassment, or doxxing
- ✅ You are responsible for complying with applicable laws and platform ToS
- ✅ Scan results should be handled securely and deleted when no longer needed

## 📤 Output Formats

### 🖥️ Terminal Output (Rich Table)
Color-coded table showing detection status, confidence level, HTTP status code, and any errors.

### 📄 JSON Export
```json
{
  "username": "testuser",
  "count": 2,
  "results": [
    {
      "username": "testuser",
      "site": "github",
      "detected": true,
      "confidence": "found",
      "status_code": 200,
      "response_url": "https://github.com/testuser",
      "response_size": 12543,
      "error": null,
      "metadata": { "signals": ["status_200", "msg_not_found"], "score": 3 }
    }
  ]
}
```

### 📊 CSV Export
```
username,site,detected,confidence,status_code,error
testuser,github,true,found,200,
testuser,twitter,false,not_found,404,
```

### 📗 XLSX Export
Microsoft Excel format with formatted headers and data rows.

### 📄 TXT Export
Plain text summary with found profiles listed.

## 🧪 Development

### 🧪 Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=anonymoustrace --cov-report=term-missing

# Run specific test suite
pytest tests/test_detection.py
```

### 🔍 Code Quality
```bash
# Linting
ruff check anonymoustrace/

# Type checking
mypy anonymoustrace/

# Formatting
ruff format anonymoustrace/
```

## 🌍 Platform Support

The framework includes definitions for over 100 platforms including:
- **📱 Social Media**: Twitter, Instagram, TikTok, Reddit, LinkedIn, Facebook
- **💻 Development**: GitHub, GitLab, Bitbucket, StackOverflow, DockerHub
- **🎨 Creative**: Behance, Dribbble, DeviantArt, SoundCloud, Spotify
- **💼 Professional**: AngelList, Crunchbase, Product Hunt
- **🔗 And many more...**

See `anonymoustrace/data/registry.json` for the complete list.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 🚀 Push to the branch (`git push origin feature/amazing-feature`)
5. 📬 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
