# Detailed Python Comment Guidelines

## Philosophy: Why > What
Comments should answer questions that the code cannot.
- **Good**: Explain *why* a workaround is used due to a framework bug.
- **Good**: Explain *why* a cache is enabled based on specific device performance testing.
- **Bad**: Explaining that a loop iterates over a list of users.

## Anticipate Questions
A good rule of thumb: If a piece of logic might prompt a question during code review, write a comment explaining it beforehand.

## Do Not Repeat the Code
Assume the reader is familiar with Python. Over-commenting creates visual noise.
- **Bad**: `count += 1  # Increment count`
- **Good**: `count += 1  # Account for the off-by-one offset in the upstream API`

## Avoid Hiding Bad Code
If logic is complex or obscure, try to refactor it first (e.g., extract variables, rename functions). Only comment if it remains inherently complex.

## No Commented-out Code
Do not commit dead code. Version control handles history. The only exception is a temporary measure (like disabling a feature due to an upstream bug that will be fixed soon).

## Special Markers (Team Communication)
- `TODO`: Pending tasks/features.
- `FIXME`: Problematic or ugly code needing refactoring.
- `NOTE`: Needs discussion or further investigation.
- `XXX`: Badly needs refactoring (e.g., should switch by core type).
- `HACK`: Temporary code to force inflexible functionality or workaround a known problem.
- `FAQ`: Interesting areas requiring external explanation.
