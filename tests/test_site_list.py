"""Tests for sample-site CSV validation."""

from pathlib import Path

from consent_audit.site_list import IssueLevel, validate_site_list


def test_validate_site_list_counts_active_rows_and_categories(tmp_path: Path) -> None:
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "# comment row,,,,\n"
        "https://www.bbc.com,BBC,news,false,smoke\n"
        "https://www.reddit.com,Reddit,social,true,mentor list\n",
        encoding="utf-8",
    )

    result = validate_site_list(sites_csv)

    assert result.active_count == 2
    assert result.categories == {"news": 1, "social": 1}
    assert result.inherited_from_phd_mentor_count == 1
    assert result.errors == []


def test_validate_site_list_flags_placeholder_duplicates_and_bad_urls(tmp_path: Path) -> None:
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text(
        "url,name,category,inherited_from_phd_mentor,notes\n"
        "https://example.com,Example,placeholder,false,delete before real run\n"
        "https://www.bbc.com,BBC,news,false,\n"
        "https://www.bbc.com/,BBC duplicate,news,false,\n"
        "not-a-url,Broken,news,false,\n",
        encoding="utf-8",
    )

    result = validate_site_list(sites_csv)

    assert {issue.level for issue in result.issues} == {IssueLevel.ERROR}
    assert {issue.code for issue in result.errors} == {
        "placeholder_url",
        "placeholder_category",
        "duplicate_url",
        "invalid_url",
    }


def test_validate_site_list_flags_missing_url_column(tmp_path: Path) -> None:
    sites_csv = tmp_path / "sites.csv"
    sites_csv.write_text("name,category\nBBC,news\n", encoding="utf-8")

    result = validate_site_list(sites_csv)

    assert [issue.code for issue in result.errors] == ["missing_required_column"]
