"""Archive a clean tagged release with Git history and SHA-256 checksums."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True
    )
    return result.stdout.strip()


def build_submission(tag: str, output: Path) -> dict:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    name, version = project["name"], project["version"]
    if tag != f"v{version}":
        raise ValueError("Tag must match the package version")
    if git("status", "--porcelain"):
        raise ValueError("Commit all changes before creating the submission")
    revision = git("rev-parse", "HEAD")
    if git("rev-parse", f"{tag}^{{commit}}") != revision:
        raise ValueError("The release tag must point to HEAD")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    stem = f"{name}-{tag}"
    archive, bundle = output / f"{stem}.zip", output / f"{stem}.bundle"
    git("archive", "--format=zip", f"--prefix={stem}/", f"--output={archive}", tag)
    git("bundle", "create", str(bundle), "--all")
    git("bundle", "verify", str(bundle))
    artifacts = [
        archive,
        bundle,
        *sorted(output.glob(f"{name}-{version}*.whl")),
        *sorted(output.glob(f"{name}-{version}.tar.gz")),
    ]
    clean_check = output / "clean_install_validation.json"
    if clean_check.is_file():
        artifacts.append(clean_check)
    checksums = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in artifacts}
    manifest = {
        "name": name,
        "version": version,
        "tag": tag,
        "commit": revision,
        "tracked_files": len(git("ls-files").splitlines()),
        "sha256": checksums,
        "archive_policy": "Committed source only; environments/caches excluded.",
        "history": "The Git bundle preserves all local refs and milestone commits.",
    }
    manifest_path = output / "release_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    checksums[manifest_path.name] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    (output / "SHA256SUMS").write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    parser.add_argument("--tag", default=f"v{project['version']}")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    manifest = build_submission(args.tag, args.output)
    print(f"Submission prepared for {manifest['tag']} at {manifest['commit'][:7]}: {args.output}")


if __name__ == "__main__":
    main()
