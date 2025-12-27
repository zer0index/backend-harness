#!/usr/bin/env python3
"""
OpenAPI Specification Validator

Validates generated openapi.json files against best practices defined in
OPENAPI_IMPROVEMENTS_PLAN.md.

Usage:
    python openapi_validator.py path/to/openapi.json
    python openapi_validator.py path/to/project/  # Auto-finds openapi.json

Exit codes:
    0 - All checks passed
    1 - Validation errors found
    2 - File not found or invalid JSON
"""

import json
import sys
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_name: str
    passed: bool
    message: str
    severity: str = "error"  # "error", "warning", "info"
    details: List[str] = field(default_factory=list)


class OpenAPIValidator:
    """Validates OpenAPI specifications against best practices."""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.results: List[ValidationResult] = []

    def validate_all(self) -> Tuple[bool, List[ValidationResult]]:
        """Run all validation checks."""
        self.check_security_schemes()
        self.check_servers_configuration()
        self.check_empty_response_schemas()
        self.check_error_response_consistency()
        self.check_path_trailing_slashes()
        self.check_operation_ids()
        self.check_pagination_responses()
        self.check_common_error_responses()

        all_passed = all(r.passed or r.severity != "error" for r in self.results)
        return all_passed, self.results

    def check_security_schemes(self) -> None:
        """Check for proper security scheme definition."""
        components = self.spec.get("components", {})
        security_schemes = components.get("securitySchemes", {})

        if not security_schemes:
            self.results.append(ValidationResult(
                check_name="Security Schemes",
                passed=False,
                message="No security schemes defined",
                details=[
                    "Expected: components.securitySchemes with bearerAuth or similar",
                    "Recommendation: Define HTTPBearer security scheme for JWT authentication"
                ]
            ))
            return

        # Check for bearer auth
        has_bearer = any(
            scheme.get("type") == "http" and scheme.get("scheme") == "bearer"
            for scheme in security_schemes.values()
        )

        if has_bearer:
            self.results.append(ValidationResult(
                check_name="Security Schemes",
                passed=True,
                message="✓ Bearer authentication security scheme found",
                severity="info"
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Security Schemes",
                passed=False,
                message="No bearer authentication scheme found",
                severity="warning",
                details=[
                    f"Found schemes: {list(security_schemes.keys())}",
                    "Expected: HTTP Bearer scheme with bearerFormat: JWT"
                ]
            ))

    def check_servers_configuration(self) -> None:
        """Check for servers configuration."""
        servers = self.spec.get("servers", [])

        if not servers:
            self.results.append(ValidationResult(
                check_name="Servers Configuration",
                passed=False,
                message="No servers configured",
                details=[
                    "Expected: servers array with at least development environment",
                    "Recommendation: Add dev/staging/prod server URLs"
                ]
            ))
            return

        if len(servers) >= 2:
            self.results.append(ValidationResult(
                check_name="Servers Configuration",
                passed=True,
                message=f"✓ Found {len(servers)} server environments",
                severity="info",
                details=[f"  - {s.get('description', 'Unknown')}: {s.get('url')}" for s in servers]
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Servers Configuration",
                passed=True,
                message=f"Found {len(servers)} server(s) (recommend 2+)",
                severity="warning",
                details=[f"  - {s.get('description', 'Unknown')}: {s.get('url')}" for s in servers]
            ))

    def check_empty_response_schemas(self) -> None:
        """Detect empty response schemas ({})."""
        paths = self.spec.get("paths", {})
        empty_schemas = []

        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.startswith("x-") or method in ["parameters", "summary", "description"]:
                    continue

                responses = operation.get("responses", {})
                for status_code, response in responses.items():
                    content = response.get("content", {})
                    for media_type, media_content in content.items():
                        schema = media_content.get("schema", None)

                        # Check for empty schema {}
                        if schema is not None and not schema:
                            empty_schemas.append(f"{method.upper()} {path} [{status_code}]")

        if empty_schemas:
            self.results.append(ValidationResult(
                check_name="Empty Response Schemas",
                passed=False,
                message=f"Found {len(empty_schemas)} empty response schema(s)",
                details=empty_schemas[:10] + (["... and more"] if len(empty_schemas) > 10 else [])
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Empty Response Schemas",
                passed=True,
                message="✓ No empty response schemas found",
                severity="info"
            ))

    def check_error_response_consistency(self) -> None:
        """Check if ErrorResponse schema is defined."""
        components = self.spec.get("components", {})
        schemas = components.get("schemas", {})

        # Look for ErrorResponse or similar
        error_schema = schemas.get("ErrorResponse") or schemas.get("ErrorDetail")

        if not error_schema:
            self.results.append(ValidationResult(
                check_name="Error Response Schema",
                passed=False,
                message="No ErrorResponse schema found",
                severity="warning",
                details=[
                    "Expected: components.schemas.ErrorResponse with fields:",
                    "  - code (string)",
                    "  - message (string)",
                    "  - details (object, optional)",
                    "  - request_id (string, optional)"
                ]
            ))
            return

        # Check for required fields
        properties = error_schema.get("properties", {})
        required = error_schema.get("required", [])

        has_code = "code" in properties
        has_message = "message" in properties

        if has_code and has_message:
            self.results.append(ValidationResult(
                check_name="Error Response Schema",
                passed=True,
                message="✓ ErrorResponse schema properly defined",
                severity="info",
                details=[f"Fields: {', '.join(properties.keys())}"]
            ))
        else:
            missing = []
            if not has_code:
                missing.append("code")
            if not has_message:
                missing.append("message")

            self.results.append(ValidationResult(
                check_name="Error Response Schema",
                passed=False,
                message=f"ErrorResponse missing required fields: {', '.join(missing)}",
                severity="warning"
            ))

    def check_path_trailing_slashes(self) -> None:
        """Check for inconsistent trailing slashes in paths."""
        paths = self.spec.get("paths", {})
        paths_with_trailing_slash = [p for p in paths.keys() if p.endswith("/") and p != "/"]

        if paths_with_trailing_slash:
            self.results.append(ValidationResult(
                check_name="Path Trailing Slashes",
                passed=False,
                message=f"Found {len(paths_with_trailing_slash)} path(s) with trailing slashes",
                details=paths_with_trailing_slash[:10]
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Path Trailing Slashes",
                passed=True,
                message="✓ No trailing slashes in paths",
                severity="info"
            ))

    def check_operation_ids(self) -> None:
        """Check for human-readable operation IDs."""
        paths = self.spec.get("paths", {})
        missing_op_ids = []
        auto_generated_pattern = re.compile(r".*_(get|post|put|delete|patch)$")

        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.startswith("x-") or method in ["parameters", "summary", "description"]:
                    continue

                op_id = operation.get("operationId")

                if not op_id:
                    missing_op_ids.append(f"{method.upper()} {path}")
                elif auto_generated_pattern.match(op_id):
                    # Likely auto-generated (e.g., "get_users_api_v1_users_get")
                    missing_op_ids.append(f"{method.upper()} {path} (auto-generated: {op_id})")

        if missing_op_ids:
            self.results.append(ValidationResult(
                check_name="Operation IDs",
                passed=False,
                message=f"{len(missing_op_ids)} endpoint(s) missing human-readable operationId",
                severity="warning",
                details=missing_op_ids[:10] + (["... and more"] if len(missing_op_ids) > 10 else [])
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Operation IDs",
                passed=True,
                message="✓ All endpoints have operation IDs",
                severity="info"
            ))

    def check_pagination_responses(self) -> None:
        """Check for consistent pagination response structure."""
        components = self.spec.get("components", {})
        schemas = components.get("schemas", {})

        # Look for PaginatedResponse or similar
        paginated_schema = None
        for schema_name, schema_def in schemas.items():
            if "paginated" in schema_name.lower() or "page" in schema_name.lower():
                paginated_schema = (schema_name, schema_def)
                break

        if not paginated_schema:
            self.results.append(ValidationResult(
                check_name="Pagination Schema",
                passed=False,
                message="No PaginatedResponse schema found",
                severity="warning",
                details=[
                    "Expected: Generic PaginatedResponse with fields:",
                    "  - items (array)",
                    "  - total (integer)",
                    "  - limit (integer)",
                    "  - offset (integer)",
                    "  - count (integer)"
                ]
            ))
            return

        schema_name, schema_def = paginated_schema
        properties = schema_def.get("properties", {})

        expected_fields = {"items", "total", "limit", "offset", "count"}
        found_fields = set(properties.keys())
        missing_fields = expected_fields - found_fields

        if not missing_fields:
            self.results.append(ValidationResult(
                check_name="Pagination Schema",
                passed=True,
                message=f"✓ {schema_name} properly defined",
                severity="info"
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Pagination Schema",
                passed=False,
                message=f"{schema_name} missing fields: {', '.join(missing_fields)}",
                severity="warning"
            ))

    def check_common_error_responses(self) -> None:
        """Check if common error responses (401, 403, 404, 409, 422) are documented."""
        paths = self.spec.get("paths", {})
        endpoints_checked = 0
        endpoints_missing_errors = []

        common_errors = {"401", "403", "404", "409", "422"}

        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.startswith("x-") or method in ["parameters", "summary", "description"]:
                    continue

                endpoints_checked += 1
                responses = operation.get("responses", {})

                # Check if endpoint has at least one error response documented
                has_error_response = any(
                    str(code) in common_errors for code in responses.keys()
                )

                if not has_error_response:
                    endpoints_missing_errors.append(f"{method.upper()} {path}")

        if endpoints_missing_errors:
            missing_pct = (len(endpoints_missing_errors) / endpoints_checked * 100) if endpoints_checked > 0 else 0
            self.results.append(ValidationResult(
                check_name="Error Response Coverage",
                passed=False,
                message=f"{len(endpoints_missing_errors)}/{endpoints_checked} endpoints ({missing_pct:.0f}%) missing error responses",
                severity="warning",
                details=endpoints_missing_errors[:10] + (["... and more"] if len(endpoints_missing_errors) > 10 else [])
            ))
        else:
            self.results.append(ValidationResult(
                check_name="Error Response Coverage",
                passed=True,
                message=f"✓ All {endpoints_checked} endpoint(s) document error responses",
                severity="info"
            ))


def print_results(results: List[ValidationResult], verbose: bool = False) -> None:
    """Print validation results in a readable format."""
    errors = [r for r in results if not r.passed and r.severity == "error"]
    warnings = [r for r in results if not r.passed and r.severity == "warning"]
    passed = [r for r in results if r.passed]

    print("\n" + "=" * 70)
    print("OpenAPI Validation Results")
    print("=" * 70 + "\n")

    # Summary
    total = len(results)
    print(f"Total checks: {total}")
    print(f"  ✓ Passed:   {len(passed)}")
    print(f"  ⚠ Warnings: {len(warnings)}")
    print(f"  ✗ Errors:   {len(errors)}")
    print()

    # Errors
    if errors:
        print("❌ ERRORS")
        print("-" * 70)
        for result in errors:
            print(f"\n  {result.check_name}: {result.message}")
            if verbose and result.details:
                for detail in result.details:
                    print(f"    {detail}")

    # Warnings
    if warnings:
        print("\n⚠️  WARNINGS")
        print("-" * 70)
        for result in warnings:
            print(f"\n  {result.check_name}: {result.message}")
            if verbose and result.details:
                for detail in result.details:
                    print(f"    {detail}")

    # Passed (only in verbose mode)
    if verbose and passed:
        print("\n✅ PASSED")
        print("-" * 70)
        for result in passed:
            print(f"\n  {result.message}")
            if result.details:
                for detail in result.details:
                    print(f"    {detail}")

    print("\n" + "=" * 70)

    if not errors:
        if warnings:
            print("✓ Validation passed with warnings")
        else:
            print("✓ All checks passed!")
    else:
        print("✗ Validation failed")

    print("=" * 70 + "\n")


def find_openapi_file(path: Path) -> Path:
    """Find openapi.json in the given path or directory."""
    if path.is_file():
        return path

    # Check for openapi.json in the directory
    openapi_path = path / "openapi.json"
    if openapi_path.exists():
        return openapi_path

    # Check in common locations
    for common_path in ["docs/openapi.json", "api/openapi.json"]:
        check_path = path / common_path
        if check_path.exists():
            return check_path

    raise FileNotFoundError(f"Could not find openapi.json in {path}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate OpenAPI specification against best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python openapi_validator.py openapi.json
  python openapi_validator.py ./my_project/
  python openapi_validator.py openapi.json --verbose
        """
    )
    parser.add_argument(
        "path",
        help="Path to openapi.json file or project directory"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output including passed checks"
    )

    args = parser.parse_args()

    try:
        # Find and load OpenAPI spec
        spec_path = find_openapi_file(Path(args.path))
        print(f"Loading OpenAPI spec from: {spec_path}")

        with open(spec_path, 'r', encoding='utf-8') as f:
            spec = json.load(f)

        # Validate
        validator = OpenAPIValidator(spec)
        all_passed, results = validator.validate_all()

        # Print results
        print_results(results, verbose=args.verbose)

        # Exit with appropriate code
        sys.exit(0 if all_passed else 1)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.path}: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
