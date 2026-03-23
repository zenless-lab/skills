# Optimizing Skill Descriptions

Use this file when the skill exists but its `description` does not trigger reliably.

## Why this matters

Agents typically see only the skill's `name` and `description` before deciding whether to load the full `SKILL.md`. A weak description causes missed triggers; an over-broad description causes false triggers.

## Description writing rules

- Use imperative phrasing such as "Use this skill when..."
- Focus on user intent rather than internal implementation
- Be slightly pushy but still accurate
- Mention adjacent contexts where the skill applies even if the user does not name the domain directly
- Stay under the 1024-character limit

## Eval design

Build a small trigger-eval set with realistic prompts:

- around 8 to 10 should-trigger prompts
- around 8 to 10 should-not-trigger prompts

Vary these dimensions:

- phrasing
- explicitness
- detail level
- workflow complexity
- casual language, typos, and abbreviations

Prefer near-miss negatives. Weak negatives like unrelated coding questions do not test precision.

## What to measure

For each prompt, record:

- the prompt text
- whether it should trigger
- whether the skill actually triggered
- trigger rate if you run multiple times

Run each prompt multiple times if the client is nondeterministic. Three runs is a reasonable default.

## Optimization loop

1. Evaluate the current description on a train set and a validation set.
2. Identify train-set failures.
3. Revise the description based on intent categories, not one-off keywords.
4. Re-run the evals.
5. Keep the best version by validation performance, not by the last iteration.

## Failure diagnosis

If should-trigger prompts fail:

- the description is probably too narrow
- add user-intent language or missing adjacent contexts

If should-not-trigger prompts fire:

- the description is probably too broad
- clarify boundaries and what the skill is not for

If iterations stall:

- change the structure, not just a few words
- verify the eval set is realistic and properly labeled

## Final checks

- update the `description` in `SKILL.md`
- verify the text still matches the real scope of the skill
- manually sanity-check with a few fresh prompts
