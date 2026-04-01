---
name: Coverage Optimizer
description: "Generate the highest-value next pytest unit tests for recently changed or selected Python files."
argument-hint: "Changed files or area to improve (for example: orchestrator error handling)"
agent: "agent"
tools: [read, search, execute]
---
Given this target area, propose the smallest set of high-impact pytest tests to improve defect detection and practical coverage:

{{input}}

Requirements:
- Prioritize behavior risk over raw percentage goals.
- Focus on boundary values, failure modes, and regression-prone branches.
- Reuse existing fixtures/patterns from the repository.
- Avoid integration-style dependencies unless explicitly requested.
- Prefer 5-12 concrete tests over long exhaustive lists.

Output format:
1. Test Plan (ordered by expected risk reduction)
2. Proposed Test Cases (name, purpose, setup notes, assertions)
3. Suggested File Targets (existing test files to extend, or new files if necessary)
4. Minimal pytest commands to run only affected tests
5. Optional follow-up if a coverage report is available
