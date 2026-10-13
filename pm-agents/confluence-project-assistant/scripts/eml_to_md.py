#!/usr/bin/env python3
"""Convert an .eml email thread into a readable Markdown file.

Usage: eml_to_md.py <input.eml> <output_dir> <attachments_dir>
Writes <output_dir>/<YYYY-MM-DD>-<subject-slug>.md and prints its path.
Saves attachments to <attachments_dir>/<YYYY-MM-DD>-<subject-slug>/ (documents
always; inline images only when >= 100 KB) and prints each saved path.
"""
import email
import html
import re
import sys
import unicodedata
from email import policy
from email.utils import parsedate_to_datetime
from pathlib import Path

PREFIX = re.compile(r"^\s*((re|fw|fwd|tr|trả lời|chuyển tiếp)\s*:\s*)+", re.I)
INLINE_NOISE = re.compile(r"^\[(A white background|Description|cid:)[^\]]*\]\s*$", re.I)


def slugify(text):
    text = unicodedata.normalize("NFKD", text.replace("đ", "d").replace("Đ", "D"))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80] or "email"


def html_to_text(src):
    src = re.sub(r"(?is)<(script|style).*?</\1>", "", src)
    src = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|h\d)>", "\n", src)
    src = re.sub(r"(?s)<[^>]+>", "", src)
    return html.unescape(src)


def clean(text):
    lines = [l.rstrip() for l in text.replace("\r\n", "\n").split("\n")]
    lines = [l for l in lines if not INLINE_NOISE.match(l)]
    out = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def main(src, out_dir, att_dir):
    msg = email.message_from_binary_file(open(src, "rb"), policy=policy.default)
    subject = str(msg["Subject"] or "(no subject)")
    try:
        date = parsedate_to_datetime(str(msg["Date"]))
        day, stamp = date.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d %H:%M %z")
    except (TypeError, ValueError):
        day, stamp = "unknown-date", str(msg["Date"] or "")

    body = msg.get_body(preferencelist=("plain", "html"))
    text = body.get_content() if body else ""
    if body is not None and body.get_content_type() == "text/html":
        text = html_to_text(text)

    title = PREFIX.sub("", subject).strip() or subject
    stem = f"{day}-{slugify(title)}"
    att_root = Path(att_dir) / stem
    attachments, skipped = [], 0
    for p in msg.walk():
        name = p.get_filename()
        data = p.get_payload(decode=True) or b""
        if not name or not data:
            continue
        is_image = p.get_content_type().startswith("image/")
        if is_image and (p.get_content_disposition() == "inline" or not p.get_content_disposition()) and len(data) < 100 * 1024:
            skipped += 1
            continue
        att_root.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r'[\/:*?"<>|]', "_", name)
        (att_root / safe).write_bytes(data)
        attachments.append(f"{safe} ({len(data) // 1024} KB) -> {stem}/{safe}")
        print(att_root / safe)

    lines = [f"# {title}", "", "| Field | Value |", "|---|---|"]
    for key in ("From", "To", "Cc"):
        if msg[key]:
            lines.append(f"| {key} | {str(msg[key]).replace('|', '/')} |")
    lines.append(f"| Date | {stamp} |")
    lines.append(f"| Subject | {subject.replace('|', '/')} |")
    lines.append(f"| Original file | {Path(src).name} |")
    if attachments:
        lines += ["", "## Attachments", "", "Saved under uncategorized/attachments/:", ""] + [f"- {a}" for a in attachments]
    if skipped:
        lines += ["", f"_{skipped} small inline image(s) (signature/logo graphics) not saved._"]
    lines += ["", "## Content", "", clean(text), ""]

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    target = out / f"{stem}.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
