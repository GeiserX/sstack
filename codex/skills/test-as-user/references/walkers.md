# Walker kits and walker rules

The orchestrator reads this file in steps 3 to 5. It sets what each walker gets, how it must behave, and which blocker to plant for each kit.

## Kits

Each surface gets its own kit. Give a walker only its kit, where the harness lets you set tools. Where it does not, the scorer flags any tool use outside the kit.

| Kit | Gets | Planted blocker for step 4 |
| --- | --- | --- |
| Web | A browser driver with a fresh profile at desktop size. No shell | A primary button that does nothing |
| Phone | The same, with touch emulation (`hasTouch`, `isMobile`, a phone user agent) at phone size | The main action hidden behind hover |
| CLI and install | A shell in the sandbox with a clean home folder, and the published docs in a browser | A wrong command in the README, or a flag that silently does nothing |
| HTTP API | A shell where `curl` is the surface, and the published docs | A documented example that returns an error |
| MCP | An agent client with only the product's MCP server, set up from the docs and started only through the launcher rule in step 3. No browser. Otherwise a scripted client (the MCP Inspector CLI), and the agent-driven goals are not reached | A tool whose description sends the agent the wrong way |
| Docs | The published docs in a browser, and the shell the docs ask for | A quick start step that is missing |
| Email | The fresh mailbox's web inbox, open in the same browser as the Web or Phone kit | A reset or sign-in link that lands on a 404 |
| Native app | The published installer for the walker's platform, and the iOS Simulator or an Android emulator for a phone app | A release asset built for the wrong CPU architecture |

People read docs in a browser while they type in a terminal. A CLI or docs walker with a shell only, and a rule against `curl`, stops at the first doc page.

## Planting

- For a URL target, plant the blocker with request interception or a browser init script instead of a rebuild.
- Plant on the destination as well as on the link. A walker that sees an address as plain text types it and skips a dead link.
- A hover-only plant can be skipped by opening a URL from the accessibility snapshot. The scorer flags that visit, but the plant is not caught until the verifier reproduces it as a finding. When the walker skipped it, plant it where the walker will meet it and walk again.
- For the CLI kit, point the documented clone at a planted local copy with git's `url.insteadOf` in the walker's clean home folder. Add both the `.git` form and the bare form of the URL, or the clone URL ends in `.git.git`.
- Run the verifier inside the planted environment too.

## Starting a walker

- A sub-session that the harness starts for the orchestrator can open in the orchestrator's project, whatever folder you ask for, and then it loads that project's instruction files. Such a sub-session fails the context check in step 3 and cannot walk. Use it only for stages that may read the source. A sub-session that starts outside the repo and passes the check can still walk.
- A headless agent CLI started from a shell with no terminal can wait forever for more input. Close its standard input.
- A headless agent CLI can refuse MCP tool calls when it has nobody to ask. Set the walker's browser server to approve its own tool calls, and no other server.
- For a clean home folder, set `HOME` after the launcher and call the agent binary itself. A launcher or wrapper that reads `HOME` breaks when `HOME` changes first.
- An agent account can carry its own skills and plugins. The harness note tells the walker to use none.
- Put anything one walk hands to the next, such as an address or a test login, in the next walker's brief or harness note. A browser-only walker cannot open a local file.
- Start each walk detached from any waiter, so a waiter that times out does not stop the walk. A transcript that ends with a completed turn is a finished walk, even with no exit code.

## Walker rules

Put these rules in every brief, in the walker's own words.

- Act through the accessibility tree, and judge from screenshots. Read every screenshot you take.
- Scroll to an element and take a screenshot before you act on it.
- On a web or phone walk, use the shell only to write your own log.
- Copy every doc command and code block exactly. Never fix a typo, add a flag or fill a gap from memory.
- A workaround is the finding. Reading the source, guessing a URL, or writing `curl`, `grep` or a script to get what the product should give all count. On the API kit, `curl` is the surface.
- Use real clicks, taps, keys and commands. Never call scripts inside the page.
- Close pop-ups and banners as a person would. Report one that blocks the main action.
- When a long operation runs (an import, a sync, a build), check it at several points and reload once. This catches a stuck spinner, a stale count or "complete" shown too early.
- Stop at the budget, and say that you reached it.

## Log

For each step the walker logs one line: the action, what it expected, what it saw (the exact text), and the screenshot path or the command output. Times come from the transcript, never from the walker.
