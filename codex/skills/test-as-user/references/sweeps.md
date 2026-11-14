# Sweeps

The sweepers read this file in step 6. Each sweep is a script that you first run against a known violation and watch go red. Read every screenshot that a sweep takes.

On a URL that may be production, sweep only steps that change nothing, unless the user says otherwise in the session. The input, destructive and revoke sweeps below then run only on a sandbox install, or are listed as not reached.

## Forced states

Force these states on each screen and command of the journeys:

- empty
- slow (3 s and 15 s)
- failed (a 500, an HTML 502 page)
- offline
- an expired session
- a missing permission

Read what the person sees. These rules apply:

- Every state names what happened and gives a next step, in the reader's language.
- No stack trace or raw error code reaches the person.
- A screen never shows a number or a verdict that it did not measure: "0" while loading, "nothing found" when the data was withheld, success after a failure.

## Input

- Submit every form on a journey with its default values through the real browser, so the browser's own validation (`pattern`, `required`, `min`, `max`, `type`) is part of the test.
- Then submit it empty, with junk, out of range and with a future date. Also try the other decimal separator, a duplicate, non-ASCII text and a very long string.
- Send the same values to the API, because agents and scripts send what forms block.
- Bad input must be refused with the field named, and the person's input must stay in the form.

## Destructive actions

List every action that deletes, overwrites, sends, pays, publishes or revokes, on every surface. Run them only on test data. For each one, check these points:

- The confirmation names the object and the result.
- There is undo, a recovery window or a dry run.
- A call without a terminal refuses unless it has an explicit flag.
- After the action, you can get the data back, or the confirmation said that you cannot.

Then walk from the state that each one leaves (no profile, no passkey left, signed out). Every screen still names a next step, and every way in has a way out.

## Layout and access

Take every screen at 320, 390, 820 and desktop width, in every shipped language and theme. Use touch emulation for the phone widths.

- No sideways scroll, and no text that runs past its own box.
- Every action is in view and works without hover.
- Touch targets are at least 24 by 24 CSS pixels (WCAG 2.2 AA). A target under 44 or 48 pixels breaks platform guidance and is a minor finding.
- A script finishes each core journey with the keyboard alone, and focus stays visible and follows the reading order. A core journey that the keyboard cannot finish is a blocker.
- Every control has a name. Run an axe scan in each theme. Zoom text to 200%. Honour reduced motion.
- Each screen has one `h1`, a `main` landmark and a heading outline, as the stand-in for a screen reader.

## Language

- Every shipped language file has the same keys.
- No screen in another language shows untranslated text or raw codes.
- Plural forms work with 0, 1, 2, 5 and 21.
- Dates and numbers follow each locale.
- A right-to-left language, if one ships, lays out right to left.

## Agent surfaces

- **CLI.** From a clean home folder, run it with no arguments, with a mistyped command, with a setting missing, with no network and with its output piped. Read stdout, stderr and the exit code apart.
- **HTTP API.** Run every documented example exactly as written, then with no auth and with a wrong key.
- **MCP.** List the tools with a client such as the MCP Inspector's CLI mode. Give an agent client a few realistic goals, each with one answer you can check. Start that client only through the launcher rule in step 3. Otherwise call the tools with the scripted client and list the agent-driven goals as not reached. Revoke its key and expect a clear error.

## Cross-surface truth

For each main job, ask the same question through every surface on the same data: counts, dates, units, what is withheld and why. A difference is a finding even when each side looks right alone.

## Promises

- Every navigation item and button either works or says plainly, without hover, that it is not available.
- No roadmap marker or plan chip shows in the shipped product.
- The version that the product shows matches the release.
