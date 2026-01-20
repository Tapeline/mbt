import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import click

from microbuildtool.click_utils import err_echo, ok_echo


def compile_classes(
    sources: list[Path],
    libs: list[Path],
    build_dir: Path,
    java_home: Path | None
):
    click.echo("Compiling classes")
    build_dir.mkdir(parents=True, exist_ok=True)

    if not sources:
        err_echo("No source files found.")
        return False

    classpath_str = os.pathsep.join(
        str(p.absolute()) for p in libs
    )

    (build_dir / "sources").write_text("\n".join(
        str(src.absolute()) for src in sources
    ))

    if java_home:
        javac_exe = str((java_home / "bin" / "javac").absolute())
    else:
        javac_exe = "javac"

    cmd = [
        javac_exe,
        "-source", "1.3",
        "-target", "1.1",
        "-d", str(build_dir.absolute()),
        "-cp", classpath_str,
        "@" + str((build_dir / "sources").absolute())
    ]

    click.echo(f"Compiling {len(sources)} source files")
    click.echo(f"Full command: {'\n'.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        ok_echo("Compilation successful.")
        return True
    except subprocess.CalledProcessError as e:
        err_echo(f"Compilation failed with exit code {e.returncode}")
        return False


def package_jar(
    resources_map: dict[Path, Path],
    bundled_libs: list[Path],
    build_dir: Path,
    output_jar: Path,
    manifest_file: Path,
    java_home: Path
):
    for lib_jar in bundled_libs:
        click.echo(f"Merging library: {os.path.basename(lib_jar)}")
        try:
            with zipfile.ZipFile(lib_jar, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if member.startswith("META-INF"):
                        continue
                    zip_ref.extract(member, build_dir)
        except Exception as e:
            err_echo(f"Error extracting {lib_jar}: {e}")
            return False

    for res_src, res_dst in resources_map.items():
        if res_src.is_file():
            shutil.copy(res_src, build_dir / res_dst)

    if java_home:
        jar_exe = str((java_home / "bin" / "jar").absolute())
    else:
        jar_exe = "jar"

    output_jar.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        jar_exe,
        "cvfm",
        str(output_jar.absolute()),
        str(manifest_file.absolute()),
        "-C", str(build_dir.absolute()),
        "."
    ]
    click.echo("Crafting JAR")
    click.echo(f"Bundling {len(bundled_libs)} libs, {len(resources_map)} resources")
    click.echo(f"Full command: {'\n'.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        ok_echo(f"JAR created successfully: {output_jar}")
        return True
    except subprocess.CalledProcessError as e:
        err_echo(f"Packaging failed with exit code {e.returncode}")
        return False
