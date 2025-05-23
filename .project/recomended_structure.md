opencostcalculator/
├── bin/                         # Optional: Executable entry scripts
│   └── opencostcalculator
├── src/
│   └── opencostcalculator/
│       ├── __init__.py
│       ├── main.py              # CLI entrypoint
│       ├── core/                # Orchestrates parsing, pricing, and reporting
│       │   ├── parser.py
│       │   ├── pricing.py
│       │   └── report.py
│       ├── resources/           # Per-resource analyzers
│       │   ├── eks.py
│       │   ├── rds.py
│       │   ├── alb.py
│       │   └── ...
│       └── utils/               # Logging, filters, config helpers
│           ├── logger.py
│           ├── config.py
│           └── filters.py
├── tests/                       # Pytest-based test suite
│   ├── test_main.py
│   ├── test_parser.py
│   └── ...
├── docs/                        # Contributor & usage docs
│   ├── usage.md
│   └── contributing.md
├── project/                     # Internal docs (planning, progress)
│   ├── project.md
│   ├── architecture.md
│   ├── techstack.md
│   └── progress.md
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions: Lint, Test, Package
├── .gitignore
├── Makefile                     # Developer commands
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Dev/test tools
├── pyproject.toml               # Package config (preferred over setup.py)
└── README.md                    # Project intro and CLI usage