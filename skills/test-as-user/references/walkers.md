# Walker kits and walker rules

The orchestrator reads this file in steps 3 to 5. It sets what each walker gets, how it must behave, and which blocker to plant for each kit.

## Kits

Each surface gets its own kit. Give a walker only its kit, where the harness lets you set tools. Where it does not, the scorer flags any tool use outside the kit.

| Kit | Gets | Planted blocker for step 4 |
| --- | --- | --- |
| Web | A browser driver with a fresh profile at desktop size. No shell | A primary button that does nothing |
| Phone | The same, with touch emulation (`hasTouch`, `isMobile`, a phone user agent) at phone size | The main action hidden behind hover |
| CLI and install | A shell in the sandbox with a clean home folder, and the published docs | A wrong command in the README, or a flag that silently does nothing |
| HTTP API | A shell where `curl` is the surface, and the published docs | A documented example that returns an error |
| MCP | An agent client with only the product's MCP server, set up from the docs and started only through the launcher rule in step 3. No browser. Otherwise a scripted client (the MCP Inspector CLI), and the agent-driven goals are not reached | A tool whose description sends the agent the wrong way |
| Docs | The published docs, and the shell the docs ask for | A quick start step that is missing |
| Email | The fresh mailbox's web inbox, open in the same browser as the Web or Phone kit | A reset or sign-in link that lands on a 404 |
| Native app | The published installer for the walker's platform, and the iOS Simulator or an Android emulator for a phone app | A release asset built for the wrong CPU architecture |

For a URL target, plant the blocker with request interception instead of a rebuild.

## Walker rules

Put these rules in every brief, in the walker's own words.

- Act through the accessibility tree, and judge from screenshots. Read every screenshot you take.
- Copy every doc command and code block exactly. Never fix a typo, add a flag or fill a gap from memory.
- A workaround is the finding. Reading the source, guessing a URL, or writing `curl`, `grep` or a script to get what the product should give all count. On the API kit, `curl` is the surface.
- Use real clicks, taps, keys and commands. Never call scripts inside the page.
- Close pop-ups and banners as a person would. Report one that blocks the main action.
- When a long operation runs (an import, a sync, a build), check it at several points and reload once. This catches a stuck spinner, a stale count or "complete" shown too early.
- Stop at the budget, and say that you reached it.

## Log

For each step the walker logs one line: the action, what it expected, what it saw (the exact text), and the screenshot path or the command output. Times come from the transcript, never from the walker.
