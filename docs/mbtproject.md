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
