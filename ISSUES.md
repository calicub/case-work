# Issues & Enhancements

Backlog of known problems and possible improvements for the case-work setup that aren't worth handling right now. Not part of the published Zensical site (lives outside `docs/`).

## Issues

- **Zensical link validation noise (~70 errors on startup)** — Log snippets pasted into case notes contain raw URLs, which Zensical's markdown parser tries to resolve as relative doc links, producing broken-link errors on every build/serve. Non-blocking (doesn't affect rendering or output), but clutters the terminal.
  - Root cause: bare URLs in prose/log blocks aren't fenced or wrapped as autolinks (`<https://...>`).
  - Proper fix: wrap log snippets in fenced code blocks (already convention per `docs/pkb/markdown.md`) and/or wrap inline URLs in `<...>`.
  - Lazy fix (chosen for now, not yet applied): disable link validation globally in `zensical.toml`:
    ```toml
    [project.validation.links]
    not_found = "ignore"
    ```
    Zensical only supports on/off per check (no per-folder/per-file scoping, unlike MkDocs' warn/ignore levels), so this silences the noise everywhere, not just in note sections with logs. Acceptable since real internal links are rarely used in the affected sections.
  - Update 2026-07-02: majority of errors traced to the case description block. Fixed at the source — `.foam/templates/case.md` now wraps the description tab stop (`${5:Describe the issue}`) in a fenced ` ```text ` block inside the `!!! quote "Case Description"` admonition, so pasted log snippets/URLs are inert to link parsing. Applies to new cases only; existing case notes still need the same fencing if their errors should go away too. The global `not_found = "ignore"` toggle above is still not applied — may now be unnecessary if remaining errors are low after this fix.
  - Added: 2026-07-02

## Enhancements

