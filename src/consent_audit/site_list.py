"""Validation helpers for research sample site CSVs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from urllib.parse import urlparse, urlunparse


class IssueLevel(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class SiteListIssue:
    level: IssueLevel
    code: str
    message: str
    row_number: int | None = None
    url: str = ""


@dataclass(frozen=True)
class SiteListValidation:
    path: Path
    active_count: int
    categories: dict[str, int]
    inherited_from_phd_mentor_count: int
    issues: list[SiteListIssue]

    @property
    def errors(self) -> list[SiteListIssue]:
        return [issue for issue in self.issues if issue.level == IssueLevel.ERROR]

    @property
    def warnings(self) -> list[SiteListIssue]:
        return [issue for issue in self.issues if issue.level == IssueLevel.WARNING]


def validate_site_list(path: Path) -> SiteListValidation:
    issues: list[SiteListIssue] = []
    categories: dict[str, int] = {}
    seen_urls: dict[str, int] = {}
    active_count = 0
    inherited_count = 0

    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = set(reader.fieldnames or [])
        if "url" not in fieldnames:
            return SiteListValidation(
                path=path,
                active_count=0,
                categories={},
                inherited_from_phd_mentor_count=0,
                issues=[
                    SiteListIssue(
                        level=IssueLevel.ERROR,
                        code="missing_required_column",
                        message="Site CSV must include a 'url' column.",
                    )
                ],
            )

        for row_number, row in enumerate(reader, start=2):
            url = (row.get("url") or "").strip()
            if not url or url.startswith("#"):
                continue

            active_count += 1
            parsed = urlparse(url)
            canonical_url = _canonicalize_url(url)
            if canonical_url == "":
                issues.append(
                    SiteListIssue(
                        level=IssueLevel.ERROR,
                        code="invalid_url",
                        message="URL must be absolute and use http or https.",
                        row_number=row_number,
                        url=url,
                    )
                )
            elif canonical_url in seen_urls:
                issues.append(
                    SiteListIssue(
                        level=IssueLevel.ERROR,
                        code="duplicate_url",
                        message=f"Duplicate of row {seen_urls[canonical_url]}.",
                        row_number=row_number,
                        url=url,
                    )
                )
            else:
                seen_urls[canonical_url] = row_number

            if parsed.hostname in {"example.com", "www.example.com"}:
                issues.append(
                    SiteListIssue(
                        level=IssueLevel.ERROR,
                        code="placeholder_url",
                        message="Placeholder URL must be removed before a real run.",
                        row_number=row_number,
                        url=url,
                    )
                )

            category = (row.get("category") or "").strip().lower()
            if category:
                categories[category] = categories.get(category, 0) + 1
            if category == "placeholder":
                issues.append(
                    SiteListIssue(
                        level=IssueLevel.ERROR,
                        code="placeholder_category",
                        message="Placeholder category must be removed before a real run.",
                        row_number=row_number,
                        url=url,
                    )
                )

            if _is_truthy(row.get("inherited_from_phd_mentor") or ""):
                inherited_count += 1

    return SiteListValidation(
        path=path,
        active_count=active_count,
        categories=categories,
        inherited_from_phd_mentor_count=inherited_count,
        issues=issues,
    )


def _canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""

    path = parsed.path.rstrip("/")
    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            "",
            parsed.query,
            "",
        )
    )


def _is_truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}
