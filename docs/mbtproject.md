---
toc-depth: 3
---
# Project file syntax

Project definition is located in `mbt-project.toml` file in project root.


## Top-level elements

### `name`
Name of MBT project.


## Assets definition

Here you define what to build from.

### `src`
List of glob patterns or filenames to supply to Java Compiler as sources.

### `res`
List of resource files in format of `glob:target_dir` or `source_path:target_path`.

When left part is a glob (i.e. has at least 1 `*` or `?`), all files matched by this glob
are placed to `target_dir` under building directory. 

Note that for each glob pattern, common path prefix of all matched files is stripped of. 
So if you have `res/a.txt` and `res/some/b.txt`, `res/*:.` resource declaration will match
both of them, strip off `res/` part, and place `a.txt` and `some/b.txt` 
to the root of the build directory.

### `manifest`
Path to manifest file.


## Build options

### `output_dir`
Build directory. All compiled classes will be transferred there. Also, all resources and
bundled libraries are copied there.

### `bootclasspath`
List of glob patterns that match JARs that represent the base library 
(usually `cldc.jar` and `midp.jar`)

### `build_cmd`
(optional) List of strings (command parts).

Command to use when building classes. Defaults to:
```toml
build_cmd = [
    "$MBT_JAVAC",
    "-source", "1.3",
    "-target", "1.1",
    "-d", "$RAW_BUILD_DIR",
    "-bootclasspath", "$BOOTCLASSPATH",
    "-cp", "$CLASSPATH",
    "@$SOURCES_FILE"
]
```

Availiable placeholders:

- `$RAW_BUILD_DIR` - building directory for unpreverified files
- `$BOOTCLASSPATH` - configured bootclasspath
- `$CLASSPATH` - assembled from libraries classpath
- `$SOURCES_FILE` - file with list of all source code files targeted

Other placeholders default to corresponding environment variables.

### `preverify_cmd`
(optional) List of strings (command parts).

Command to use when preverifying classes. Defaults to:
```toml
preverify_cmd = [
    "$MBT_PREVERIFIER",
    "-classpath", "$BOOTCLASSPATH",
    "-d", "$PREVERIFIED_BUILD_DIR",
    "$RAW_BUILD_DIR",
]
```

Availiable placeholders:

- `$RAW_BUILD_DIR` - building directory for unpreverified files
- `$PREVERIFIED_BUILD_DIR` - result building directory for preverified files
- `$BOOTCLASSPATH` - configured bootclasspath

Other placeholders default to corresponding environment variables.

### `package_cmd`
(optional) List of strings (command parts).

Command to use when crafting a JAR package. Defaults to:
```toml
package_cmd = [
    "$MBT_JAR",
    "cvfm",
    "$OUTPUT_JAR",
    "$MANIFEST",
    "-C", "$PREVERIFIED_BUILD_DIR",
    "."
]
```

Availiable placeholders:

- `$PREVERIFIED_BUILD_DIR` - result building directory for preverified files
- `$OUTPUT_JAR` - configured output path for resulting JAR file
- `$MANIFEST` - path of custom user supplied `MANIFEST.MF`

Other placeholders default to corresponding environment variables.

## Libraries definitions

### Library def
Library definition is a section under `libs.{library-name}` name.

It has two properties:

- `glob` — glob pattern for JAR library files
- `include` — boolean, whether to include these libraries to final JAR, 
   or just use them in compilation process for name resolution.


## Example
```toml
name = "Test J2ME"

[assets]
src = ["src/**/*.java"]
res = ["res/*:."]
manifest = "MANIFEST.MF"

[build]
output_dir = "build"

[libs]
[libs.nokia-platform-libs]
glob = "lib/**.jar"
include = false
```
