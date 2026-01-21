import os
import sys
from pathlib import Path

import click

from microbuildtool.build import compile_classes, package_jar
from microbuildtool.collect import (
    collect_all_libs,
    collect_bundled_libs,
    collect_res,
    collect_sources,
)
from microbuildtool.config import load_config


@click.command()
def mbt():
    click.echo("MicroBuildTool v0.0.0")


@click.group()
def mbt_group():
    """MBT CLI."""


def _get_mbt_java():
    return Path(os.environ["MBT_JAVA"]) \
        if os.environ.get("MBT_JAVA", None) \
        else None


@mbt_group.command("build")
def build_command():
    cfg = load_config(Path("mbt-project.toml"))
    click.echo("Collecting sources")
    sources = collect_sources(Path(""), cfg.assets.src)
    click.echo(f"Collected {len(sources)} sources")
    click.echo("Collecting libraries")
    all_libs = collect_all_libs(cfg.libs, Path(""))
    click.echo(f"Collected {len(all_libs)} libraries")
    compile_classes(
        sources,
        all_libs,
        Path(cfg.build.output_dir),
        _get_mbt_java(),
    )


@mbt_group.command("jar")
@click.argument(
    "output_jar",
    type=click.Path(),
)
def jar_command(output_jar):
    cfg = load_config(Path("mbt-project.toml"))
    resources = collect_res(Path(""), cfg.assets.res)
    bundled_libs = collect_bundled_libs(cfg.libs, Path(""))
    package_jar(
        resources,
        bundled_libs,
        Path(cfg.build.output_dir),
        Path(output_jar),
        Path(cfg.assets.manifest),
        _get_mbt_java()
    )


def main():
    if len(sys.argv) > 1:
        mbt_group()
    else:
        mbt()


if __name__ == '__main__':
    main()
