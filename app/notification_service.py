import subprocess


def notify(title: str, message: str):
    """Send a macOS desktop notification."""

    # Escape characters that could break AppleScript strings
    safe_title = (
        title
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )

    safe_message = (
        message
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )

    script = (
        f'display notification "{safe_message}" '
        f'with title "{safe_title}"'
    )

    result = subprocess.run(
        [
            "osascript",
            "-e",
            script,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print(
            "Notification warning:",
            result.stderr.strip(),
        )