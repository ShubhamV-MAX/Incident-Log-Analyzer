def log_line_phraser(line):
    """

    Phrase a single log line and Extract its Components.
    Expected Format: YYYY-MM-DD HH:MM:SS LOG_LEVEL Message.....

    Arguments:
        line (str): A single line from the log file.

    Return:
        dict: Contains 'date', 'time', 'level', 'message' If valid,
              else return None.
    
    """

    # Strip the line to remove leading/trailing whitespace
    line = line.strip()

    # Handle empty lines
    if not line:
        return None

    # Split the line into components 
    parts = line.split()

    # Check if the line has at least 4 parts (date, time, level, message)
    if len(parts) < 4:
        return None

    # Extract the components
    date = parts[0]
    time = parts[1]
    level = parts[2]

    # Valid log levels
    if level not in ['INFO', 'WARNING', 'ERROR']:
        return None

    # Extract the message by joining the remaining parts
    message = ' '.join(parts[3:]) 

    # Return the parsed components
    return {
        'date': date,
        'time': time,
        'level': level,
        'message': message
    }

def read_and_analyze_log(filename):
    """

    Read a log file and analyze all Entries.

    Arguments:
        filename (str): The Path to the log file.

    Return:
        dict: A dictionary containing the analyzed log entries.

    """

    # Initialize counters and storage for log entries.
    total_entries = 0
    info_count = 0
    warning_count = 0
    error_count = 0
    error_messages = []
    malformed_lines = 0

    try:
        # Open and Read the log file.
        with open(filename, 'r') as file:
            for line in file:
                phrase = log_line_phraser(line)

                # Handling malformed lines.
                if phrase is None:
                    malformed_lines += 1
                    continue

                # Increment total entries.
                total_entries += 1

                # Count log levels and store error messages.
                if phrase['level'] == 'INFO':
                    info_count += 1 
                elif phrase['level'] == 'WARNING':
                    warning_count += 1
                elif phrase['level'] == 'ERROR':
                    error_count += 1
                    error_messages.append({
                        'timestamp': f"{phrase['date']} {phrase['time']}",
                        'message': phrase['message']
                    })

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except Exception as e:
        print(f"An Error occurred while reading the file: {e}")
        return None

    # Return the results as Directory.
    return {
        'total_entries': total_entries,
        'info_count': info_count,
        'warning_count': warning_count,
        'error_count': error_count,
        'error_messages': error_messages,
        'malformed_lines': malformed_lines
    }

def display_analysis_results(results):
    """

    Display the analysis results in a readable format.

    Arguments:
        results (dict): The dictionary containing the analyzed log entries.

    Return:
        0    

    """

    if results is None:
        return

    print(f"\n" + "="*50)
    print(" "*12 + "Log Analysis Results")
    print("="*50)
    print(f"\nTotal Entries: {results['total_entries']}")
    print(f"\nINFO Entries: {results['info_count']}")
    print(f"\nWARNING Entries: {results['warning_count']}")
    print(f"\nERROR Entries: {results['error_count']}")

    if results['malformed_lines'] > 0:
        print(f"\nMalformed Lines: {results['malformed_lines']}")

    # Print the Errors messages if any.
    if results['error_count'] > 0:
        print("\n" + "="*50)
        print(f" "*12 + "Error Messages")
        print("="*50)
        print("\nError Messages:")
        for idx, error in enumerate(results['error_messages'], start=1):
            print(f"\n{idx}. [{error['timestamp']}]")
            print(f"   {error['message']}")

    print("\n" + "="*50 + "\n")

    return 0

def main():
    """

    Main Function to run the log analyzer.

    """
    filename = 'app.log' 

    print("Starting Log Analyzer")
    print(f"Reading File: {filename}")

    # Analyze the log file.
    results = read_and_analyze_log(filename)

    # Display the result.
    if results is not None:
        display_analysis_results(results)
        print("\nThe Analysis is Completed.")
    else:
        print("\nAnalysis Failed. Check your log file.")

main()
