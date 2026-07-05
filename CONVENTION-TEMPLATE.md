# Council Convention -- Template

Copy this file to `.council-convention.md` in your project root and edit the
values below. The council reads it to learn your domain, your cross-vendor
command, where to file verdicts, and how heavy a panel to convene by default.

Everything here is yours to change. The template ships with safe, generic
defaults; replace them with what fits your project.

---

## Domain seats

The eight core seats (Analyst, Contrarian, Empiricist, Cross-vendor, Advocate,
Red team, Historian, Pragmatist) are always available. Add domain seats here
when your project has a recurring lens the core roster does not cover. Give each
a name and a one-line charter -- what it is responsible for looking at.

```
# domain-seats:
#   SECURITY:   review authz, secrets handling, and data-exposure surface.
#   PERF:       re-derive latency / throughput / cost claims from benchmarks.
#   COMPLIANCE: check the change against policy, license, and retention rules.
```

(Delete the ones you do not need. Leave this section empty to run core seats
only.)

---

## Cross-vendor CLI command

The cross-vendor seat runs on a DIFFERENT model family to break same-DNA bias.
Put the exact shell command that invokes your second-vendor CLI here. It should
accept a prompt and return the seat's argument on stdout.

```
# cross-vendor-cmd: <your-second-vendor-cli> <args>   (a different model family's CLI that reads a prompt and returns text on stdout)
```

If you have no second vendor available, leave this blank and the council will
note that the cross-vendor seat could not be seated.

---

## Where to save verdicts

Directory (project-relative) where the Chair writes each verdict scaffold. One
file per decision. Create the directory if it does not exist.

```
# verdict-dir: council/verdicts/
```

---

## Default panel weight

How heavy a panel to convene when the caller does not specify. Heavier weights
seat more of the roster. Match this to your project's typical stakes.

```
# default-weight: standard
```

Valid weights:

- `routine`      -- small panel; low-blast-radius questions.
- `standard`     -- the everyday default.
- `heavy`        -- most of the roster; expensive-to-reverse decisions.
- `irreversible` -- the full board; deletes, migrations, history rewrites.

---

## Notes

- Keep this file ASCII-only and free of secrets. It is checked into the repo.
- The council recommends; you ratify. Nothing configured here changes that.
