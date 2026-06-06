# Import argparse module for working with command-line arguments
from openai import OpenAI
from analyzer import analyze_log

import argparse
parser = argparse.ArgumentParser(description="Analyze log files and create a report")
parser.add_argument("log_file", help="Path to log file")
parser.add_argument("--output", default="report.md", help="Path to report file")
parser.add_argument("--last", type=int, default=3, help="How many last problems to show")
parser.add_argument("--level", choices=["ERROR", "WARNING", "CRITICAL"], help="Filter problems by level")
parser.add_argument("--ai", action="store_true", help="Explain found problems using AI")

args = parser.parse_args()

# Define args
log_file = args.log_file
report_file = args.output

last_count = args.last
level_filter = args.level
use_ai = args.ai

if last_count <= 0:
    print("--last must be greater than 0")
    exit()

### Functions ###

#AI
def explain_with_ai(stats, last_count, level_filter):
    client = OpenAI()

    problems = stats["problem_lines"][-last_count:]

    if level_filter is None:
        level_text = "ALL"
    else:
        level_text = level_filter

    prompt = f"""
You are helping a beginner DevOps engineer understand log errors.

Log level filter: {level_text}

Explain these log lines:
{chr(10).join(problems)}

Give:
1. Short summary
2. Possible causes
3. First 3 checks to do
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    return response.output_text

# Print summary to terminal
def print_summary(stats, level_filter):
    print("--- Summary ---")
    if level_filter is None:
        print("Level filter: ALL")
    else:
        print(f"Level filter: {level_filter}")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Total problems: {len(stats['problem_lines'])}")
    print(f"Total errors: {stats['errors']}")
    print(f"Total warnings: {stats['warnings']}")
    print(f"Total critical: {stats['critical']}")

# Write summary to report file
def write_summary(report, stats, level_filter):
    report.write("\n")
    report.write("## Summary\n")
    if level_filter is None:
        report.write("Level filter: ALL\n")
    else:
        report.write(f"Level filter: {level_filter}\n")
    report.write(f"Total lines: {stats['total_lines']}\n")
    report.write(f"Total problems: {len(stats['problem_lines'])}\n")
    report.write(f"Total errors: {stats['errors']}\n")
    report.write(f"Total warnings: {stats['warnings']}\n")
    report.write(f"Total critical: {stats['critical']}\n")

# Write problems to report file
def write_problems(report, stats, last_count, level_filter):
    if stats["problem_lines"]:
        if level_filter is None:
            report.write(f"## Last {last_count} problems found:\n")
        else:
            report.write(f"## Last {last_count} {level_filter} problems found:\n")

        for problem in stats["problem_lines"][-last_count:]:
            report.write(problem)
            report.write("\n")
    else:
        report.write("No problems found.\n")
        report.write("\n")


# Print problems to terminal
def print_problems(stats, last_count, level_filter):
    if stats["problem_lines"]:
        if level_filter is None:
            print(f"Last {last_count} problems found:")
        else:
            print(f"Last {last_count} {level_filter} problems found:")
        for problem in stats["problem_lines"][-last_count:]:
            print(problem)
    else:
        print("No problems found.")

### Main program ###

# Open logs, if exists
try:
    stats = analyze_log(log_file, level_filter)
except FileNotFoundError:
    print(f"File not found: {log_file}")
    exit()

# Check if log is not empty
if stats["total_lines"] == 0:
    print(f"Log file is empty: {log_file}")
    exit()

# Check if there are any problems in log
print_problems(stats, last_count, level_filter)

print()

# Print summary
print_summary(stats, level_filter)

# Use AI
if use_ai and stats["problem_lines"]:
    try:
        ai_explanation = explain_with_ai(stats, last_count, level_filter)

        print()
        print("--- AI Explanation ---")
        print(ai_explanation)
    except Exception as error:
        print()
        print(f"AI explanation failed: {error}")
elif use_ai:
    print()
    print("AI explanation skipped: no problems found.")

# Write in report file
with open(report_file, "w") as report:
    report.write("# Log Doctor Report\n")
    report.write("\n")
    write_problems(report, stats, last_count, level_filter)
    write_summary(report, stats, level_filter)

print()
# Info for user
print(f"Report saved to: {report_file}")