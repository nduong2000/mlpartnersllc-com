#!/usr/bin/env python3
"""Contact form endpoint for mlpartnersllc.com.

Listens on 127.0.0.1:8826 behind OpenResty (location = /api/contact).
Accepts JSON {name, email, message, website} and relays it to
nduong@mlpartnersllc.com through AWS SES (us-east-1). The `website`
field is a honeypot: bots that fill it get a fake success response.
"""

import json
import re
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import boto3

LISTEN = ("127.0.0.1", 8826)
REGION = "us-east-1"
TO_ADDRESS = "nduong@mlpartnersllc.com"
FROM_ADDRESS = "ML Partners Contact <nduong@mlpartnersllc.com>"
MAX_BODY = 32 * 1024
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

# Rate limits: per-IP 5/hour, global 50/day
PER_IP_LIMIT, PER_IP_WINDOW = 5, 3600
GLOBAL_LIMIT, GLOBAL_WINDOW = 50, 86400

ses = boto3.client("sesv2", region_name=REGION)
ip_hits = defaultdict(deque)
global_hits = deque()


def rate_ok(ip):
    now = time.time()
    while global_hits and now - global_hits[0] > GLOBAL_WINDOW:
        global_hits.popleft()
    hits = ip_hits[ip]
    while hits and now - hits[0] > PER_IP_WINDOW:
        hits.popleft()
    if len(hits) >= PER_IP_LIMIT or len(global_hits) >= GLOBAL_LIMIT:
        return False
    hits.append(now)
    global_hits.append(now)
    return True


class Handler(BaseHTTPRequestHandler):
    server_version = "contact-api"

    def reply(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/contact":
            return self.reply(404, {"ok": False, "error": "not found"})

        length = int(self.headers.get("Content-Length") or 0)
        if not 0 < length <= MAX_BODY:
            return self.reply(413, {"ok": False, "error": "payload too large"})

        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return self.reply(400, {"ok": False, "error": "invalid JSON"})

        # Honeypot: pretend success so bots learn nothing
        if (data.get("website") or "").strip():
            return self.reply(200, {"ok": True})

        name = (data.get("name") or "").strip()[:100]
        email = (data.get("email") or "").strip()[:200]
        message = (data.get("message") or "").strip()[:5000]

        if len(name) < 2:
            return self.reply(400, {"ok": False, "error": "Please enter your name."})
        if not EMAIL_RE.match(email):
            return self.reply(400, {"ok": False, "error": "Please enter a valid email address."})
        if len(message) < 10:
            return self.reply(400, {"ok": False, "error": "Message is too short."})

        ip = self.headers.get("X-Real-IP", self.client_address[0])
        if not rate_ok(ip):
            return self.reply(429, {"ok": False, "error": "Too many messages — please try again later."})

        body = (
            f"Contact form submission — mlpartnersllc.com\n"
            f"{'-' * 44}\n"
            f"Name:  {name}\n"
            f"Email: {email}\n"
            f"IP:    {ip}\n"
            f"Time:  {time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"{'-' * 44}\n\n"
            f"{message}\n"
        )

        try:
            ses.send_email(
                FromEmailAddress=FROM_ADDRESS,
                Destination={"ToAddresses": [TO_ADDRESS]},
                ReplyToAddresses=[email],
                Content={
                    "Simple": {
                        "Subject": {"Data": f"[mlpartnersllc.com] Contact: {name}"},
                        "Body": {"Text": {"Data": body}},
                    }
                },
            )
        except Exception as exc:  # noqa: BLE001 — report any SES failure the same way
            self.log_message("SES error: %s", exc)
            return self.reply(502, {"ok": False, "error": "Could not send right now — please try again later."})

        self.log_message("sent contact mail from %s <%s> (ip %s)", name, email, ip)
        return self.reply(200, {"ok": True})

    def do_GET(self):
        # Health check
        if self.path == "/api/contact/health":
            return self.reply(200, {"ok": True})
        return self.reply(404, {"ok": False, "error": "not found"})


if __name__ == "__main__":
    print(f"contact-api listening on {LISTEN[0]}:{LISTEN[1]}", flush=True)
    ThreadingHTTPServer(LISTEN, Handler).serve_forever()
