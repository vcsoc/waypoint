/**
 * Helper utilities for Claude Code Marketplace
 */

import type { Plugin, PluginSource } from "./types";

export interface SkillSourcePreview {
  parsed: PluginSource;
  label: string;
  suggestedName: string;
}

export const SUBDIR_PATH_REGEX = /^(?!\.{1,2}(?:\/|$))[a-zA-Z0-9._-]+(?:\/(?!\.{1,2}(?:\/|$))[a-zA-Z0-9._-]+)*$/;

export const normalizeSubPath = (subPath: string): string => subPath.trim().replace(/\/+$/, "");

export const isValidSubPath = (subPath: string): boolean => {
  const normalized = normalizeSubPath(subPath);
  return normalized !== "" && SUBDIR_PATH_REGEX.test(normalized);
};

const GITHUB_HOST = "github.com";

const SKILL_FILE_EXTENSION_REGEX = /\.(md|markdown|txt|json|ya?ml|toml)$/i;

const ZIP_ARCHIVE_REGEX = /\.zip$/i;

export const SHA256_REGEX = /^[0-9a-fA-F]{64}$/;

export const isValidSha256 = (digest: string): boolean => digest.trim() === "" || SHA256_REGEX.test(digest.trim());

// WHATWG normalizes obfuscated IPv4 (e.g. 2130706433, 0x7f.0.0.1) to dotted-decimal on https, so
// this catches every IPv4 form there; on a non-special scheme like ssh it catches the dotted form
// only. Bracketed IPv6 is rejected separately.
const IPV4_HOST_REGEX = /^\d{1,3}(\.\d{1,3}){3}$/;

const GITHUB_ORG_REGEX = /^[A-Za-z0-9-]+$/;
const GITHUB_REPO_REGEX = /^[A-Za-z0-9._-]+$/;

const BROWSABLE_URL_REGEX = /^https?:\/\//i;
const SSH_SCHEME = "ssh://";
const SSH_SCP_REGEX = /^([a-z0-9._-]+)@([^:/@]+):(?!\/)(.+)$/i;

const buildRepoUrl = (url: URL): string => `${url.protocol}//${url.host}${url.pathname.replace(/\/+$/, "")}`;

const pathSegments = (url: URL): string[] => url.pathname.split("/").filter((seg) => seg !== "");

const toUrl = (candidate: string): URL | null => {
  try {
    return new URL(candidate);
  } catch {
    return null;
  }
};

/** One host rule for every scheme, so an ssh remote is neither more nor less trusted than its https twin. */
const isSafeHost = (url: URL): boolean =>
  url.hostname.includes(".") && !url.hostname.startsWith("[") && !IPV4_HOST_REGEX.test(url.hostname);

/**
 * Validate and normalize a repository URL into a parsed URL, or null. Enforces https (rejects
 * http/ssh/git/etc.), rejects embedded credentials, and requires a dotted host, so the public
 * skill feeds never serve an insecure or credentialed clone URL. Everything downstream parses
 * this normalized object rather than the raw string.
 */
const parseRepoUrl = (raw: string): URL | null => {
  const trimmed = raw.trim();
  if (trimmed === "" || trimmed.startsWith("//")) {
    return null;
  }
  const withScheme = /^[a-z][a-z0-9+.-]*:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
  const url = toUrl(withScheme);
  if (!url || url.protocol !== "https:" || url.username !== "" || url.password !== "" || !isSafeHost(url)) {
    return null;
  }
  return url;
};

const lastSegment = (path: string): string => {
  const segments = path.split("/").filter((seg) => seg !== "");
  return segments[segments.length - 1] ?? "";
};

const toKebabCase = (value: string): string =>
  value
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-+|-+$/g, "");

const parseGitHubSource = (url: URL, subPath?: string): SkillSourcePreview | null => {
  const parts = pathSegments(url);
  if (parts.length < 2) {
    return null;
  }

  const org = parts[0];
  const repoBase = parts[1].replace(/\.git$/, "");
  if (!GITHUB_ORG_REGEX.test(org) || !GITHUB_REPO_REGEX.test(repoBase)) {
    return null;
  }
  const repoFull = `${org}/${repoBase}`;
  const repoUrl = `https://github.com/${repoFull}`;
  const repoPreview: SkillSourcePreview = {
    parsed: { source: "github", repo: repoFull },
    label: `GitHub repo — ${repoFull}`,
    suggestedName: toKebabCase(repoBase),
  };

  const isTreeOrBlob = parts.length >= 4 && (parts[2] === "tree" || parts[2] === "blob");
  if (isTreeOrBlob) {
    const pathParts = parts.slice(4);
    const last = lastSegment(pathParts.join("/"));
    const effective = SKILL_FILE_EXTENSION_REGEX.test(last) ? pathParts.slice(0, -1) : pathParts;
    if (effective.length === 0) {
      return repoPreview;
    }
    const path = normalizeSubPath(effective.join("/"));
    if (!SUBDIR_PATH_REGEX.test(path)) {
      return null;
    }
    return {
      parsed: { source: "git-subdir", url: repoUrl, path },
      label: `GitHub subdir — ${repoFull} @ ${path}`,
      suggestedName: toKebabCase(lastSegment(path)),
    };
  }

  if (parts.length !== 2) {
    return null;
  }

  const normalized = normalizeSubPath(subPath ?? "");
  if (normalized !== "") {
    if (!SUBDIR_PATH_REGEX.test(normalized)) {
      return null;
    }
    return {
      parsed: { source: "git-subdir", url: repoUrl, path: normalized },
      label: `GitHub subdir — ${repoFull} @ ${normalized}`,
      suggestedName: toKebabCase(lastSegment(normalized)),
    };
  }

  return repoPreview;
};

const buildGitSourcePreview = (
  kind: "Git" | "SSH",
  repoUrl: string,
  repoName: string,
  subPath?: string,
): SkillSourcePreview | null => {
  const normalized = normalizeSubPath(subPath ?? "");
  if (normalized !== "") {
    if (!SUBDIR_PATH_REGEX.test(normalized)) {
      return null;
    }
    return {
      parsed: { source: "git-subdir", url: repoUrl, path: normalized },
      label: `${kind} subdir — ${repoUrl} @ ${normalized}`,
      suggestedName: toKebabCase(lastSegment(normalized)),
    };
  }

  return {
    parsed: { source: "url", url: repoUrl },
    label: `${kind} repo — ${repoUrl}`,
    suggestedName: toKebabCase(repoName),
  };
};

const parseRawGitSource = (url: URL, subPath?: string): SkillSourcePreview | null => {
  if (pathSegments(url).length < 2) {
    return null;
  }
  const repoName = lastSegment(url.pathname).replace(/\.git$/, "");
  return buildGitSourcePreview("Git", buildRepoUrl(url), repoName, subPath);
};

/**
 * Parse an scp-style `git@host:org/repo` or `ssh://git@host/org/repo` clone URL, registering it
 * exactly as typed: git treats the `.git` suffix as optional, and forcing one on breaks hosts whose
 * paths are not `org/repo`, like Azure DevOps `v3/...` and CodeCommit `v1/repos/...`. The scp form is
 * rewritten to `ssh://` only to reuse the https host and credential rules, and only a URL that
 * survives that round trip unchanged is accepted, which keeps traversal segments off the feed.
 */
const parseSshSource = (raw: string, subPath?: string): SkillSourcePreview | null => {
  const trimmed = raw.trim();
  const scp = SSH_SCP_REGEX.exec(trimmed);
  const candidate = scp ? `${SSH_SCHEME}${scp[1]}@${scp[2]}/${scp[3]}` : trimmed;
  if (!candidate.toLowerCase().startsWith(SSH_SCHEME)) {
    return null;
  }
  const url = toUrl(candidate);
  if (!url || url.username === "" || url.password !== "" || !isSafeHost(url)) {
    return null;
  }
  const pathStart = candidate.indexOf("/", SSH_SCHEME.length);
  if (pathStart === -1 || url.pathname !== candidate.slice(pathStart) || pathSegments(url).length < 2) {
    return null;
  }
  return buildGitSourcePreview("SSH", trimmed, lastSegment(url.pathname).replace(/\.git$/i, ""), subPath);
};

const parseArchiveSource = (url: URL): SkillSourcePreview => ({
  parsed: { source: "archive", url: url.href },
  label: `Zip archive — ${url.host}${url.pathname}`,
  suggestedName: toKebabCase(lastSegment(url.pathname).replace(ZIP_ARCHIVE_REGEX, "")),
});

/**
 * Parse any git-accessible repository URL or https zip archive URL into a registerable skill
 * source. A `.zip` path is an `archive` source (S3, Artifactory, any static host). GitHub URLs
 * keep their `github`/`git-subdir` shorthand; ssh clone URLs stay ssh so a private host
 * authenticates with the user's own key; every other host is treated as a raw repo URL,
 * with an optional subfolder turning it into git-subdir.
 */
export const parseSkillSource = (rawUrl: string, subPath?: string): SkillSourcePreview | null => {
  const ssh = parseSshSource(rawUrl, subPath);
  if (ssh) {
    return ssh;
  }
  const url = parseRepoUrl(rawUrl);
  if (!url) {
    return null;
  }
  if (ZIP_ARCHIVE_REGEX.test(url.pathname)) {
    return parseArchiveSource(url);
  }
  if (url.hostname.replace(/^www\./, "") === GITHUB_HOST) {
    return parseGitHubSource(url, subPath);
  }
  return parseRawGitSource(url, subPath);
};

/**
 * Build the `~/.claude/settings.json` snippet that registers the proxy as a marketplace.
 * Claude Code expects `extraKnownMarketplaces.<name>.source` to be a source object, not a
 * bare `"url"` string, so the url/source pair is nested one level deeper. The key must be
 * "litellm" to match the name the proxy returns in marketplace.json.
 */
export const buildMarketplaceSettingsSnippet = (proxyOrigin: string): string =>
  JSON.stringify(
    {
      extraKnownMarketplaces: {
        litellm: {
          source: {
            source: "url",
            url: `${proxyOrigin}/claude-code/marketplace.json`,
          },
        },
      },
    },
    null,
    2,
  );

/**
 * Generate install command for Claude Code CLI.
 * Installs the named plugin from the "litellm" marketplace registered in settings.json.
 */
export const formatInstallCommand = (plugin: { name: string }): string => `/plugin install ${plugin.name}@litellm`;

export const PORTABLE_SKILLS_CLI = "npx --yes skills@1.7.1";
export type SkillHarness = "pi" | "codex" | "claude-code";

const shellQuote = (value: string): string => `'${value.replaceAll("'", "'\\''")}'`;
const safeSubdirectory = (value: string): boolean => SUBDIR_PATH_REGEX.test(value);
const safeGitSource = (value: string): boolean => {
  if (Array.from(value).some((character) => character.charCodeAt(0) < 32 || character.charCodeAt(0) === 127)) return false;
  if (/^git@[a-zA-Z0-9.-]+:[^\s]+$/.test(value)) return true;
  try {
    const url = new URL(value);
    const secureAuthority = ["https:", "ssh:"].includes(url.protocol) && !!url.hostname && !url.password;
    const allowedIdentity = url.protocol === "ssh:" || !url.username;
    return secureAuthority && allowedIdentity;
  } catch {
    return false;
  }
};

const gitSubdirectoryInstall = (source: Plugin["source"], options: string): string | null => {
  if (!source.url || !source.path) return null;
  if (!safeGitSource(source.url) || !safeSubdirectory(source.path)) return null;
  return [
    "(", "  set -eu", "  work=$(mktemp -d)", "  trap 'rm -rf -- \"$work\"' EXIT",
    `  git clone --depth 1 -- ${shellQuote(source.url)} "$work/repo"`,
    `  ${PORTABLE_SKILLS_CLI} add "$work/repo"/${shellQuote(source.path)} ${options}`, ")",
  ].join("\n");
};

const archiveInstall = (source: Plugin["source"], options: string): string | null => {
  if (!source.url) return null;
  try {
    const url = new URL(source.url);
    const secureAuthority = url.protocol === "https:" && !!url.hostname;
    const hasCredentials = !!url.username || !!url.password;
    if (!secureAuthority || hasCredentials) return null;
  } catch {
    return null;
  }
  if (source.sha256 && !/^[a-fA-F0-9]{64}$/.test(source.sha256)) return null;
  const verify = source.sha256
    ? [`  printf '%s  %s\\n' ${shellQuote(source.sha256)} "$work/skill.zip" | sha256sum --check -`]
    : [];
  return [
    "(", "  set -eu", "  work=$(mktemp -d)", "  trap 'rm -rf -- \"$work\"' EXIT",
    `  curl --fail --location --proto '=https' --proto-redir '=https' --max-filesize 10485760 --output "$work/skill.zip" ${shellQuote(source.url)}`,
    ...verify,
    '  python3 - "$work/skill.zip" "$work/skill" <<\'PY\'',
    "from pathlib import PurePosixPath",
    "from stat import S_ISLNK",
    "from zipfile import ZipFile",
    "import sys",
    "with ZipFile(sys.argv[1]) as archive:",
    "    entries = tuple(archive.infolist())",
    "    if len(entries) > 1000 or sum(entry.file_size for entry in entries) > 33554432:",
    "        raise SystemExit('Skill archive exceeds extraction limits')",
    "    names = tuple(PurePosixPath(entry.filename).as_posix() for entry in entries)",
    "    if len(names) != len(frozenset(names)):",
    "        raise SystemExit('Skill archive contains duplicate paths')",
    "    for entry in entries:",
    "        path = PurePosixPath(entry.filename)",
    "        if path.is_absolute() or '..' in path.parts or '\\\\' in entry.filename or S_ISLNK(entry.external_attr >> 16):",
    "            raise SystemExit('Skill archive contains unsafe paths')",
    "    archive.extractall(sys.argv[2])",
    "PY",
    `  ${PORTABLE_SKILLS_CLI} add "$work/skill" ${options}`, ")",
  ].join("\n");
};

export const formatPortableInstallCommand = (source: Plugin["source"], harness: SkillHarness): string | null => {
  const install = `${PORTABLE_SKILLS_CLI} add`;
  const options = `--agent ${harness} --copy`;
  switch (source.source) {
    case "github":
      return source.repo && /^[a-zA-Z0-9][a-zA-Z0-9_.-]*\/[a-zA-Z0-9_.-]+$/.test(source.repo)
        ? `${install} ${shellQuote(source.repo)} ${options}` : null;
    case "url":
      return source.url && safeGitSource(source.url) ? `${install} ${shellQuote(source.url)} ${options}` : null;
    case "git-subdir":
      return gitSubdirectoryInstall(source, options);
    case "archive":
      return archiveInstall(source, options);
    default:
      return null;
  }
};

/**
 * Validate plugin name format (kebab-case)
 * Must be lowercase letters, numbers, and hyphens only
 */
export const validatePluginName = (name: string): boolean => {
  if (!name || name.trim() === "") {
    return false;
  }
  // Regex: lowercase letters, numbers, hyphens
  return /^[a-z0-9-]+$/.test(name);
};

/**
 * Get human-readable source display text
 */
export const getSourceDisplayText = (source: Plugin["source"]): string => {
  if (source.source === "github" && source.repo) {
    return `GitHub: ${source.repo}`;
  }
  if (source.source === "git-subdir" && source.url && source.path) {
    return `${source.url} @ ${source.path}`;
  }
  if ((source.source === "url" || source.source === "archive") && source.url) {
    return source.url;
  }
  return "Unknown source";
};

/**
 * Get clickable link for plugin source. Ssh clone urls are not browsable, so they yield null.
 */
export const getSourceLink = (source: Plugin["source"]): string | null => {
  if (source.source === "github" && source.repo) {
    return `https://github.com/${source.repo}`;
  }
  const linksToUrl = source.source === "url" || source.source === "git-subdir" || source.source === "archive";
  return linksToUrl && source.url && BROWSABLE_URL_REGEX.test(source.url) ? source.url : null;
};

/**
 * Get badge color based on category
 */
export const getCategoryBadgeColor = (
  category?: string | null,
): "blue" | "green" | "purple" | "red" | "orange" | "yellow" | "gray" => {
  if (!category) {
    return "gray";
  }

  const categoryLower = category.toLowerCase();

  if (categoryLower.includes("development") || categoryLower.includes("dev")) {
    return "blue";
  } else if (categoryLower.includes("productivity") || categoryLower.includes("workflow")) {
    return "green";
  } else if (categoryLower.includes("learning") || categoryLower.includes("education")) {
    return "purple";
  } else if (categoryLower.includes("security") || categoryLower.includes("safety")) {
    return "red";
  } else if (categoryLower.includes("data") || categoryLower.includes("analytics")) {
    return "orange";
  } else if (categoryLower.includes("integration") || categoryLower.includes("api")) {
    return "yellow";
  }

  return "gray";
};

/**
 * Validate semantic version format (basic check)
 */
export const isValidSemanticVersion = (version?: string): boolean => {
  if (!version) {
    return true; // Version is optional
  }

  // Basic semver check: X.Y.Z
  const semverRegex = /^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$/;
  return semverRegex.test(version);
};

/**
 * Validate email format
 */
export const isValidEmail = (email?: string): boolean => {
  if (!email) {
    return true; // Email is optional
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate URL format
 */
export const isValidUrl = (url?: string): boolean => {
  if (!url) {
    return true; // URL is optional
  }

  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

/**
 * Parse keywords from comma-separated string
 */
export const parseKeywords = (keywordsString: string): string[] => {
  if (!keywordsString || keywordsString.trim() === "") {
    return [];
  }

  return keywordsString
    .split(",")
    .map((kw) => kw.trim())
    .filter((kw) => kw !== "");
};
