import inspect
from pathlib import Path
import re

import openai

# Read the contents of the APIRequestor class
path = Path(inspect.getfile(openai.api_requestor.APIRequestor))
with path.open("r") as f:
    contents = f.read()

# Check if the method has already been patched
if 'request_without_cache' in contents:
    raise RuntimeError("Already patched")

# Find the request method. Take the method signature and indentation
match = re.search(r"([ \t]+)(def request[^.]+]:)", contents, re.MULTILINE | re.DOTALL)
if match is None:
    raise RuntimeError("Method signature not found")
indent, signature = match.groups()
without_cache = signature.replace("request(", "request_without_cache(")

# Read the contents of helper.py, containing the caching logic
with Path("helper.py").open() as f:
    helper = f.read()
helper = helper[helper.index("def"):]
helper = helper.replace(" " * 4, indent).replace("\n", "\n" + indent)

# Prepare the code to be inserted
replacement = f"""
{indent}{helper}

{indent}def request(self, *args, **kwargs):
{indent}{indent}if kwargs["stream"]:
{indent}{indent}{indent}return self.request_without_cache(*args, **kwargs)
{indent}{indent}return self.request_with_cache(*args, **kwargs)

{indent}{without_cache}
""".strip()

# Insert the code and write to disk
with path.open("w") as f:
    f.write(contents.replace(signature, replacement))
