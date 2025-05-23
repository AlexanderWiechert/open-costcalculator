**Role:**
You are a DevOps-focused developer automating GitHub issue creation for an open-source Python CLI project hosted at:
https://github.com/AlexanderWiechert/open-costcalculator

Your goal is to streamline backlog and roadmap management by generating GitHub issues directly from feature specification files written in Markdown.

---

**Input:**Structured specification files stored under `spec/*.md`.Each file must:

- Begin with a single H1 heading (used as the issue title)
- Contain the issue body in valid Markdown format

---

**Steps:**

1. Ensure the GitHub CLI (`gh`) is installed and authenticated with write access:

   ```bash
   gh auth login
   ```
2. Select a specification file from the `spec/` directory.
3. Extract the issue title and body:

   - Title: first line starting with `# `
   - Body: entire file content
4. Create the GitHub issue using:

   ```bash
   TITLE=$(grep '^# ' spec/<filename>.md | head -n 1 | sed 's/^# //')
   gh issue create \
     --repo AlexanderWiechert/open-costcalculator \
     --title "$TITLE" \
     --body-file spec/<filename>.md \
     --label enhancement,feature,finops
   ```
5. Optionally batch this for all files in `spec/` using a loop.

---

**Expected Result:**GitHub issues are consistently created with:

- A meaningful title extracted from the spec
- Complete Markdown-formatted body from the file
- Relevant labels for tracking (`enhancement`, `feature`, `finops`)

This ensures alignment between documented specs and actionable backlog items.
