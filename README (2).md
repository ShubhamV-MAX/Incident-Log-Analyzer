# Log Analyzer

A Python utility for parsing, analyzing, and reporting on structured log files. This tool extracts log components (timestamp, level, message), counts entries by severity level, and generates a detailed analysis report.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Log File Format](#log-file-format)
- [Output](#output)
- [Function Reference](#function-reference)
- [Error Handling](#error-handling)
- [Example](#example)
- [Author](#author)

## Overview

The Log Analyzer is designed to process log files that follow a standardized format (YYYY-MM-DD HH:MM:SS LOG_LEVEL Message). It provides valuable insights into your application logs by categorizing entries by severity level (INFO, WARNING, ERROR) and extracting all error messages for review.

## Features

- **Log Parsing**: Extracts timestamp, log level, and message from structured log entries
- **Entry Classification**: Categorizes log entries into three severity levels: INFO, WARNING, and ERROR
- **Error Aggregation**: Collects all error messages with their timestamps for quick reference
- **Malformed Line Detection**: Tracks lines that don't match the expected format
- **Formatted Report**: Displays analysis results in a clean, readable format
- **Robust Error Handling**: Handles missing files and unexpected exceptions gracefully

## Installation

No special installation or external dependencies are required. This is a pure Python application that works with Python 3.x.

**Requirements:**
- Python 3.x

**Steps:**
1. Download `Log_Analyzer.py` to your desired directory
2. Ensure you have a log file named `app.log` in the same directory (or modify the `main()` function to point to your log file)

## Usage

### Basic Usage

Run the script from the command line:

```bash
python Log_Analyzer.py
```

This will analyze the default log file `app.log` in the current directory and display the results.

### Programmatic Usage

You can import the functions into another Python file:

```python
from Log_Analyzer import read_and_analyze_log, display_analysis_results

# Analyze a specific log file
results = read_and_analyze_log('your_logfile.log')

# Display the results
display_analysis_results(results)
```

### Analyzing a Different Log File

Modify the `main()` function or directly call `read_and_analyze_log()`:

```python
from Log_Analyzer import read_and_analyze_log, display_analysis_results

results = read_and_analyze_log('path/to/your/logfile.log')
if results:
    display_analysis_results(results)
```

## Log File Format

The log file must follow this exact format:

```
YYYY-MM-DD HH:MM:SS LOG_LEVEL Message content here...
```

### Format Specifications

| Component | Format | Example |
|-----------|--------|---------|
| Date | YYYY-MM-DD | 2024-08-26 |
| Time | HH:MM:SS | 14:30:45 |
| Log Level | INFO, WARNING, or ERROR | INFO |
| Message | Any text (can contain spaces) | Database connection established |

### Valid Log Levels

- `INFO`: Informational messages about normal operations
- `WARNING`: Warning messages indicating potential issues
- `ERROR`: Error messages indicating failures or exceptions

### Example Log Entries

```
2024-08-26 10:15:32 INFO Application started successfully
2024-08-26 10:16:01 WARNING Memory usage at 75%
2024-08-26 10:17:45 ERROR Failed to connect to database
2024-08-26 10:18:30 INFO Retry attempt 1 of 3
```

## Output

The Log Analyzer generates a formatted report with the following information:

### Summary Statistics

- **Total Entries**: Count of all valid log entries
- **INFO Count**: Number of informational entries
- **WARNING Count**: Number of warning entries
- **ERROR Count**: Number of error entries
- **Malformed Lines**: Count of lines that didn't match the expected format

### Error Details

If errors are found, the report displays each error with:
- Sequential index number
- Timestamp (date and time combined)
- Full error message

### Example Output

```
==================================================
            Log Analysis Results
==================================================

Total Entries: 127

INFO Entries: 89

WARNING Entries: 25

ERROR Entries: 13

==================================================
            Error Messages
==================================================

Error Messages:

1. [2024-08-26 10:17:45]
   Failed to connect to database

2. [2024-08-26 10:22:10]
   Timeout on API request

3. [2024-08-26 10:45:33]
   Insufficient disk space

==================================================
```

## Function Reference

### `log_line_phraser(line)`

Parses a single log line and extracts its components.

**Parameters:**
- `line` (str): A single line from the log file

**Returns:**
- `dict`: Contains keys `'date'`, `'time'`, `'level'`, `'message'` if valid
- `None`: If the line is empty, malformed, or has an invalid log level

**Error Handling:**
- Returns `None` for empty lines
- Returns `None` if fewer than 4 components are present
- Returns `None` if the log level is not INFO, WARNING, or ERROR

---

### `read_and_analyze_log(filename)`

Reads a log file and performs a complete analysis of all entries.

**Parameters:**
- `filename` (str): Path to the log file to analyze

**Returns:**
- `dict`: Contains the following keys:
  - `'total_entries'` (int): Total count of valid log entries
  - `'info_count'` (int): Count of INFO level entries
  - `'warning_count'` (int): Count of WARNING level entries
  - `'error_count'` (int): Count of ERROR level entries
  - `'error_messages'` (list): List of dictionaries containing error timestamps and messages
  - `'malformed_lines'` (int): Count of lines that couldn't be parsed
- `None`: If the file is not found or an error occurs during reading

**Error Handling:**
- Prints an error message and returns `None` if the file is not found
- Catches and reports any exceptions that occur during file reading
- Handles malformed lines gracefully without stopping analysis

---

### `display_analysis_results(results)`

Displays the log analysis results in a formatted, readable manner.

**Parameters:**
- `results` (dict): The dictionary returned by `read_and_analyze_log()`

**Returns:**
- `0`: On successful display (or `None` if results is `None`)

**Output:**
- Prints a formatted report to the console
- Shows summary statistics for all log levels
- Lists individual error messages with timestamps if errors are present

---

### `main()`

The main entry point for the script. Orchestrates the log reading, analysis, and display workflow.

**Workflow:**
1. Sets the log filename (default: `'app.log'`)
2. Prints startup messages
3. Calls `read_and_analyze_log()` to process the file
4. Calls `display_analysis_results()` to show the report
5. Prints completion or failure message

---

## Error Handling

The Log Analyzer implements comprehensive error handling:

### File Errors

- **FileNotFoundError**: When the specified log file doesn't exist
  - Message: `Error: The file '{filename}' was not found.`
  - Returns: `None`

- **General Exceptions**: Any other errors during file reading
  - Message: `An Error occurred while reading the file: {error}`
  - Returns: `None`

### Data Validation Errors

- **Empty Lines**: Silently skipped (no error message)
- **Malformed Lines**: Counted and reported, but don't stop processing
- **Invalid Log Levels**: Lines with levels other than INFO, WARNING, or ERROR are treated as malformed

### Graceful Degradation

- The script continues processing even if some lines are malformed
- Partial results are still available and displayed
- Users are informed of the malformed line count

## Example

### Sample Log File (`app.log`)

```
2024-08-26 09:15:32 INFO Application started
2024-08-26 09:16:01 INFO Database connection established
2024-08-26 09:17:45 WARNING CPU usage at 85%
2024-08-26 09:18:30 ERROR Failed to fetch user data
2024-08-26 09:19:15 INFO Retry initiated
2024-08-26 09:20:00 ERROR Connection timeout
This is a malformed line
2024-08-26 09:21:30 WARNING Low memory warning
2024-08-26 09:22:45 INFO Cleanup completed
```

### Running the Analyzer

```bash
$ python Log_Analyzer.py
Starting Log Analyzer
Reading File: app.log

==================================================
            Log Analysis Results
==================================================

Total Entries: 8

INFO Entries: 4

WARNING Entries: 2

ERROR Entries: 2

Malformed Lines: 1

==================================================
            Error Messages
==================================================

Error Messages:

1. [2024-08-26 09:18:30]
   Failed to fetch user data

2. [2024-08-26 09:20:00]
   Connection timeout

==================================================

The Analysis is Completed.
```

## Author

**Optional by Shubham Vinod Vishwakarma**

This script prevents the `main()` function from running automatically when imported as a module into another Python file by using the `if __name__ == "__main__":` guard.

---

## License

[Specify your license here, e.g., MIT, GPL, etc.]

## Contributing

[Add contribution guidelines if applicable]

## Support

[Add contact or support information if needed]
