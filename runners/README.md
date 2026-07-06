# Runners

Scripts for running the companion code examples.

## `runner.sh`

Executes all Python scripts across all chapters with formatted, educational output. Spreadsheets and configuration files are listed with instructions on how to use them.

### Run All Chapters

```bash
./runners/runner.sh
```

### Run a Single Chapter

```bash
./runners/runner.sh 4    # Run only Chapter 4 examples
./runners/runner.sh 10   # Run only Chapter 10 examples
```

### What It Does

For each chapter, the runner:

1. **Executes Python scripts** with clear headers explaining what each script demonstrates
2. **Lists spreadsheet files** (`.xlsx`) with instructions on what to do — which columns to fill in, what the output tells you, and where to find interactive versions on the [companion site](https://ddpe.platformetrics.com)
3. **Lists configuration files** (`.yaml`, `.sql`, `.rego`, `.http`) with usage context

### Prerequisites

```bash
pip install -r requirements.txt
```

The only required dependency is `openpyxl`. OpenTelemetry packages are optional — scripts handle their absence gracefully.

### Interactive Assessment Models

Many of the spreadsheet-based assessment tools in this repository have interactive equivalents on the companion site at [ddpe.platformetrics.com](https://ddpe.platformetrics.com). The interactive versions are kept up to date as frameworks and best practices evolve.
