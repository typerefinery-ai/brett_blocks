#!/usr/bin/env python3
"""
Run all example StixORM forms through make_stixorm_object and compare outputs.

For each form in Block_Families/StixORM/Generic/example_forms:
1) Build `overall = base_required | base_optional | object | extensions`
2) Call make_stixorm_object(form)
3) Compare overall vs returned dict with DeepDiff
4) Log details to a local text report file
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from deepdiff import DeepDiff
except ImportError as exc:
    raise ImportError(
        "DeepDiff is required. Install it with: pip install deepdiff"
    ) from exc

import make_stixorm_object as stixorm_maker


def _repo_root() -> Path:
    # .../Block_Families/StixORM/Generic -> repo root
    return Path(__file__).resolve().parents[3]


def _example_forms_dir() -> Path:
    return Path(__file__).resolve().parent / "example_forms"


def _default_log_path() -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path(__file__).resolve().parent / f"check_make_stixorm_object_{ts}.txt"


def _json_dumpable(diff: DeepDiff) -> Any:
    # DeepDiff contains non-JSON-native objects; use its JSON serializer.
    return json.loads(diff.to_json())


def _pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def _write_text_entry(log_file, entry: dict[str, Any], index: int) -> None:
    line = "=" * 100
    section = "-" * 100
    log_file.write(f"{line}\n")
    log_file.write(f"CASE {index:02d}: {entry['form_name']}\n")
    log_file.write(f"{line}\n\n")
    log_file.write(f"Status       : {entry['status']}\n")
    log_file.write(f"Timestamp    : {entry['timestamp_utc']}\n")
    log_file.write(f"Form Path    : {entry['form_path']}\n")
    if entry["error"]:
        log_file.write(f"Error        : {entry['error']}\n")
    log_file.write("\n")
    log_file.write(f"{section}\nOVERALL DICT\n{section}\n")
    log_file.write(f"{_pretty_json(entry['overall'])}\n\n")
    log_file.write(f"{section}\nRETURNED DICT\n{section}\n")
    log_file.write(f"{_pretty_json(entry['returned_dict'])}\n\n")
    log_file.write(f"{section}\nDEEPDIFF\n{section}\n")
    log_file.write(f"{_pretty_json(entry['deepdiff'])}\n\n")


def _load_form(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    required = data["base_required"]
    optional = data["base_optional"]
    obj = data["object"]
    extensions = data["extensions"]
    overall = required | optional | obj | extensions
    overall = _remove_empty_values(overall)
    return {"form": data, "overall": overall}


def _is_empty_value(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _remove_empty_values(data: Any) -> Any:
    if isinstance(data, dict):
        cleaned: dict[str, Any] = {}
        for key, val in data.items():
            next_val = _remove_empty_values(val)
            if _is_empty_value(next_val):
                continue
            cleaned[key] = next_val
        return cleaned
    if isinstance(data, list):
        cleaned_list = [_remove_empty_values(item) for item in data]
        return [item for item in cleaned_list if not _is_empty_value(item)]
    return data


def run_check(log_path: Path, verbose: bool = True) -> int:
    forms_dir = _example_forms_dir()
    form_files = sorted(forms_dir.glob("*.json"))
    if not form_files:
        raise FileNotFoundError(f"No JSON forms found in: {forms_dir}")

    # make_stixorm_object.py uses a relative path for parse.py; set it explicitly.
    stixorm_maker.TR_Common_Files = str(
        _repo_root() / "Orchestration" / "generated" / "os-triage" / "common_files"
    )

    log_path.parent.mkdir(parents=True, exist_ok=True)
    success_count = 0
    mismatch_count = 0
    error_count = 0

    with log_path.open("w", encoding="utf-8") as log_file:
        header_line = "#" * 100
        log_file.write(f"{header_line}\n")
        log_file.write("CHECK MAKE STIXORM OBJECT REPORT\n")
        log_file.write(f"{header_line}\n\n")
        log_file.write(f"Run Timestamp (UTC): {datetime.now(timezone.utc).isoformat()}\n")
        log_file.write(f"Forms Directory    : {forms_dir}\n")
        log_file.write(f"Total Forms        : {len(form_files)}\n\n")

        for idx, form_path in enumerate(form_files, start=1):
            entry: dict[str, Any] = {
                "form_name": form_path.name,
                "form_path": str(form_path),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "overall": None,
                "returned_dict": None,
                "deepdiff": None,
                "status": "unknown",
                "error": None,
            }
            try:
                loaded = _load_form(form_path)
                form = loaded["form"]
                overall = loaded["overall"]
                returned = stixorm_maker.make_stixorm_object(form)
                diff = DeepDiff(overall, returned, ignore_order=True)

                entry["overall"] = overall
                entry["returned_dict"] = returned
                entry["deepdiff"] = _json_dumpable(diff)
                entry["status"] = "match" if not diff else "mismatch"

                if diff:
                    mismatch_count += 1
                else:
                    success_count += 1
            except Exception as exc:  # noqa: BLE001
                error_count += 1
                entry["status"] = "error"
                entry["error"] = repr(exc)

            _write_text_entry(log_file, entry, idx)
            if verbose:
                print(f"{entry['form_name']}: {entry['status']}")

        summary_line = "#" * 100
        log_file.write(f"{summary_line}\n")
        log_file.write("SUMMARY\n")
        log_file.write(f"{summary_line}\n")
        log_file.write(f"Forms checked : {len(form_files)}\n")
        log_file.write(f"Matches       : {success_count}\n")
        log_file.write(f"Mismatches    : {mismatch_count}\n")
        log_file.write(f"Errors        : {error_count}\n")

    print("\nRun complete")
    print(f"- Forms checked : {len(form_files)}")
    print(f"- Matches       : {success_count}")
    print(f"- Mismatches    : {mismatch_count}")
    print(f"- Errors        : {error_count}")
    print(f"- Log file      : {log_path}")

    return 0 if error_count == 0 else 1


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check all example StixORM forms against make_stixorm_object output"
    )
    parser.add_argument(
        "--log-file",
        default=str(_default_log_path()),
        help="Path to text output log",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-form status output",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()
    raise SystemExit(run_check(log_path=Path(args.log_file), verbose=not args.quiet))
