from __future__ import annotations

import subprocess
from pathlib import Path

from ..errors import PreparationError
from .models import GitProvenance


def _run_git(arguments: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreparationError(
            "git_unavailable", "required Git information is unavailable"
        ) from exc


def capture_git(project_root: Path) -> GitProvenance:
    try:
        root_result = _run_git(["rev-parse", "--show-toplevel"], project_root)
    except PreparationError:
        raise
    discovered_root = Path(root_result.stdout.strip()).resolve()
    expected_root = project_root.resolve()
    if discovered_root != expected_root:
        raise PreparationError("git_root_mismatch", "Git root does not match the project root")
    try:
        commit_result = _run_git(["rev-parse", "--verify", "HEAD^{commit}"], project_root)
    except PreparationError as exc:
        raise PreparationError(
            "git_commit_missing", "Git HEAD does not resolve to a commit"
        ) from exc
    commit = commit_result.stdout.strip()
    if len(commit) != 40 or any(character not in "0123456789abcdef" for character in commit):
        raise PreparationError("git_commit_missing", "Git HEAD does not resolve to a full commit")
    branch_result = _run_git(["branch", "--show-current"], project_root)
    status_result = _run_git(["status", "--porcelain=v1", "--untracked-files=all"], project_root)
    branch = branch_result.stdout.strip() or None
    return GitProvenance(
        root=expected_root,
        commit=commit,
        branch=branch,
        clean=status_result.stdout == "",
    )
