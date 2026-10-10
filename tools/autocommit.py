"""Guarda y sube automáticamente los cambios del kit de marca.

Lo ejecuta el hook "Stop" de Claude Code al final de cada respuesta.
También se puede correr a mano:  python -I tools/autocommit.py

- Si no hay cambios, no hace nada.
- Arma el mensaje del commit a partir de las carpetas que cambiaron.
- No sube archivos de más de 90 MB (GitHub rechaza los de más de 100 MB).
- Imprime un JSON con "systemMessage" para que Claude Code muestre el resultado.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_MB = 90

AREAS = {
    "editor": "editor",
    "plantillas": "plantillas",
    "aplicaciones": "aplicaciones",
    "video": "video",
    "brand": "datos de marca",
    "tools": "herramientas",
    "logo": "logo",
    "assets": "recursos",
}


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def say(msg):
    print(json.dumps({"systemMessage": msg}, ensure_ascii=False))


def main():
    gitdir = ROOT / ".git"
    if any((gitdir / f).exists() for f in ("MERGE_HEAD", "REBASE_HEAD", "rebase-merge", "rebase-apply")):
        say("Autocommit: hay un merge o rebase a medias; no hice nada.")
        return

    status = git("status", "--porcelain", "-uall")
    if not status.strip():
        return

    # Archivos demasiado grandes: se dejan fuera.
    grandes = []
    for line in status.splitlines():
        path = line[3:].split(" -> ")[-1].strip('"')
        p = ROOT / path
        if p.is_file() and p.stat().st_size > MAX_MB * 1024 * 1024:
            grandes.append(path)

    git("add", "-A")
    for g in grandes:
        git("reset", "-q", "--", g)

    files = [f for f in git("diff", "--cached", "--name-only").splitlines() if f]
    if not files:
        if grandes:
            say(f"Autocommit: no subí {', '.join(grandes)} (más de {MAX_MB} MB).")
        return

    areas = []
    for f in files:
        top = f.split("/")[0]
        name = AREAS.get(top, "documentación" if f.endswith(".md") else "otros")
        if name not in areas:
            areas.append(name)

    title = "Actualiza " + ", ".join(areas[:4]) + (" y más" if len(areas) > 4 else "")
    shown = files[:30]
    body = "\n".join(f"- {f}" for f in shown)
    if len(files) > len(shown):
        body += f"\n- … y {len(files) - len(shown)} archivos más"
    msg = f"{title}\n\nCommit automático ({len(files)} archivos):\n{body}\n"
    subprocess.run(["git", "commit", "-q", "-F", "-"], cwd=ROOT, input=msg, text=True,
                   encoding="utf-8", check=True, capture_output=True)

    short = git("rev-parse", "--short", "HEAD").strip()
    push = subprocess.run(["git", "push", "-q"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    extra = f" No subí {', '.join(grandes)} (más de {MAX_MB} MB)." if grandes else ""
    if push.returncode != 0:
        say(f"Autocommit {short}: «{title}» guardado, pero el push falló: {push.stderr.strip()[:200]}{extra}")
    else:
        say(f"Autocommit {short}: «{title}» ({len(files)} archivos) subido a GitHub.{extra}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # nunca bloquear a Claude Code
        say(f"Autocommit falló: {e}")
    sys.exit(0)
