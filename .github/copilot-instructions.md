# GitHub Copilot — Workspace Instructions

Keep responses short, actionable, and link-first. The canonical developer guide is
`AGENTS.md` and the quick build/run instructions are in `README.md`.

Quick build & test
- Quick build (Unix/macOS): `./clean_build.sh`
- Manual build:
```
git submodule update --init --recursive
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug -GNinja
cmake --build . --parallel
ctest --verbose
```

Where to look
- Source: `src/`
- Tests: `src/test/unittests/`
- CMake options: `CMakeLists.txt` (see root for common `-D` flags)

Conventions (short)
- 4-space indent, LF, UTF-8
- Namespace: `inputleap::`; `#pragma once` in headers
- Class PascalCase, function camelCase, private members `m_`

How the assistant should help
- Prefer small, focused patches and link to existing docs.
- Don’t reformat unrelated files or add large unrelated changes.
- When suggesting code, follow the project's C++ style and CMake usage.

Example prompts
- "Create a unit test for X in `src/test/unittests/` following project conventions."
- "Patch the CMakeLists to add option Y with minimal changes."

See AGENTS.md and README.md for full details and communication channels.
