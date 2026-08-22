from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field

from cli.core.models.audit.Severity import Severity


class Status(StrEnum):
    """
    Status for each finding
    """

    PASS = "pass"
    FAIL = "fail"
    SKIPPED = "skipped"
    ERROR = "error"


class Category(StrEnum):
    """
    The category of a finding
    """

    FIREWALL = "Firewall"
    SERVICE = "Service"
    SYSTEM = "System"


class Finding(BaseModel):
    """
    A single finding from the audit

    Parameters
    ----------
    id: str
        Identifier ID for the finding
    title: str
        Title of the finding
    severity: Severity
        Severity of the finding (Enum)
    status: Status
        Status of the finding (Enum)
    host: str
        Where this finding was found
    category: Category
        Category of the finding (Enum)
    description: str
        Description of the finding
    evidence: str
        Evidence found of the finding
    remediation: str
        Recommended remediation for this finding
    references: list[str]
        Reference of this finding (NIS2, ISO27001...)
    """

    id: str
    title: str
    severity: Severity
    status: Status
    host: str | None = None
    category: Category
    description: str | None = None
    evidence: str | None = None
    remediation: str | None = None
    references: list[str] = Field(default_factory=list)
