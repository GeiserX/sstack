# Changelog

## Unreleased

- New skill: `tidy-repo` sweeps an established repo without changing what it does, refreshes the living docs and leaves guards that keep it clean.

## 1.1.0 (2026-11-07)

- Renamed from `agent-skills` to `sstack` (sergio stack). GitHub redirects the old repository URLs; the documentation site moved to https://geiserx.github.io/sstack/.
- Installable as a Claude Code plugin: `/plugin marketplace add GeiserX/sstack`, then `/plugin install sstack@sstack`. Plugin skills are namespaced, as in `/sstack:file-pr`.
- `scripts/install.sh` links the skills (and with `--hooks` the sergio-loop runtime) in one command, replacing the installer that was pasted into the docs. It now also links `sergio_loop_registration.py`, which the SessionStart hook imports.
- New skills: `full-loop` (sergio-loop to done, then refine-loop) and `github-video-embed` (videos that play inline on GitHub).
- `file-pr` no longer requests reviewers and keeps provenance in one References section.
- `eli5`, `help-decide`, `docs-loop` and `refine-loop` trigger on the user rather than one named person.
- The runtime's default accounts folder is now `~/.config/sstack/accounts` (`SERGIO_LOOP_ACCOUNTS_DIR` still overrides it). Point it at your accounts folder, or set the variable, before upgrading.
- The validator checks that every skill has a README row and that the plugin and marketplace versions match.

## 1.0.0

- First tagged release as `agent-skills`.
