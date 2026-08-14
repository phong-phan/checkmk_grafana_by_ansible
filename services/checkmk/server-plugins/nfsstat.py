from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
    Metric,
)

def parse_nfsstat(string_table):
    """
    Parses the 'nfsstat -s' output.
    Focuses specifically on error-related server stats.
    """
    # Updated target list to your specific requirements
    targets = ['badcalls', 'badfmt', 'badauth', 'badclnt', 'calls']
    parsed = {}
    current_headers = None

    for line in string_table:
        line_str = " ".join(line).strip()

        # Skip empty lines or client-side sections
        if not line_str or "Client" in line_str:
            current_headers = None
            continue

        if "Server" in line_str:
            continue

        # Detect header lines (containing letters)
        if any(c.isalpha() for c in line_str):
            current_headers = [h.strip(':').lower() for h in line_str.split()]
            continue

        # Process data lines (containing numbers)
        if current_headers:
            values = [v for v in line_str.split() if '%' not in v]
            for i, val in enumerate(values):
                if i < len(current_headers):
                    key = current_headers[i]
                    if key in targets:
                        try:
                            parsed[key] = int(val)
                        except ValueError:
                            continue
    return parsed

def discover_nfsstat(section):
    if section:
        yield Service()

def check_nfsstat(section):
    """
    Evaluates the health based on bad calls.
    """
    # Define our specific error targets
    error_keys = ['badcalls', 'badfmt', 'badauth', 'badclnt']

    # Get total calls for context
    total_calls = section.get('calls', 0)

    # Check if any errors exist and determine state
    worst_state = State.OK
    details = []
    summary_parts = []

    for key in error_keys:
        val = section.get(key, 0)
        details.append(f"{key}: {val}")
        yield Metric(name=key, value=float(val))

        # Simple logic: If any bad metrics are > 0, we flag it as Warning
        # You can adjust these thresholds as needed
        if val > 0:
            summary_parts.append(f"{key}: {val}")
            worst_state = State.WARN

    summary = ", ".join(summary_parts) if summary_parts else "No server errors"

    yield Result(
        state=worst_state,
        summary=f"{summary} (Total Calls: {total_calls})",
        details="\n".join(details)
    )

# --- REGISTRATION ---

agent_section_nfsstat = AgentSection(
    name="nfsstat",
    parse_function=parse_nfsstat,
)

check_plugin_nfsstat = CheckPlugin(
    name="nfsstat",
    service_name="NFS Server Errors",
    discovery_function=discover_nfsstat,
    check_function=check_nfsstat,
)
