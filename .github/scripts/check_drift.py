#!/usr/bin/env python3
"""Fail when authenticity-check's docs drift out of agreement with each other.

Checks versions, catalog and example counts, eval structure, what every tool
adapter must mention, the vendored criteria headers and sync stamps, file
references, the README layout and anchors, and house style. Adapted from
humanizer's drift check. Repository tooling, not part of the skill. Standard
library only; run from anywhere inside the repository:

    python3 .github/scripts/check_drift.py
"""
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
).stdout.strip()
os.chdir(ROOT)
TRACKED = subprocess.run(
    ["git", "ls-files"], capture_output=True, text=True, check=True
).stdout.splitlines()

ADAPTER_HEADING = "# authenticity-check ("
# Every adapter restates the method in its own words, so instead of one shared
# body each must mention the entry point, the references the method loads,
# the output sections, and the humanizer split.
ADAPTER_MENTIONS = (
    "SKILL.md",
    "references/tell-patterns.md",
    "references/do-not-flag.md",
    "references/voice-matching.md",
    "references/provenance-signals.md",
    "Provenance signals",
    "Flagged spans",
    "Reads as human",
    "Score basis",
    "Caveats",
    "Next step",
    "humanizer",
)
VENDORED = (
    "references/tell-patterns.md",
    "references/do-not-flag.md",
    "references/voice-matching.md",
)
SENTINEL = "VENDORED FILE - SYNCED COPY, NOT THE SOURCE OF TRUTH"
STAMP = re.compile(r"^Last synced: (\d{4}-\d{2}-\d{2}) from humanizer @ ([0-9a-f]{7,40})$", re.M)
LAYOUT_EXEMPT = {"README.md", "LICENSE", ".gitignore"}
# Maintainer workflow state, not part of the skill.
LAYOUT_EXEMPT_PREFIXES = (".godpowers/",)
SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
WORDS = (
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty"
).split()
# Built from code points so this file stays ASCII and cannot trip its own check.
DASH = re.compile("[%s%s]" % (chr(0x2013), chr(0x2014)))
EMOJI = re.compile("[%s-%s%s-%s%s-%s]" % (
    chr(0x2600), chr(0x27BF), chr(0x2B00), chr(0x2BFF), chr(0x1F000), chr(0x1FAFF)))

TEXT = {}
for _path in TRACKED:
    try:
        with open(_path, encoding="utf-8") as _f:
            TEXT[_path] = _f.read()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        pass

problems = []


def report(path, line, message):
    problems.append((path, line, message))


def line_of(path, index):
    return TEXT[path].count("\n", 0, index) + 1


def number(word):
    word = word.lower()
    if word.isdigit():
        return int(word)
    return WORDS.index(word) if word in WORDS else None


def frontmatter(path):
    match = re.match(r"\A---\n(.*?)\n---\n", TEXT[path], re.S)
    return match.group(1) if match else None


def strip_frontmatter(text):
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)


def normalize(text):
    return " ".join(text.split())


def parse_frontmatter(block):
    """Top-level keys of a simple YAML mapping, with block scalars folded."""
    keys, values = [], {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", lines[i])
        i += 1
        if not match:
            continue
        key, rest = match.groups()
        nested = []
        while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
            nested.append(lines[i])
            i += 1
        keys.append(key)
        if rest in (">", ">-", ">+", "|", "|-", "|+"):
            values[key] = " ".join(l.strip() for l in nested if l.strip())
        elif rest:
            values[key] = rest.strip().strip("'\"")
        else:
            values[key] = "\n".join(nested)
    return keys, values


def check_skill_frontmatter():
    block = frontmatter("SKILL.md")
    if block is None:
        report("SKILL.md", 1, "missing YAML frontmatter")
        return None
    keys, values = parse_frontmatter(block)
    for key in keys:
        if key not in SPEC_KEYS:
            report("SKILL.md", 1, f"frontmatter key '{key}' is not in the Agent Skills spec")
    name = values.get("name", "")
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        report("SKILL.md", 1, f"name '{name}' must be 1-64 lowercase letters, digits, and single hyphens")
    description = values.get("description", "")
    if not 1 <= len(description) <= 1024:
        report("SKILL.md", 1, f"description is {len(description)} characters; the spec allows 1-1024")
    if len(values.get("compatibility", "")) > 500:
        report("SKILL.md", 1, "compatibility is over the spec's 500-character limit")
    match = re.search(r"^\s+version:\s*['\"]?(\d[\w.-]*)", values.get("metadata", ""), re.M)
    if not match:
        report("SKILL.md", 1, "metadata.version is missing")
        return None
    return match.group(1)


def check_versions(version):
    readme, log = "README.md", "CHANGELOG.md"
    sources = [
        (readme, re.search(r"badge/version-(\d[\w.]*?)-\w+\)", TEXT[readme]), "README version badge"),
        (log, re.search(r"^## \[(\d[\w.]*)\]", TEXT[log], re.M), "latest CHANGELOG release"),
        (log, re.search(r"^\[(\d[\w.]*)\]: \S+", TEXT[log], re.M), "first CHANGELOG version link"),
    ]
    for path, match, label in sources:
        if not match:
            report(path, 1, f"cannot find the {label}")
        elif match.group(1) != version:
            report(path, line_of(path, match.start()), f"{label} says {match.group(1)}, SKILL.md says {version}")
    link = sources[2][1]
    if link and not link.group(0).endswith(f"v{version}"):
        report(log, line_of(log, link.start()), f"the {version} link should point at tag v{version}")


def check_catalog():
    path = "references/tell-patterns.md"
    text = TEXT[path]
    heads = [(int(m.group(1)), m.group(2).strip(), m.start())
             for m in re.finditer(r"^### (\d+)\. (.+)$", text, re.M)]
    numbers = [n for n, _, _ in heads]
    if numbers != list(range(1, len(numbers) + 1)):
        report(path, 1, f"pattern headings must be numbered 1-{len(numbers)} in order")
    toc = re.search(r"^## Table of contents\n(.*?)^---$", text, re.M | re.S)
    if not toc:
        report(path, 1, "no '## Table of contents' section ending at a '---' line")
    else:
        entries = {int(n): title.strip() for n, title in re.findall(r"^(\d+)\. (.+)$", toc.group(1), re.M)}
        for n, title, index in heads:
            if entries.get(n) != title:
                report(path, line_of(path, index), f"table of contents entry {n} reads '{entries.get(n)}'")
        for n in sorted(set(entries) - set(numbers)):
            report(path, line_of(path, toc.start()), f"table of contents lists pattern {n}, which has no heading")
    families = len(re.findall(r"^## Family [A-Z]:", text, re.M))
    return len(heads), families


def check_examples():
    path = "references/examples.md"
    numbers = [int(n) for n in re.findall(r"^## Example (\d+):", TEXT[path], re.M)]
    if numbers != list(range(1, len(numbers) + 1)):
        report(path, 1, f"examples must be numbered 1-{len(numbers)} in order")
    return len(numbers)


def check_evals():
    path = "evals/evals.json"
    try:
        evals = json.loads(TEXT[path]).get("evals", [])
    except json.JSONDecodeError as error:
        report(path, error.lineno, f"invalid JSON: {error.msg}")
        return 0
    ids = [case.get("id") for case in evals]
    if ids != list(range(1, len(evals) + 1)):
        report(path, 1, f"eval ids must run 1-{len(evals)} in order")
    required = {"id", "prompt", "expected_output", "files", "expectations"}
    for case in evals:
        missing = required - set(case)
        if missing:
            report(path, 1, f"eval {case.get('id')} is missing {', '.join(sorted(missing))}")
        if not case.get("expectations"):
            report(path, 1, f"eval {case.get('id')} has no expectations")
        for name in case.get("files", []):
            if name not in TEXT:
                report(path, 1, f"eval {case.get('id')} needs missing file {name}")
    return len(evals)


def check_counts(counts):
    patterns, families, examples, evals = counts
    for path, text in TEXT.items():
        if path == "CHANGELOG.md":
            continue
        for match in re.finditer(r"\b(\d+)[- ]patterns?\b", text):
            if int(match.group(1)) != patterns:
                report(path, line_of(path, match.start()), f"says '{match.group(0)}'; the catalog has {patterns}")
        for match in re.finditer(r"\b(\w+) families\b", text):
            n = number(match.group(1))
            if n is not None and n != families:
                report(path, line_of(path, match.start()), f"says '{match.group(0)}'; the catalog has {families}")
        example_phrases = (
            r"\b(\w+) (?:full )?worked (?:end-to-end |diagnostic )?(?:runs|examples)\b",
            r"\b(\w+) full runs\b",
        )
        for phrase in example_phrases:
            for match in re.finditer(phrase, text, re.I):
                n = number(match.group(1))
                if n is not None and n != examples:
                    report(path, line_of(path, match.start()), f"says '{match.group(0)}'; examples.md has {examples}")
        for match in re.finditer(r"\b(\w+) verification cases\b", text):
            n = number(match.group(1))
            if n is not None and n != evals:
                report(path, line_of(path, match.start()), f"says '{match.group(0)}'; evals.json has {evals}")


def check_tools():
    readme = TEXT["README.md"]
    badge = re.search(r"works%20with-(\d+)%20", readme)
    section = re.search(r"^## Supported tools\n(.*?)(?=^## )", readme, re.M | re.S)
    if not badge or not section:
        report("README.md", 1, "cannot find the tools badge or the Supported tools section")
        return 0
    rows = [l for l in section.group(1).splitlines()
            if l.startswith("|") and not re.match(r"^\|\s*(Tool\b|-)", l)]
    if len(rows) != int(badge.group(1)):
        report("README.md", line_of("README.md", badge.start()),
               f"badge says {badge.group(1)} tools, the Supported tools table has {len(rows)} rows")
    return len(rows)


def check_adapters():
    adapters = sorted(
        path for path, text in TEXT.items()
        if strip_frontmatter(text).lstrip().startswith(ADAPTER_HEADING)
    )
    for path in adapters:
        body = normalize(strip_frontmatter(TEXT[path]))
        for phrase in ADAPTER_MENTIONS:
            if phrase not in body:
                report(path, 1, f"adapter never mentions {phrase}")
        block = frontmatter(path)
        if block is None:
            continue
        for offset, line in enumerate(block.splitlines(), 2):
            if not re.match(r"^[A-Za-z][\w-]*:( .*)?$", line):
                report(path, offset, f"frontmatter line is not 'key: value': {line}")
    return len(adapters)


def check_vendored():
    stamps = {}
    for path in VENDORED:
        text = TEXT.get(path)
        if text is None:
            report("README.md", 1, f"vendored file {path} is missing")
            continue
        header = text.split("\n-->\n", 1)[0] if text.startswith("<!--\n") else ""
        if SENTINEL not in header:
            report(path, 1, "missing the vendored-file header")
            continue
        if f"Canonical upstream: the `humanizer` repo, {path}" not in header:
            report(path, 1, f"header must name the humanizer repo's {path} as canonical upstream")
        match = STAMP.search(header)
        if not match:
            report(path, 1, "header has no 'Last synced: YYYY-MM-DD from humanizer @ <commit>' stamp")
            continue
        stamps[path] = match.groups()
    if len(set(stamps.values())) > 1:
        detail = ", ".join(f"{path} {date} @ {commit}" for path, (date, commit) in sorted(stamps.items()))
        report(VENDORED[0], 1, f"vendored files carry different sync stamps: {detail}")
        return None
    if not stamps:
        return None
    date, commit = next(iter(stamps.values()))
    readme = TEXT["README.md"]
    expected = f"Last synced {date} from humanizer commit `{commit}`"
    if expected not in normalize(readme):
        found = re.search(r"Last synced", readme)
        line = line_of("README.md", found.start()) if found else 1
        report("README.md", line, f"README sync stamp should read '{expected}'")
    return f"{date} @ {commit}"


def check_references():
    for path in TRACKED:
        if path.startswith("references/") and f"`{path}`" not in TEXT["SKILL.md"]:
            report("SKILL.md", 1, f"never mentions {path}, so the skill cannot load it")
    for path, text in TEXT.items():
        if path == "CHANGELOG.md":
            continue
        for match in re.finditer(r"`((?:references|evals|\.cursor|\.continue|\.github)/[^`\s*]+)`", text):
            ref = match.group(1)
            if not ref.endswith("/") and ref not in TEXT:
                report(path, line_of(path, match.start()), f"mentions missing file {ref}")


def check_layout():
    readme = TEXT["README.md"]
    block = re.search(r"^## Layout\n+```\n(.*?)\n```", readme, re.M | re.S)
    if not block:
        report("README.md", 1, "cannot find the Layout code block")
        return
    start = line_of("README.md", block.start(1))
    listed = {}
    for offset, line in enumerate(block.group(1).splitlines()):
        if line.strip():
            listed[line.split()[0]] = start + offset
    for path, line in listed.items():
        if path not in TEXT:
            report("README.md", line, f"Layout lists {path}, which does not exist")
    for path in TRACKED:
        if path in listed or path in LAYOUT_EXEMPT or path.startswith(LAYOUT_EXEMPT_PREFIXES):
            continue
        report("README.md", start, f"Layout does not list {path}")


def slug(heading):
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def check_anchors():
    for path, text in TEXT.items():
        if not path.endswith(".md"):
            continue
        anchors = {slug(h) for h in re.findall(r"^#+ (.+)$", text, re.M)}
        for match in re.finditer(r"\]\(#([^)\s]+)\)", text):
            if match.group(1) not in anchors:
                report(path, line_of(path, match.start()), f"link to #{match.group(1)} has no matching heading")


def check_style():
    for path, text in TEXT.items():
        for number_, line in enumerate(text.splitlines(), 1):
            if DASH.search(line):
                report(path, number_, "em or en dash; use a comma, colon, parentheses, or a hyphen")
            if EMOJI.search(line):
                report(path, number_, "emoji; use words or an icon instead")
            if line != line.rstrip(" \t"):
                report(path, number_, "trailing whitespace")
        if text and not text.endswith("\n"):
            report(path, text.count("\n") + 1, "missing final newline")
        if not path.endswith((".md", ".mdc")):
            continue
        in_code = False
        body_start = len(text) - len(strip_frontmatter(text))
        first_line = text.count("\n", 0, body_start) + 1
        for number_, line in enumerate(text.splitlines(), 1):
            if number_ < first_line:
                continue
            if line.startswith("```"):
                in_code = not in_code
                continue
            if in_code or line.startswith(("|", "![", "[![")):
                continue
            # A link reference definition is one unbreakable URL.
            if re.match(r"^\[[^\]]+\]: \S+$", line):
                continue
            if len(line) > 80:
                report(path, number_, f"{len(line)} columns; wrap prose at 80")


def escape(value, prop=False):
    value = value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return value.replace(":", "%3A").replace(",", "%2C") if prop else value


def main():
    version = check_skill_frontmatter()
    if version:
        check_versions(version)
    patterns, families = check_catalog()
    examples = check_examples()
    evals = check_evals()
    check_counts((patterns, families, examples, evals))
    tools = check_tools()
    adapters = check_adapters()
    stamp = check_vendored()
    check_references()
    check_layout()
    check_anchors()
    check_style()

    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for path, line, message in sorted(set(problems)):
        if in_actions:
            print(f"::error file={escape(path, True)},line={line}::{escape(message)}")
        else:
            print(f"{path}:{line}: {message}")
    if problems:
        print(f"\ndrift check failed: {len(set(problems))} problem(s)")
        return 1
    print(f"drift check passed: version {version}, {patterns} patterns in {families} families, "
          f"{examples} examples, {evals} evals, {tools} tools, {adapters} adapters, "
          f"criteria synced {stamp}, {len(TRACKED)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
