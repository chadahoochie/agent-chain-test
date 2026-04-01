---
name: Pytest Testing Standards
description: "Use when writing or reviewing Python pytest tests. Standardizes test naming, fixture scope, and mocking conventions."
applyTo:
  - "**/tests/**/*.py"
  - "**/test_*.py"
  - "**/*_test.py"
---
# Pytest Unit Testing Standards

## Test Naming
- Name test functions as `test_<unit>_<condition>_<expected_result>`.
- Keep names behavioral, not implementation-specific.
- Prefer parameterized tests for multiple input/output examples of one behavior.

## Fixture Scope
- Default to `function` scope unless a broader scope is justified.
- Use `module` or `session` scope only for expensive, read-only setup.
- Avoid mutable shared fixture state across tests.
- Keep fixtures small and composable; do not hide core assertions in fixtures.

## Mocking Conventions
- Mock at boundaries (HTTP clients, DB clients, external SDKs), not internal pure logic.
- Prefer fakes/stubs over deep mock chains where practical.
- Assert externally visible behavior first; call assertions are secondary.
- Avoid brittle assertions tied to exact call ordering unless ordering is a real requirement.
- Patch where the dependency is looked up, not where it is defined.

## Reliability Rules
- No real network, filesystem, or clock dependence in unit tests without explicit need.
- Seed randomness when random data is used.
- Keep tests independent and runnable in any order.
- Each test should assert at least one meaningful outcome.

## Structure
- Use clear arrange/act/assert phases.
- Keep one primary behavior assertion per test; use additional assertions only when tightly related.
- Prefer explicit expected values over loose truthy/falsy checks when possible.
