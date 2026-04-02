# Input Leap - AI Agent Guide

## Project Overview

Input Leap is a free and open-source software KVM (Keyboard, Video, Mouse) switch that allows users to control multiple computers with a single keyboard and mouse. Move the mouse to the edge of the screen to switch control to a different machine, or use hotkeys to switch focus.

**Key characteristics:**
- Fork of the Barrier project by Barrier's active maintainers
- Cross-platform: Windows 10/11, macOS 10.12+, Linux, FreeBSD, OpenBSD
- GPLv2 licensed
- Clipboard sharing support (not on Linux/Wayland)
- TLS/SSL encryption for secure connections

## Technology Stack

- **Language**: C++ (C++17 for Qt6, C++14 for Qt5)
- **Build System**: CMake (minimum version 3.21)
- **UI Framework**: Qt5 (5.9+) or Qt6 (6.2+)
- **Cryptography**: OpenSSL 1.1.1+
- **Testing**: Google Test/Mock
- **Package Management**: Conan (optional), system packages

## Directory Structure

```
input-leap/
├── src/                    # Source code
│   ├── lib/               # Core libraries
│   │   ├── arch/          # Architecture abstraction (platform detection)
│   │   ├── base/          # Base utilities (logging, events, strings)
│   │   ├── client/        # Client-side logic
│   │   ├── common/        # Common utilities
│   │   ├── inputleap/     # Core application logic
│   │   ├── io/            # I/O utilities
│   │   ├── ipc/           # Inter-process communication
│   │   ├── mt/            # Multi-threading
│   │   ├── net/           # Networking
│   │   ├── platform/      # Platform-specific implementations
│   │   └── server/        # Server-side logic
│   ├── client/            # Client executable (input-leapc)
│   ├── server/            # Server executable (input-leaps)
│   ├── daemon/            # Windows service daemon
│   ├── gui/               # Qt GUI application
│   └── test/              # Test suites
├── cmake/                 # CMake modules
├── dist/                  # Distribution packaging (deb, rpm, wix, etc.)
├── doc/                   # Documentation and man pages
├── res/                   # Resources (icons, translations, etc.)
└── ext/                   # External dependencies (git submodules)
    ├── gtest/             # Google Test
    └── gulrak-filesystem/ # std::filesystem polyfill
```

## Build Instructions

### Prerequisites

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install cmake g++ git ninja-build \
    libssl-dev libxinerama-dev libxrandr-dev libxtst-dev \
    libxkbcommon-dev libglib2.0-dev \
    qt6-base-dev qt6-tools-dev-tools qt6-tools-dev \
    libavahi-compat-libdnssd-dev
```

**macOS:**
```bash
brew install cmake ninja qt@6 openssl
```

**Windows:**
- Visual Studio 2019 or 2022
- Qt 5.15 or 6.x
- Bonjour SDK (for auto-discovery)

### Build Commands

**Quick build (Unix):**
```bash
./clean_build.sh
```

**Manual build:**
```bash
# Initialize submodules
git submodule update --init --recursive

# Configure
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug -GNinja

# Build
cmake --build . --parallel

# Run tests
ctest --verbose
```

**Build Options:**
- `INPUTLEAP_BUILD_GUI=ON/OFF` - Build the GUI (default: ON)
- `INPUTLEAP_BUILD_TESTS=ON/OFF` - Build tests (default: OFF)
- `INPUTLEAP_BUILD_X11=ON/OFF` - Build with X11 support (default: ON)
- `INPUTLEAP_BUILD_LIBEI=ON/OFF` - Build with libei support (default: OFF)
- `QT_DEFAULT_MAJOR_VERSION=5/6` - Qt version (default: 6)
- `INPUTLEAP_USE_EXTERNAL_GTEST=ON/OFF` - Use system gtest (default: OFF)

### Using Conan (optional)

```bash
conan install . --build=missing
cmake --preset conan-release
cmake --build --preset conan-release
```

## Code Style Guidelines

**Formatting (from .editorconfig):**
- Indentation: 4 spaces (no tabs)
- Line endings: LF
- Charset: UTF-8
- Trim trailing whitespace
- Insert final newline

**C++ Conventions:**
- Namespace: `inputleap::`
- Header guards: `#pragma once` (preferred)
- Class naming: PascalCase (e.g., `ClientApp`, `EventQueue`)
- Function naming: camelCase (e.g., `parseArgs()`, `getInstance()`)
- Private members: prefix with `m_` (e.g., `m_client`, `m_serverAddress`)
- Macros: UPPER_CASE with prefix (e.g., `ARCH`, `CLOG`, `LOG_INFO`)

**Example:**
```cpp
namespace inputleap {

class ClientApp {
public:
    ClientApp(IEventQueue* events);
    void parseArgs(int argc, const char* const* argv);
    
private:
    Client* m_client;
    std::string m_serverAddress;
};

} // namespace inputleap
```

**Includes:**
- Group: project headers, then system headers
- Use quotes for project headers (`#include "base/Log.h"`)
- Use angle brackets for system headers (`#include <vector>`)

## Platform Abstraction

The project uses conditional compilation for platform-specific code:

```cpp
#if SYSAPI_WIN32
    // Windows-specific code
#elif SYSAPI_UNIX
    // Unix-specific code
    #if WINAPI_CARBON
        // macOS Carbon
    #elif WINAPI_XWINDOWS
        // Linux/Unix X11
    #elif WINAPI_LIBEI
        // Linux libei (Wayland)
    #endif
#endif
```

Platform implementations are in `src/lib/platform/`:
- `MSWindows*.cpp/h` - Windows
- `OSX*.cpp/h/mm` - macOS
- `XWindows*.cpp/h` - X11
- `Ei*.cpp/h` - libei

## Testing

**Running Tests:**
```bash
# Build with tests
cmake .. -DINPUTLEAP_BUILD_TESTS=ON

# Run all tests
ctest --verbose

# Run specific test
./bin/unittests --gtest_filter="StringTests.*"
```

**Writing Tests:**
- Location: `src/test/unittests/`
- Framework: Google Test
- Test naming: `<Component>Tests` (e.g., `StringTests`)
- Use mock objects from `src/test/mock/`

**Example test:**
```cpp
TEST(StringTests, format_formatWithArguments_formatedString)
{
    const char* format = "%%%{1}=%{2}";
    std::string result = string::format(format, "answer", "42");
    EXPECT_EQ("%answer=42", result);
}
```

## Logging

Use the logging macros from `base/Log.h`:

```cpp
#include "base/Log.h"

LOG_INFO("Connecting to server: %s", address);
LOG_DEBUG("Received packet: %d", packetId);
LOG_ERR("Failed to connect: %s", errorMsg);
```

Log levels (in order of severity): `kFATAL`, `kERROR`, `kWARNING`, `kNOTE`, `kINFO`, `kDEBUG` through `kDEBUG5`.

## Release Notes

The project uses [towncrier](https://towncrier.readthedocs.io/) for changelog management.

**Adding release notes:**
Create a file in `doc/newsfragments/` with format: `<issue_number>.<type>.md`

Types:
- `.feature` - New features
- `.bugfix` - Bug fixes
- `.security` - Security fixes
- `.doc` - Documentation improvements
- `.removal` - Deprecations and removals

**Building release notes:**
```bash
towncrier build --version X.Y.Z --date YYYY-MM-DD
```

## Security Considerations

- TLS/SSL encryption is used for network communication (OpenSSL)
- Certificate fingerprints are verified
- Input injection is sandboxed on supported platforms
- Be cautious with clipboard content handling (can contain executable content)

## Common Tasks

**Adding a new file:**
1. Add to appropriate `CMakeLists.txt`
2. Follow naming conventions
3. Add license header
4. Update tests if needed

**Adding platform-specific code:**
1. Add interface to `src/lib/platform/`
2. Implement for each platform (MSWindows, OSX, XWindows, Ei)
3. Use conditional compilation with `SYSAPI_*` and `WINAPI_*` macros

**Updating version:**
Edit these files:
- `cmake/Version.cmake`
- `doc/input-leapc.1`
- `doc/input-leaps.1`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `dist/debian/changelog`

## CI/CD

GitHub Actions workflows in `.github/workflows/builds.yml`:
- Builds for Linux (Ubuntu, Debian, Fedora, openSUSE), macOS, Windows, FreeBSD
- Uses both Qt5 and Qt6
- Produces installers for each platform
- Flatpak builds for Linux

## License Headers

All source files should include the GPLv2 license header:

```cpp
/*
 * InputLeap -- mouse and keyboard sharing utility
 * Copyright (C) 2012-2016 Symless Ltd.
 * Copyright (C) 2009 Nick Bolton
 *
 * This package is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * found in the file LICENSE that should have accompanied this file.
 *
 * This package is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
```

## Communication

- IRC: `#inputleap` (support) and `#inputleap-dev` (development) on LiberaChat
- Issues: GitHub issue tracker (preferred for bug reports)
- Pull requests should include release notes for user-visible changes
