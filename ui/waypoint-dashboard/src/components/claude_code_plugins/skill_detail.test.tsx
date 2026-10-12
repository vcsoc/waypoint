import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { Plugin } from "./types";
import userEvent from "@testing-library/user-event";
import { PORTABLE_SKILLS_CLI, formatInstallCommand } from "./helpers";

import SkillDetail from "./skill_detail";

const buildSkill = (source: Plugin["source"]): Plugin => ({
  id: "plugin-id",
  name: "my-skill",
  source,
  enabled: true,
  version: null,
  description: null,
  created_at: null,
  updated_at: null,
});

describe("SkillDetail source", () => {
  it("installs with Pi by default, changes harness commands, and retains Claude Code setup", async () => {
    const user = userEvent.setup();
    const skill = buildSkill({ source: "github", repo: "org/repo" });
    render(<SkillDetail skill={skill} onBack={vi.fn()} />);
    await user.click(screen.getByText("How to Use"));
    expect(screen.getByRole("combobox", { name: "Coding harness" })).toHaveValue("pi");
    expect(screen.getByText(/Pi discovers project skills/)).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Copy" }));
    expect(await navigator.clipboard.readText()).toBe(`${PORTABLE_SKILLS_CLI} add 'org/repo' --agent pi --copy`);
    await user.selectOptions(screen.getByRole("combobox"), "codex");
    await user.click(screen.getByRole("button", { name: /Copied|Copy/ }));
    expect(await navigator.clipboard.readText()).toContain("--agent codex --copy");
    await user.selectOptions(screen.getByRole("combobox"), "claude-code");
    expect(screen.getByText(formatInstallCommand(skill))).toBeInTheDocument();
    await user.click(screen.getByText("See one-time setup"));
    expect(screen.getByRole("heading", { name: "One-time marketplace setup" })).toBeInTheDocument();
  });

  it("does not offer unsafe archive installation and explains missing checksums", async () => {
    const user = userEvent.setup();
    render(<SkillDetail skill={buildSkill({ source: "archive", url: "http://example.test/skill.zip" })} onBack={vi.fn()} />);
    await user.click(screen.getByText("How to Use"));
    expect(screen.getByText(/cannot generate a safe install command/)).toBeInTheDocument();
    expect(screen.getByText(/No archive checksum/)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Copy" })).not.toBeInTheDocument();
  });
  it("renders a skill whose API metadata is null", () => {
    render(
      <SkillDetail
        skill={{ ...buildSkill({ source: "github", repo: "org/repo" }), keywords: null, author: null, category: null }}
        onBack={vi.fn()}
      />,
    );
    expect(screen.getByRole("heading", { name: "my-skill" })).toBeInTheDocument();
    expect(screen.getByText("Public")).toBeInTheDocument();
  });

  it("links a github source to the repository", () => {
    render(<SkillDetail skill={buildSkill({ source: "github", repo: "org/repo" })} onBack={vi.fn()} />);
    expect(screen.getByRole("link", { name: "github.com/org/repo" })).toHaveAttribute(
      "href",
      "https://github.com/org/repo",
    );
  });

  it("renders an ssh clone url as plain text instead of an unusable link", () => {
    render(
      <SkillDetail skill={buildSkill({ source: "url", url: "git@ghe.example.com:org/repo.git" })} onBack={vi.fn()} />,
    );
    expect(screen.getByText("git@ghe.example.com:org/repo.git")).toBeInTheDocument();
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
  });

  it("renders an ssh git-subdir source as plain text without a tree path", () => {
    render(
      <SkillDetail
        skill={buildSkill({ source: "git-subdir", url: "git@ghe.example.com:org/repo.git", path: "plugins/x" })}
        onBack={vi.fn()}
      />,
    );
    expect(screen.getByText("git@ghe.example.com:org/repo.git @ plugins/x")).toBeInTheDocument();
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
  });
});
