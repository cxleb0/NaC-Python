from modules.git import compare_findings
from modules.module import Finding

old_finding = Finding(
    rule="Allow DNS",
    issue="Missing Description",
    severity="MEDIUM",
    message="Security rule missing description"
)

def test_new_findings():
    old_findings = []
    new_findings = [
        Finding(
            rule="Allow DNS",
            issue="Missing Description",
            severity="MEDIUM",
            message="Security rule missing description"
        )
    ]
    results = compare_findings(old_findings, new_findings)
    assert len(results["new"]) == 1
    assert results["new"][0].rule == "Allow DNS"
    assert results["new"][0].issue == "Missing Description"
    assert results["new"][0].severity == "MEDIUM"
    assert results["new"][0].message == "Security rule missing description"
    assert len(results["resolved"]) == 0
    assert len(results["persistent"]) == 0

def test_persistent_findings():
    old_findings = [old_finding]
    new_findings = [
        Finding(
            rule="Allow DNS",
            issue="Missing Description",
            severity="MEDIUM",
            message="Security rule missing description"
        )
    ]
    results = compare_findings(old_findings, new_findings)
    assert len(results["persistent"]) == 1
    assert results["persistent"][0].rule == "Allow DNS"
    assert results["persistent"][0].issue == "Missing Description"
    assert results["persistent"][0].severity == "MEDIUM"
    assert results["persistent"][0].message == "Security rule missing description"
    assert len(results["resolved"]) == 0
    assert len(results["new"]) == 0

def test_resolved_findings():
    old_findings = [old_finding]
    new_findings = []
    results = compare_findings(old_findings, new_findings)
    assert len(results["resolved"]) == 1
    assert results["resolved"][0].rule == "Allow DNS"
    assert results["resolved"][0].issue == "Missing Description"
    assert results["resolved"][0].severity == "MEDIUM"
    assert results["resolved"][0].message == "Security rule missing description"
    assert len(results["new"]) == 0
    assert len(results["persistent"]) == 0

def test_multiple_findings():
        old_findings = [old_finding]
        new_findings = [
            Finding(
                rule="Allow DNS",
                issue="Missing Description",
                severity="MEDIUM",
                message="Security rule missing description"
            ),
            Finding(
                rule="Allow DHCP",
                issue="Logging is disabled",
                severity="HIGH",
                message="Security rule's logging is disabled"
            )
        ]
        results = compare_findings(old_findings, new_findings)
        assert len(results["new"]) == 1
        assert len(results["persistent"]) == 1
        assert results["new"][0].rule == "Allow DHCP"
        assert results["persistent"][0].rule == "Allow DNS"
