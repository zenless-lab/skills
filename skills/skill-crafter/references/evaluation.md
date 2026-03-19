# Evaluating and Iterating Skills

Skills must be validated for both **activation accuracy** (does it trigger?) and **output quality** (does it work?). Evaluation strategies can range from manual sanity checks to automated scripting depending on the agent environment you use.

## Testing Trigger Rates (Description Accuracy)
Once you have drafted your `description` following best practices, you must test if it actually triggers the skill in practice.

1. **Design Test Queries:** Write ~10-20 user prompts.
   - Half should clearly require the skill.
   - Half should be near-misses (e.g., mention similar concepts but require a different approach) that should *not* trigger the skill.
2. **Execute:**
   - *Manual Approach:* Open a new chat session with your agent and paste the query. Observe if the agent explicitly activates or references the skill.
   - *Automated Approach:* Script the execution of these queries via your agent's CLI/API and parse the logs to detect skill activation.
3. **Optimize:**
   - If should-trigger queries fail, broaden the scope of the `description`.
   - If shouldn't-trigger queries falsely activate, add specific exclusions.

## Evaluating Output Quality
Check if the skill actually improves the agent's work when it does trigger.

### The Eval Loop
1. **Define Test Cases:** Create a set of realistic user prompts, expected outputs, and any required input files.
2. **Run Baselines:** Run the prompt through the agent *without* the skill enabled, then *with* the skill (use a fresh session for each).
3. **Write Assertions:** Define objective, verifiable pass/fail rules (e.g., "The output file is valid JSON", "The chart has labeled axes").
4. **Grade Outputs:** Evaluate the outputs against the assertions. This can be done by:
   - *Manual Inspection:* Review the files directly.
   - *LLM Judge:* Pass the outputs to an LLM script with a prompt to grade PASS/FAIL.
   - *Verification Script:* Write a Python/Bash script to assert file existence/format.
5. **Analyze & Iterate:**
   - Did the skill improve the success rate compared to the baseline?
   - Look at execution transcripts: If the agent ignored instructions, they are too vague. If it performed unproductive steps, the instructions are too bloated.
   - Refine the `SKILL.md` instructions or extract repetitive logic into `scripts/`.
