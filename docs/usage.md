# CLI usage

MBT provides a minimalist CLI to compile your projects.

## `mbt build`

Builds project from `mbt-project.toml` in current directory.

> [See how to define an `mbt-project.toml`.](./mbtproject.md)

Uses `java 1.1` as target and `java 1.3` as source.

Outputs a handful of class files in defined build output directory.
Also does preverifying.

!!! attention
    Needs to have a set environment variable in order to work.
    [Learn more 1](./mbtproject.md#build_cmd), [Learn more 2](./mbtproject.md#preverify_cmd)

## `mbt jar <jarfile>`

Packages previously built classes, bundled libraries, resources and MANIFEST
into a JAR and stores it under defined `<jarfile>` path.

!!! attention
    Needs to have a set environment variable in order to work.
    [Learn more](./mbtproject.md#package_cmd)
