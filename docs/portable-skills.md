# Portable skills

Waypoint's Skills page catalogs skill packages that can be used with Pi, Codex and Claude Code. Use the [Agent Skills format](https://agentskills.io/specification): a directory containing `SKILL.md`, with any scripts, references and assets alongside it

```text
code-review/
├── SKILL.md
├── references/
└── scripts/
```

```markdown
---
name: code-review
description: Review changes for correctness and security. Use when reviewing a diff or pull request
---

# Code review

Read the changed files and check their callers before reviewing the diff
Resolve references and scripts relative to this skill directory
```

Keep the instructions independent of a particular tool's names or configuration paths. Declare genuine environment requirements in the optional `compatibility` frontmatter field

## Add and install

Add the Git repository, repository subdirectory or HTTPS archive through the Skills page. Open the skill's **How to Use** tab and choose your coding harness. Pi is the default choice. Run the generated command from the project where you want the skill installed and select the skill when prompted

The installer uses a pinned Skills CLI release and copies the files, so temporary downloads can be removed without breaking installed skills. Repository subdirectories use the repository's default branch. Archive commands verify the registered SHA-256 checksum when present and reject oversized archives, duplicate paths, traversal paths and symbolic links before extraction. Register a checksum for archives you distribute

Review the skill instructions and all bundled scripts before installing or granting project trust. Installation does not execute the skill's bundled scripts, but using the skill can cause your coding agent to run them

Private repositories use your existing Git credentials. Waypoint's API key is not included in installation commands. Direct source installation does not require enabling the public skills index or publishing other stored skills. A key's permission to see registry metadata does not grant access to a private source repository

## Use in Pi

Pi discovers project skills in `.agents/skills/` and user-wide skills in `~/.agents/skills/`. You can also manually place a reviewed skill folder in either location

Run `/reload` in an existing Pi session, then invoke `/skill:code-review`. Use the name declared in the installed `SKILL.md`, which may differ from the registry's display name. Pi also advertises the skill's description for automatic selection when a task matches

Choose **Claude Code** in the same tab to use the existing marketplace installation and setup instructions
