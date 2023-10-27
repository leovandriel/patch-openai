# Patch OpenAI

*Insert caching and logging directly into the package source.*

## Usage

Patch the source:

    python -m patch

This will:

* Find the `request` method and insert a `request_without_cache` method and a
  `request_with_cache` replacement.
* Cache all invocations int `/cache` folder, unless `stream=True`.
* Cache all request and reponse data, *including API key*.

## License

MIT
