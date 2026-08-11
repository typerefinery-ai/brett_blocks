#!/usr/bin/env python3
"""
One-off utility: copy StixORM template JSON files into the os-triage generated tree.

Layout (flat buckets, lowercase):

    Orchestration/generated/os-triage/common_files/templates/sdo/<name>.json
    Orchestration/generated/os-triage/common_files/templates/sco/<name>.json
    Orchestration/generated/os-triage/common_files/templates/sro/<name>.json

Templates from SDO/SCO/SRO land in the matching bucket only (no per-class subfolders).
Anything resolved under StixORM but outside those three top-level dirs uses ``meta/``.

Mode is controlled by COPY_MODE:

- "dict": only templates listed in INITIAL_SET_TEMPLATE_PATHS (kept in sync with
  a_seed/2_initial_set_of_blocks.md — the sdo/sco/sro_make_files entries).
- "all": every *template*.json under Block_Families/StixORM/{SDO,SCO,SRO}.

Run from anywhere:

    python Block_Families/StixORM/extract_templates.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Switch to "all" when you want every StixORM template copied again.
# ---------------------------------------------------------------------------
COPY_MODE: str = "dict"  # "dict" | "all"

# Template paths from a_seed/2_initial_set_of_blocks.md (sdo/sco/sro_make_files).
INITIAL_SET_TEMPLATE_PATHS: tuple[str, ...] = (
    "Block_Families/StixORM/SDO/Identity/Identity_template.json",
    "Block_Families/StixORM/SDO/Indicator/Indicator_template.json",
    "Block_Families/StixORM/SDO/Impact/Impact_template.json",
    "Block_Families/StixORM/SDO/Incident/Incident_template.json",
    "Block_Families/StixORM/SDO/Event/Event_template.json",
    "Block_Families/StixORM/SDO/Observed_Data/ObservedData_template.json",
    "Block_Families/StixORM/SDO/Sequence/Sequence_template.json",
    "Block_Families/StixORM/SDO/Task/Task_template.json",
    "Block_Families/StixORM/SCO/Anecdote/Anecdote_template.json",
    "Block_Families/StixORM/SCO/EmailAddress/EmailAddress_template.json",
    "Block_Families/StixORM/SCO/UserAccount/UserAccount_template.json",
    "Block_Families/StixORM/SCO/URL/URL_template.json",
    "Block_Families/StixORM/SCO/Email_Message/EmailMessage_template.json",
    "Block_Families/StixORM/SRO/Relationship/Relationship_template.json",
    "Block_Families/StixORM/SRO/Sighting/Sighting_template.json",
)

_BUCKET_FOR_TOP = {"SDO": "sdo", "SCO": "sco", "SRO": "sro"}


def _stixorm_root() -> Path:
    return Path(__file__).resolve().parent


def _repo_root(stixorm: Path) -> Path:
    return stixorm.parent.parent


def _is_template_json(path: Path) -> bool:
    if path.suffix.lower() != ".json":
        return False
    return "template" in path.name.lower()


def _join_repo(repo: Path, posix_path: str) -> Path:
    return repo.joinpath(*posix_path.split("/"))


def _resolve_dict_source(repo: Path, posix_path: str) -> Path:
    """
    Resolve a repo-relative path from the seed dict. Applies small path fixes
    where the markdown still uses older folder names.
    """
    primary = _join_repo(repo, posix_path)
    if primary.is_file():
        return primary
    fixed = posix_path.replace("Observed_Data/", "ObservedData/").replace(
        "Email_Message/", "EmailMessage/"
    )
    if fixed != posix_path:
        alt = _join_repo(repo, fixed)
        if alt.is_file():
            return alt
    return primary


def _bucket_for_source(stixorm: Path, src: Path) -> str:
    rel = src.resolve().relative_to(stixorm.resolve())
    top = rel.parts[0].upper()
    return _BUCKET_FOR_TOP.get(top, "meta")


def _copy_flat(stixorm: Path, dest_root: Path, src: Path) -> tuple[Path, Path, str, str] | None:
    """
    Copy src into dest_root/<bucket>/<basename>.

    Returns (src, dest, bucket, basename) for logging, or None if skipped (collision).
    """
    bucket = _bucket_for_source(stixorm, src)
    name = src.name
    dest = dest_root / bucket / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        try:
            if dest.samefile(src):
                return (src, dest, bucket, name)
        except OSError:
            pass
        print(
            f"ERROR: destination already exists with a different file (skipped): {dest}",
            file=sys.stderr,
        )
        return None
    shutil.copy2(src, dest)
    return (src, dest, bucket, name)


def _print_logical(bucket: str, basename: str) -> None:
    logical = (
        Path("Orchestration")
        / "generated"
        / "os-triage"
        / "common_files"
        / "templates"
        / bucket
        / basename
    )
    print(logical.as_posix())


def copy_from_dict(stixorm: Path, dest_root: Path, repo: Path) -> int:
    copied: list[tuple[Path, Path, str, str]] = []
    errors = 0
    for posix_path in INITIAL_SET_TEMPLATE_PATHS:
        src = _resolve_dict_source(repo, posix_path)
        if not src.is_file():
            print(f"ERROR: template not found (skipped): {src}", file=sys.stderr)
            errors += 1
            continue
        item = _copy_flat(stixorm, dest_root, src)
        if item is None:
            errors += 1
            continue
        copied.append(item)

    print(f"Copied {len(copied)} template file(s) (dict mode) to:\n  {dest_root}\n")
    for _src, _dst, bucket, basename in copied:
        _print_logical(bucket, basename)
    if errors:
        print(f"\nSkipped {errors} path(s) that were missing or collided on disk.", file=sys.stderr)
    return 1 if errors else 0


def copy_all(stixorm: Path, dest_root: Path) -> int:
    groups = ("SDO", "SCO", "SRO")
    copied: list[tuple[Path, Path, str, str]] = []
    skipped = 0

    for group in groups:
        src_base = stixorm / group
        if not src_base.is_dir():
            print(f"WARNING: source directory missing, skipping: {src_base}", file=sys.stderr)
            continue

        for path in sorted(src_base.rglob("*.json")):
            if not _is_template_json(path):
                continue
            item = _copy_flat(stixorm, dest_root, path)
            if item is None:
                skipped += 1
                continue
            copied.append(item)

    print(f"Copied {len(copied)} template file(s) (all mode) to:\n  {dest_root}\n")
    for _src, _dst, bucket, basename in copied:
        _print_logical(bucket, basename)
    if skipped:
        print(f"\nSkipped {skipped} file(s) due to name collisions in flat layout.", file=sys.stderr)
    return 1 if skipped else 0


def main() -> int:
    stixorm = _stixorm_root()
    repo = _repo_root(stixorm)
    dest_root = repo / "Orchestration" / "generated" / "os-triage" / "common_files" / "templates"

    mode = COPY_MODE.strip().lower()
    if mode == "dict":
        return copy_from_dict(stixorm, dest_root, repo)
    if mode == "all":
        return copy_all(stixorm, dest_root)

    print(f"ERROR: unknown COPY_MODE {COPY_MODE!r} (use 'dict' or 'all')", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
