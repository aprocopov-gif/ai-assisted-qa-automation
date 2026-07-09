#!/usr/bin/env python3
"""Block edits under tests/** and pages/** that introduce constitution WON'T violations."""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

STRONG_MATCHERS = (
    "toBeVisible",
    "toBeHidden",
    "toHaveText",
    "toHaveCount",
    "toBeEnabled",
    "toBeDisabled",
    "toHaveURL",
    "toHaveTitle",
    "toContainText",
    "toHaveValue",
    "toBeChecked",
)

WEAK_MATCHERS = ("toBeTruthy", "toBeFalsy", "toBeDefined", "toBeUndefined")

RE_SNAPSHOT_EXPECT = re.compile(r"expect\s*\(\s*await\s+")
RE_CREDENTIAL_ASSIGN = re.compile(
    r"(?:password|passwd|pwd|secret|api[_-]?token|api[_-]?key)\s*[:=]\s*['\"][^'\"]{4,}['\"]",
    re.IGNORECASE,
)
RE_EMAIL_ASSIGN = re.compile(
    r"(?:email|user(?:name)?)\s*[:=]\s*['\"][^'\"]+@[^'\"]+['\"]",
    re.IGNORECASE,
)
RE_LOGIN_LITERAL = re.compile(
    r"\.login\s*\(\s*['\"][^'\"]+@[^'\"]+['\"]\s*,\s*['\"][^'\"]+['\"]\s*\)"
)
RE_KNOWN_TOKEN = re.compile(
    r"['\"](?:dt_[a-f0-9]{20,}|ATATT[a-zA-Z0-9+/=_-]{20,}|github_pat_[a-zA-Z0-9_]{20,}|crsr_[a-f0-9]{20,})['\"]"
)


@dataclass(frozen=True)
class ViolationCheck:
    name: str
    message: str
    pattern: re.Pattern[str] | None = None
    detect: Callable[[str], bool] | None = None

    def matches(self, content: str) -> bool:
        if self.detect is not None:
            return self.detect(content)
        if self.pattern is not None:
            return bool(self.pattern.search(content))
        return False


def has_hardcoded_credential(text: str) -> bool:
    for line in text.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("//") or trimmed.startswith("*"):
            continue
        if re.search(r"process\.env|requireEnv\s*\(", line):
            continue
        if RE_CREDENTIAL_ASSIGN.search(line):
            return True
        if RE_EMAIL_ASSIGN.search(line):
            return True
        if RE_LOGIN_LITERAL.search(line):
            return True
        if RE_KNOWN_TOKEN.search(line):
            return True
    return False


VIOLATION_CHECKS: tuple[ViolationCheck, ...] = (
    ViolationCheck(
        name="waitForTimeout",
        message="`.waitForTimeout()` is forbidden — use web-first `expect()` assertions",
        pattern=re.compile(r"\.waitForTimeout\s*\("),
    ),
    ViolationCheck(
        name="xpath",
        message="XPath locators are forbidden — use `getByRole`, `getByLabel`, or `getByText`",
        pattern=re.compile(
            r"""\.locator\s*\(\s*[`'"]\s*//"""
            r"""|\.locator\s*\(\s*[`'"][^`'"]*xpath"""
            r"""|xpath\s*=\s*[`'"]""",
            re.IGNORECASE,
        ),
    ),
    ViolationCheck(
        name="any_type",
        message="The `any` type is forbidden — use concrete types",
        pattern=re.compile(r":\s*any\b|as\s+any\b|<any>|Array<any>"),
    ),
    ViolationCheck(
        name="hardcoded_credential",
        message="Hardcoded credentials are forbidden — use `process.env` / `requireEnv()`",
        detect=has_hardcoded_credential,
    ),
    ViolationCheck(
        name="describe_tag",
        message="Tags on `test.describe()` are forbidden — tag individual `test()` blocks only",
        pattern=re.compile(
            r"(?:test|describe)\.describe\s*\([^)]*,\s*\{[^}]*\btag\s*:",
            re.DOTALL,
        ),
    ),
)


def is_guarded_file(file_path: str) -> bool:
    normalized = file_path.replace("\\", "/")
    if not re.search(r"(^|/)(tests|pages)/", normalized):
        return False
    return normalized.endswith((".ts", ".tsx", ".js", ".jsx"))


def is_test_file(file_path: str) -> bool:
    normalized = file_path.replace("\\", "/")
    return re.search(r"(^|/)tests/.+\.(spec|test)\.[jt]sx?$", normalized) is not None


def active_expect_count(content: str) -> int:
    count = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("*"):
            continue
        comment_idx = line.find("//")
        code = line[:comment_idx] if comment_idx >= 0 else line
        count += code.count("expect(")
    return count


def reconstruct_before(after: str, edits: list[dict]) -> str | None:
    before = after
    for edit in reversed(edits):
        new_string = edit.get("new_string", "")
        old_string = edit.get("old_string", "")
        if new_string:
            if new_string not in before:
                return None
            before = before.replace(new_string, old_string, 1)
        elif old_string and old_string not in before:
            before = before + old_string
        else:
            return None
    return before


def expect_delta_from_edits(edits: list[dict]) -> int:
    delta = 0
    for edit in edits:
        old_string = edit.get("old_string", "")
        new_string = edit.get("new_string", "")
        delta += active_expect_count(old_string) - active_expect_count(new_string)
    return delta


def find_violations(content: str) -> list[ViolationCheck]:
    return [check for check in VIOLATION_CHECKS if check.matches(content)]


def introduced_from_edits(edits: list[dict]) -> list[ViolationCheck]:
    hits: list[ViolationCheck] = []
    seen: set[str] = set()
    for edit in edits:
        new_string = edit.get("new_string", "")
        old_string = edit.get("old_string", "")
        for check in find_violations(new_string):
            if check.name in seen or check.matches(old_string):
                continue
            hits.append(check)
            seen.add(check.name)
    return hits


def introduced_violations(before: str, after: str, edits: list[dict]) -> list[ViolationCheck]:
    before_names = {check.name for check in find_violations(before)}
    hits = [check for check in find_violations(after) if check.name not in before_names]
    if hits:
        return hits
    return introduced_from_edits(edits)


def check_weakened_expect(before: str, after: str) -> str | None:
    if RE_SNAPSHOT_EXPECT.search(after) and not RE_SNAPSHOT_EXPECT.search(before):
        return "snapshot `expect(await …)` — use `await expect(locator)`"

    for strong in STRONG_MATCHERS:
        strong_re = re.compile(rf"\.{strong}\s*\(")
        if (
            strong_re.search(before)
            and not strong_re.search(after)
            and "expect(" in after
            and active_expect_count(after) >= active_expect_count(before)
        ):
            return f"weakened assertion: removed `.{strong}()`"

    for strong in STRONG_MATCHERS:
        strong_re = re.compile(rf"\.{strong}\s*\(")
        for weak in WEAK_MATCHERS:
            weak_re = re.compile(rf"\.{weak}\s*\(")
            if strong_re.search(before) and weak_re.search(after) and not weak_re.search(before):
                return f"weakened assertion: `.{strong}()` → `.{weak}()`"

    if (
        ".not." in before
        and ".not." not in after
        and "expect(" in before
        and "expect(" in after
        and active_expect_count(after) >= active_expect_count(before)
    ):
        return "weakened assertion: removed `.not.`"

    return None


def block(message: str, path_name: str) -> None:
    full = f"Blocked: constitution violation in {path_name}\n  {message}"
    sys.stderr.write(full + "\n")
    print(json.dumps({"user_message": full, "agent_message": full}))
    sys.exit(2)


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.stderr.write("guard-constitution: empty stdin\n")
        sys.exit(1)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"guard-constitution: invalid JSON: {exc}\n")
        sys.exit(1)

    file_path = payload.get("file_path", "")
    if not file_path or not is_guarded_file(file_path):
        sys.exit(0)

    path = Path(file_path)
    if not path.is_file():
        sys.stderr.write(f"guard-constitution: file not found: {file_path}\n")
        sys.exit(1)

    after = path.read_text(encoding="utf-8")
    edits = payload.get("edits") or []
    if not edits:
        sys.exit(0)

    reconstructed = reconstruct_before(after, edits)
    edit_delta = expect_delta_from_edits(edits)
    before = reconstructed if reconstructed is not None else after

    new_violations = introduced_violations(before, after, edits)
    if new_violations:
        details = "; ".join(check.message for check in new_violations)
        block(details, path.name)

    if is_test_file(file_path):
        after_count = active_expect_count(after)
        before_count = (
            active_expect_count(before)
            if reconstructed is not None
            else after_count + edit_delta
        )
        if after_count < before_count:
            block(
                f"active `expect(` count dropped ({before_count} -> {after_count}); "
                "do not delete or comment out assertions to go green",
                path.name,
            )

        weakened = check_weakened_expect(before, after)
        if weakened:
            block(weakened, path.name)

    sys.stderr.write(f"guard-constitution: OK — {path.name}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
