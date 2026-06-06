# Analyze log
def analyze_log(log_file, level_filter):
    stats = {
        "errors": 0,
        "total_lines": 0,
        "problem_lines": [],
        "warnings": 0,
        "critical": 0,
    }

    with open(log_file) as log:
        for line in log:
            stats["total_lines"] += 1
            if level_filter is not None and level_filter not in line:
                continue
            if "CRITICAL" in line:
                stats["problem_lines"].append(line.strip())
                stats["critical"] += 1
            elif "ERROR" in line:
                stats["problem_lines"].append(line.strip())
                stats["errors"] += 1
            elif "WARNING" in line:
                stats["problem_lines"].append(line.strip())
                stats["warnings"] += 1

    return stats