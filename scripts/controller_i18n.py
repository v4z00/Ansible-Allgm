"""Shared controller language selection and message catalogs (Python standard library)."""
from functools import lru_cache
import json
import os
from pathlib import Path
import re
import stat
from string import Formatter
import sys
import zipfile
import zipimport

ROOT = Path(__file__).resolve().parent.parent
CATALOGS = (zipfile.Path(__loader__.archive, "lib/i18n/") if isinstance(__loader__, zipimport.zipimporter)
            else ROOT / "lib/i18n")
LANGUAGES = ("de", "en")
_active = "de"


def unique(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Duplicate translation key")
    return result


def read_catalog(path):
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    if not isinstance(data, dict) or not all(isinstance(value, str) and value.strip() for value in data.values()):
        raise ValueError(f"Invalid language catalog: {path.name}")
    return data


@lru_cache(maxsize=2)
def catalog(lang):
    combined = {}
    folder = CATALOGS / lang
    fragments = sorted((path for path in folder.iterdir() if path.name.endswith(".json")),
                       key=lambda path: path.name) if folder.is_dir() else []
    for path in [CATALOGS / (lang + ".json"), *fragments]:
        entries = read_catalog(path)
        if combined.keys() & entries.keys():
            raise ValueError(f"Duplicate translation keys in {path.name}")
        combined.update(entries)
    return combined


def settings_language(root):
    """Read only one top-level literal preference. Never follow settings symlinks or evaluate YAML."""
    if root is None:
        return None
    folder_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    try:
        directory = os.open(root, folder_flags)
        try:
            for part in ("group_vars", "all"):
                child = os.open(part, folder_flags, dir_fd=directory)
                os.close(directory)
                directory = child
            fd = os.open("settings.yml", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
            with os.fdopen(fd, "rb") as stream:
                info = os.fstat(fd)
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > 1024 * 1024:
                    return None
                data = stream.read(1024 * 1024 + 1)
                if len(data) > 1024 * 1024:
                    return None
        finally:
            os.close(directory)
    except OSError:
        return None
    rows = [line for line in data.splitlines() if re.match(rb"controller_lang[ \t]*:", line)]
    if len(rows) != 1:
        return None
    match = re.fullmatch(rb"""controller_lang[ \t]*:[ \t]+(['"]?)(de|en)\1(?:[ \t]+#.*|[ \t]*)""", rows[0])
    return match[2].decode("ascii") if match else None


def configure(root=None, lang=None):
    global _active
    choice = lang or os.environ.get("CONTROLLER_LANG") or settings_language(root) or "de"
    if choice not in LANGUAGES:
        invalid_language()
    _active = choice
    return choice


def language():
    return _active


def invalid_language():
    print("--lang / CONTROLLER_LANG: de | en", file=sys.stderr)
    raise SystemExit(2)


def cli_args(argv=None, root=None):
    args = list(sys.argv[1:] if argv is None else argv)
    clean = []
    explicit = None
    index = 0
    while index < len(args):
        arg = args[index]
        index += 1
        if arg == "--":
            clean.extend([arg, *args[index:]])
            break
        if arg == "--lang" or arg.startswith("--lang="):
            if explicit is not None or (arg == "--lang" and index == len(args)):
                invalid_language()
            explicit = args[index] if arg == "--lang" else arg.partition("=")[2]
            index += int(arg == "--lang")
            if explicit not in LANGUAGES:
                invalid_language()
            continue
        if arg in ("--root", "--controller", "--project", "--project-root") and index < len(args):
            root = args[index]
        elif arg.startswith(("--root=", "--controller=", "--project=", "--project-root=")):
            root = arg.partition("=")[2]
        clean.append(arg)
    os.environ["CONTROLLER_LANG"] = configure(root, explicit)
    return clean


def tr(key, /, **params):
    return catalog(language())[key].format(**params)


@lru_cache(maxsize=1)
def status_codes():
    return read_catalog(CATALOGS / "status_codes.json")


def status_code(value):
    if value.startswith("DEAKTIVIERT_"):
        return "disabled_" + status_code(value.removeprefix("DEAKTIVIERT_"))
    redirect = re.fullmatch(r"HTTP_([0-9]{3})_REDIRECT_NICHT_VERFOLGT", value)
    if redirect:
        return "http_" + redirect[1] + "_redirect_not_followed"
    return status_codes().get(value, value.lower())


def status_text(value):
    if value.startswith("DEAKTIVIERT_"):
        return tr("status.disabled", status=status_text(value.removeprefix("DEAKTIVIERT_")))
    if language() == "en" and value.startswith("HTTP_") and value.endswith("_REDIRECT_NICHT_VERFOLGT"):
        return status_code(value).upper()
    return catalog(language()).get("status." + value, value)


@lru_cache(maxsize=2)
def shared_errors(lang):
    # The bootstrap verifier and transport also run independently of this library.
    # Match only their explicit diagnostic templates at the controller CLI boundary.
    patterns = []
    for key, template in catalog(lang).items():
        if not key.startswith("errors."):
            continue
        pattern = ""
        for literal, field, _, _ in Formatter().parse(template):
            pattern += re.escape(literal)
            if field:
                pattern += "(?P<" + field + ">[^\\r\\n]+?)"
        patterns.append((re.compile(pattern), key))
    return patterns


def error_text(error):
    text = str(error)
    if text in status_codes():
        return status_text(text)
    source = "en" if language() == "de" else "de"
    for pattern, key in shared_errors(source):
        match = pattern.fullmatch(text)
        if match:
            return tr(key, **match.groupdict())
    return text


def machine_report(data):
    """Add stable English codes without replacing legacy values or mutating audit data."""
    if isinstance(data, list):
        return [machine_report(row) for row in data]
    if isinstance(data, dict):
        result = {key: machine_report(value) for key, value in data.items()}
        if isinstance(data.get("status"), str):
            result["status_code"] = status_code(data["status"])
        return result
    return data


def main(argv):
    args = cli_args(argv, ROOT)
    if not args or args[0] == "language":
        print(language())
        return
    params = dict(pair.split("=", 1) for pair in args[1:])
    print(tr(args[0], **params))


if __name__ == "__main__":
    main(sys.argv[1:])
