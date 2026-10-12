# Contributing

Describe the problem, reproduction, and expected behavior in an Issue. Small fixes may go directly to a Pull Request; changes to record formats, public interfaces, or responsibility boundaries should first explain consumers, compatibility, and verification conditions.

## Local checks

Python 3.12+ and Node.js are required. Prepare panel/I/O dependencies in a separate virtual environment:

```sh
python -m venv .venv
```

Use `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on POSIX, installing `plugins/gamecaden/scripts/requirements.txt` with that interpreter. Run from the repository root:

```sh
python scripts/check.py --suite all
```

Choose smaller suites according to impact as described in the [validation history](docs/validation.md). Retain commands, environment, and results, including checks that could not run. A release still requires the full suite.

## Authoring and language compatibility

English is the authoritative development and maintenance language for code interfaces, schemas, Skill bodies, shared contracts, material references, and templates. Update the actual English source when behavior changes rather than maintaining separate language-specific rule branches. Public English and Chinese usage guides explain the same package; complete Chinese rule comparisons are local review material and are not published.

The toolkit's authoring language is separate from the user's material language. New project documents default to the user's current language unless explicitly chosen otherwise; localize headings, labels, table headers, prompts, and prose, retaining executable identifiers. Maintain existing documents in their language unless conversion is requested. The [workspace language convention](plugins/gamecaden/shared/workspace.md#6-language-preferences) is authoritative. Avoid parsers that require one natural language's headings. Preserve UTF-8 content, Unicode titles, and original record identities; localized fixtures test compatibility rather than define an English-only output format.

## Contributions and releases

`main` holds checked public versions; unfinished development uses separate branches. Increase the version when plugin content changes and synchronize all three manifests. Released tags and same-version packages are immutable. Default-branch users receive changes through update commands; pinned-tag users choose the next version explicitly.

- Keep the public plugin separate from maintenance tests: `plugins/gamecaden/`, `tests/`, and `scripts/` have distinct responsibilities.
- Describe the problem, resulting behavior, compatibility, and actual verification; update related contracts alongside implementation.
- Use anonymous fixtures. Never commit connection data, real project records, machine-specific paths, private history, or local Chinese rule comparisons.
- Preserve third-party licenses and attribution. Test success does not imply user acceptance or runtime adoption.

The project uses [MIT](LICENSE). Contributions must have rights compatible with that license; third-party materials retain their own licenses.
