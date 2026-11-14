# Personas, journeys and briefs

The planner reads this file in step 2. Pick the personas and journeys that fit the surfaces in `surfaces.md`, and write a line for each one you skip.

## Personas

A persona sets what the person knows, what they want, which surface they use and how much effort they will spend. Leave out age, job and feelings. They make an agent sound believable without making it more accurate.

- **New user.** Knows only what the landing page or the README says. Has never used the product. Does not know its terms unless a screen explains them.
- **Advanced user.** Has read the docs and the help. Uses the CLI, the API and the settings, and tries every promise the docs make.
- **Self-hoster**, when the product can be self-hosted. Runs it on their own server from the published install docs and keeps it running.
- **Agent user**, when the product has a CLI, an API or an MCP server. A coding agent with a goal and the product's own docs or tool descriptions, and nothing else.

## Budgets

- A new-user journey gets 20 actions. An advanced or self-hoster journey gets 40.
- The same action twice with no visible change ends that attempt.
- A third approach to the same part of the goal ends the journey.
- Every limit that a walk hits is a finding.

These numbers are a starting point. Tune them after the first real runs.

## The basics

Write at least one journey for each basic on every surface that offers it.

1. Install and first run. Type the README or the quick start literally on a clean machine. Use the asset for the walker's platform (arm64 or x86), and record any operating system prompt (Gatekeeper, SmartScreen) that a person must pass.
2. Sign up, sign in and sign out with each method the product offers: password, passkey, OIDC, magic link, recovery codes. Include an expired session and a deep link opened while signed out.
3. Get real data in through each import path, starting from zero data.
4. Do the main jobs, found from the navigation or the help, never from a URL the planner knows.
5. Do the advanced jobs the docs promise: configuration, integrations, automation, export and import, limits.
6. Settings and leaving: export the data, delete what was created, delete the account.
7. Errors and recovery, and the empty state of every screen that a new account lands on.

Add these where the product has them:

- **Self-hosting.** Install with the documented compose file or chart. Set the environment config. Run it behind a reverse proxy and under a subpath. Read the logs when something is wrong and check that they say what. Back up and restore. Upgrade from the last release with existing data. Uninstall, and list what it leaves behind.
- **A second person.** Invite someone, accept the invite, check that a limited role sees the right things, then revoke it.
- **A returning user on a second device.** Sign up at desktop width, then sign in at phone width. Use a passkey made on the first device.
- **Native apps.** Install the desktop or mobile build the way the docs say. Use the iOS Simulator or an Android emulator when no real device is available, and list real devices as not reached.
- **Real-world data.** Import a realistic volume (10,000 rows or more) and messy files: a byte order mark, `;` as the separator, an export from a spreadsheet app.
- **Connecting an agent**, for an MCP server. It takes two walkers. Walker A follows the docs and writes the client config. Walker B starts an agent client with that config and does a real task. When the launcher rule in step 3 leaves no way to start walker B, list the journey as not reached.

## The other two rounds

- **Bad input and failures.** The same goals with bad input, a slow or failed backend, an expired session, a destructive action and the way back from it.
- **Coverage gaps.** Each core journey at phone width and through each agent surface on the same data. Other widths, other languages, themes and keyboard-only use go to the sweeps, not to walks.

## Brief template

Every brief has this shape, plus the walker rules from `walkers.md`. The brief checker rejects one that names a screen, a button, a URL past the entry point or a known issue. The walker rules name none of these, so the checker accepts them.

```text
You are: <what you know, what you want, how much effort you will spend>
Your goal: <the goal in the person's words>
You are done when: <what you have or know at the end>
Start here: <the public entry point: a URL, a package name, a command or a doc page>
Budget: <N actions>. Stop when you reach it, and say so.
Rules: use only what the product shows you. Copy commands exactly. If you need anything the product did not give you, say what and why.
For each step, log: the action, what you expected, what you saw (exact text), and the screenshot path or the command output.
```

Write "You have last month's bank statement as a CSV. Find out what you spent on food." Never write "Click Import, choose CSV". A list of steps tests the list, not the product.
