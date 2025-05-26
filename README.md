repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        args: ["--line-length", "120"]

  - repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.12.0
    hooks:
      - id: isort

---

⚠️ **Wichtig:** Falls `pre-commit` wiederholt `src/main.py` verändert und kein Commit gelingt, führe Folgendes manuell aus:

```bash
black --line-length 120 src/main.py
isort src/main.py
git add src/main.py
git commit --no-verify -m "style: fix import order and formatting after pre-commit"
git push
```

Dieser Schritt verhindert Endlosschleifen durch automatische Formatierungen beim Commit.

TEST