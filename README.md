# Patch OpenAI

*Insert caching and logging directly into the OpenAI package source.*

## Usage

Patch the source:

    python -m patch

This will:

* Find the `request` method and insert a `request_without_cache` method and a
  `request_with_cache` replacement.
* Cache all invocations int `/cache` folder, unless `stream=True`.
* Cache all request and response data, *including API key*.

Undo changes:

    python -m restore

This will restore a backup of the original source file.

## License

MIT
