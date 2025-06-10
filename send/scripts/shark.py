import pyshark
import json
import os
import sys


def extract_analytics_posts(pcapng_file):
    capture = pyshark.FileCapture(
        pcapng_file, display_filter='http.request.method == "POST"'
    )
    output = []

    for packet in capture:
        try:
            if "HTTP" not in packet:
                continue

            http_layer = packet.http
            if "analytics" not in http_layer.request_uri:
                continue

            if hasattr(http_layer, "file_data"):
                json_data = http_layer.file_data.binary_value.decode(
                    "utf-8", errors="ignore"
                )
                try:
                    parsed = json.loads(json_data)
                    output.append(parsed)
                except json.JSONDecodeError:
                    output.append({"raw": json_data})
        except Exception:
            continue

    capture.close()

    if output:
        output_file = os.path.splitext(pcapng_file)[0] + ".json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        print(f"[+] {pcapng_file}: saved {len(output)} entries to {output_file}")
    else:
        print(f"[-] {pcapng_file}: no matching POST requests found.")


def main(path):
    if os.path.isdir(path):
        files = [
            os.path.join(path, f) for f in os.listdir(path) if f.endswith(".pcapng")
        ]
        if not files:
            print("No .pcapng files found in the directory.")
            return
        for file in files:
            extract_analytics_posts(file)
    elif path.endswith(".pcapng") and os.path.isfile(path):
        extract_analytics_posts(path)
    else:
        print("Invalid path: must be a .pcapng file or a directory containing them.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_analytics.py <file_or_directory>")
        sys.exit(1)

    main(sys.argv[1])
