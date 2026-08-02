#!/usr/bin/env python3
"""Normalize and validate English-only CLARYEL project documentation."""

from __future__ import annotations

import argparse
import pathlib
import re
import unicodedata

EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
}
DOCUMENTATION_SUFFIXES = {".md", ".mdx", ".rst", ".adoc", ".txt"}
CYRILLIC = re.compile(r"[\u0400-\u04ff]")
RU_COMMENT = re.compile(r"^\s*(?:#|//|;|--)?\s*\[RU\]", re.IGNORECASE)
RU_BLOCK_START = re.compile(r"<!--\s*RU:BEGIN\s*-->", re.IGNORECASE)
RU_BLOCK_END = re.compile(r"<!--\s*RU:END\s*-->", re.IGNORECASE)
TABLE_SEPARATOR = re.compile(r"^\s*:?-{3,}:?\s*$")
TRANSLATION_SEPARATOR = re.compile(r"\s+/\s+")


def has_forbidden_letter(text: str) -> bool:
    return any(
        unicodedata.category(character).startswith("L")
        and not ("A" <= character <= "Z" or "a" <= character <= "z")
        for character in text
    )


def forbidden_ratio(text: str) -> float:
    letters = [character for character in text if character.isalpha()]
    if not letters:
        return 0.0
    forbidden = [
        character
        for character in letters
        if not ("A" <= character <= "Z" or "a" <= character <= "z")
    ]
    return len(forbidden) / len(letters)


def split_translation(text: str) -> tuple[str, str] | None:
    match = TRANSLATION_SEPARATOR.search(text)
    if not match:
        return None
    return text[: match.start()], text[match.end() :]


def clean_inline(text: str) -> str:
    if not has_forbidden_letter(text):
        return text.strip()
    translated = split_translation(text)
    if translated:
        left, right = translated
        if has_forbidden_letter(right) and not has_forbidden_letter(left):
            return left.rstrip()
    if forbidden_ratio(text) >= 0.15:
        return ""
    return " ".join(
        token
        for token in text.split()
        if not CYRILLIC.search(token) and not has_forbidden_letter(token)
    ).strip()


def clean_table_line(line: str) -> str:
    leading = line.startswith("|")
    trailing = line.rstrip().endswith("|")
    cells = line.strip().strip("|").split("|")
    cleaned_cells = [
        cell.strip() if TABLE_SEPARATOR.fullmatch(cell) else clean_inline(cell).strip()
        for cell in cells
    ]
    if not any(cell and not TABLE_SEPARATOR.fullmatch(cell) for cell in cleaned_cells):
        return ""
    rebuilt = " | ".join(cleaned_cells)
    if leading:
        rebuilt = "| " + rebuilt
    if trailing:
        rebuilt += " |"
    return rebuilt


def clean_mermaid_labels(line: str) -> str:
    line = re.sub(
        r"\[([^\[\]]*)\]",
        lambda match: "[" + clean_inline(match.group(1)) + "]",
        line,
    )
    return re.sub(
        r"\{([^{}]*)\}",
        lambda match: "{" + clean_inline(match.group(1)) + "}",
        line,
    )


def normalize_document(source: str) -> str:
    output: list[str] = []
    inside_ru_block = False
    in_fence = False

    for raw_line in source.splitlines():
        stripped = raw_line.strip()
        if RU_BLOCK_START.search(raw_line):
            inside_ru_block = True
            continue
        if RU_BLOCK_END.search(raw_line):
            inside_ru_block = False
            continue
        if inside_ru_block or RU_COMMENT.search(raw_line):
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            output.append(raw_line.rstrip())
            in_fence = not in_fence
            continue

        line = raw_line
        if has_forbidden_letter(line):
            if not in_fence and line.lstrip().startswith("|"):
                line = clean_table_line(line)
            else:
                candidate = clean_mermaid_labels(line) if in_fence else line
                line = clean_inline(candidate)
        output.append(line.rstrip())

    compact: list[str] = []
    blank_count = 0
    for line in output:
        if line:
            blank_count = 0
            compact.append(line)
        else:
            blank_count += 1
            if blank_count <= 1:
                compact.append("")
    return "\n".join(compact).strip() + "\n"


def validate_structure(relative: str, text: str) -> list[str]:
    problems: list[str] = []
    in_fence = False
    fence_language = ""
    table_width: int | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            if not in_fence:
                fence_language = stripped[3:].strip().lower()
            in_fence = not in_fence
            if not in_fence:
                fence_language = ""
            continue
        if not in_fence:
            if line.count("`") % 2:
                problems.append(f"{relative}:{line_number}: unmatched inline backtick")
            if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
                cells = line.strip().strip("|").split("|")
                width = len(cells)
                if all(TABLE_SEPARATOR.fullmatch(cell) for cell in cells):
                    if table_width is not None and width != table_width:
                        problems.append(
                            f"{relative}:{line_number}: Markdown table separator width mismatch"
                        )
                elif table_width is None:
                    table_width = width
                elif width != table_width:
                    problems.append(
                        f"{relative}:{line_number}: Markdown table row width mismatch"
                    )
            else:
                table_width = None
        elif fence_language == "mermaid":
            if line.count("[") != line.count("]"):
                problems.append(
                    f"{relative}:{line_number}: unbalanced Mermaid square brackets"
                )
            if line.count("{") != line.count("}"):
                problems.append(
                    f"{relative}:{line_number}: unbalanced Mermaid braces"
                )
    if in_fence:
        problems.append(f"{relative}: unclosed fenced code block")
    return problems


def documentation_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in DOCUMENTATION_SUFFIXES
        and not any(part in EXCLUDED_PARTS for part in path.parts)
    )


def run(root: pathlib.Path, mode: str) -> int:
    changed: list[pathlib.Path] = []
    violations: list[str] = []
    for path in documentation_files(root):
        relative = path.relative_to(root).as_posix()
        current = path.read_text(encoding="utf-8")
        normalized = normalize_document(current)
        if mode == "fix" and normalized != current:
            path.write_text(normalized, encoding="utf-8")
            changed.append(path)
        text = normalized if mode == "fix" else current
        for line_number, line in enumerate(text.splitlines(), start=1):
            if CYRILLIC.search(line) or has_forbidden_letter(line):
                violations.append(
                    f"{relative}:{line_number}: non-English alphabetic text"
                )
        violations.extend(validate_structure(relative, text))
    if mode == "fix":
        print(f"Normalized {len(changed)} documentation files.")
    if violations:
        print("Documentation language or structure violations:")
        print("\n".join(violations))
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("check", "fix"))
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path.cwd())
    args = parser.parse_args()
    return run(args.root.resolve(), args.mode)


if __name__ == "__main__":
    raise SystemExit(main())
