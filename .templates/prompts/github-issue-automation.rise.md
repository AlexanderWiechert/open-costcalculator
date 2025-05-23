You are building an automation process to create GitHub issues for the repository:
https://github.com/AlexanderWiechert/open-costcalculator

The goal is to streamline backlog and roadmap management by automatically generating GitHub issues from structured specification files in `spec/*.md`.

---

## Steps:

1. Ensure GitHub CLI (`gh`) is installed and authenticated:

   ```bash
   gh auth login
   ```
2. From a given `.md` file in `spec/`, extract:

   - `title`: the first Markdown H1 heading (`# …`)
   - `body`: the full content of the file
3. Use the following logic to create an issue dynamically:

   ```bash
   TITLE=$(grep '^# ' spec/<filename>.md | head -n 1 | sed 's/^# //')
   gh issue create \
     --repo AlexanderWiechert/open-costcalculator \
     --title "$TITLE" \
     --body-file spec/<filename>.md \
     --label enhancement,feature,finops
   ```

   Example:

   ```bash
   TITLE=$(grep '^# ' spec/aws-secretsmanager-analyzer.md | head -n 1 | sed 's/^# //')
   gh issue create \
     --repo AlexanderWiechert/open-costcalculator \
     --title "$TITLE" \
     --body-file spec/aws-secretsmanager-analyzer.md \
     --label enhancement,feature,finops
   ```

---

## Expected result:

An issue is created with a meaningful title and full Markdown body from the specification file – fully automatable and consistent across features.
