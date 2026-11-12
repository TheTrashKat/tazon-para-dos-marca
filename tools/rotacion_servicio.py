"""Servicio de rotación: se queda corriendo y, cuando toca, genera la siguiente pieza.

Lo arranca y lo detiene el panel de servicios de D: (D:\\panel). No publica nada: en modo
'aprobar' la pieza queda pendiente; en 'automatico' queda marcada para el publicador.
Revisa cada hora la fecha de la próxima pieza según tools/rotacion_config.json.
"""
import datetime as dt, json, os, pathlib, sys, time, traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import rotacion  # noqa: E402

PID = ROOT / "salida" / "rotacion" / "servicio.pid"
LOG = ROOT / "salida" / "rotacion" / "servicio.log"
REVISAR_CADA_S = 3600


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M} {msg}\n")


def toca(estado):
    return dt.date.today() >= rotacion.proxima_fecha(estado)


def main():
    PID.parent.mkdir(parents=True, exist_ok=True)
    PID.write_text(str(os.getpid()), encoding="utf-8")
    log(f"arranca · modo {rotacion.CFG['modo']} · cada {rotacion.CFG['cada_dias']} días")
    try:
        while True:
            try:
                # Relee la configuración en cada vuelta: puedes cambiar frecuencia o modo sin reiniciar.
                rotacion.CFG.update(json.loads((ROOT / "tools" / "rotacion_config.json").read_text(encoding="utf-8")))
                estado = rotacion.cargar_estado()
                if toca(estado):
                    rotacion.main_generar()
                    log("pieza generada")
            except Exception:
                log("error:\n" + traceback.format_exc())
            time.sleep(REVISAR_CADA_S)
    finally:
        PID.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
