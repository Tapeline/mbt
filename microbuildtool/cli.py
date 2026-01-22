import os
import sys
from pathlib import Path

import click

from microbuildtool.build import (
    compile_classes, package_jar,
    DEFAULT_BUILD_CMD, preverify, DEFAULT_PREVERIFY_CMD, BuildError,
    DEFAULT_JAR_CMD,
)
from microbuildtool.click_utils import err_echo
from microbuildtool.collect import (
    collect_all_libs,
    collect_bundled_libs,
    collect_res,
    collect_sources, collect_bootclasspath,
)
from microbuildtool.config import load_config


@click.command()
def mbt():
    click.echo("MicroBuildTool v0.3.0")


@click.group()
def mbt_group():
    """MBT CLI."""


@mbt_group.command("build")
def build_command():
    cfg = load_config(Path("mbt-project.toml"))
    click.echo("Collecting sources")
    sources = collect_sources(Path(""), cfg.assets.src)
    click.echo(f"Collected {len(sources)} sources")
    click.echo("Collecting libraries")
    all_libs = collect_all_libs(cfg.libs, Path(""))
    bundled_libs = collect_bundled_libs(cfg.libs, Path(""))
    click.echo(
        f"Collected {len(all_libs)} libraries, "
        f"out of them {len(bundled_libs)} bundled"
    )
    boot_cp = collect_bootclasspath(cfg.build.bootclasspath, Path(""))
    click.echo(f"Using {boot_cp} as boot classpath")
    try:
        compile_classes(
            cfg.build.build_cmd or DEFAULT_BUILD_CMD,
            {key: val for key, val in os.environ.items()},
            sources,
            all_libs,
            bundled_libs,
            boot_cp,
            Path(cfg.build.output_dir),
        )
        preverify(
            cfg.build.preverify_cmd or DEFAULT_PREVERIFY_CMD,
            {key: val for key, val in os.environ.items()},
            Path(cfg.build.output_dir),
            boot_cp,
        )
    except BuildError as e:
        err_echo(f"Failed: {e}")


@mbt_group.command("jar")
@click.argument(
    "output_jar",
    type=click.Path(),
)
def jar_command(output_jar):
    cfg = load_config(Path("mbt-project.toml"))
    resources = collect_res(Path(""), cfg.assets.res)
    package_jar(
        cfg.build.package_cmd or DEFAULT_JAR_CMD,
        {key: val for key, val in os.environ.items()},
        resources,
        Path(cfg.build.output_dir),
        Path(output_jar),
        Path(cfg.assets.manifest),
    )


def main():
    if len(sys.argv) > 1:
        mbt_group()
    else:
        mbt()


if __name__ == '__main__':
    main()
