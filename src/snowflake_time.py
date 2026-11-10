#!/usr/bin/env python3
"""Decode the posting time of X (Twitter) posts from their status IDs.

Purpose: X shows post times in the viewer's own time zone, at minute precision, and the
reviews here need exact UTC times to compare a hash-commitment post with Arlo's round start
(when the seed was entered and the sample drawn). Every status ID is a "snowflake" whose top
bits are milliseconds since 2010-11-04T01:42:54.657Z, so the ID alone gives the UTC time.

Usage:
    python3 -I src/snowflake_time.py URL_OR_ID [URL_OR_ID ...] [--since 2026-05-28T15:49:15Z]

--since prints each post's offset from a reference time (e.g. Arlo's Round 1 start).
"""
import re
import sys
from datetime import datetime, timezone

TWITTER_EPOCH_MS = 1288834974657


def post_time(id_or_url: str) -> datetime:
    m = re.search(r"(\d{15,20})", id_or_url)
    if not m:
        raise ValueError(f"no status id in {id_or_url!r}")
    ms = (int(m.group(1)) >> 22) + TWITTER_EPOCH_MS
    return datetime.fromtimestamp(ms / 1000, timezone.utc)


def main(argv):
    since = None
    if "--since" in argv:
        i = argv.index("--since")
        since = datetime.fromisoformat(argv[i + 1].replace("Z", "+00:00"))
        argv = argv[:i] + argv[i + 2:]
    for arg in argv:
        t = post_time(arg)
        line = f"{t.isoformat(timespec='milliseconds').replace('+00:00', 'Z')}  {arg}"
        if since:
            d = (t - since).total_seconds()
            line += f"  ({'+' if d >= 0 else '-'}{int(abs(d)) // 60}m{abs(d) % 60:06.3f}s vs --since)"
        print(line)


if __name__ == "__main__":
    main(sys.argv[1:])
