
import sys
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orion import Orion

from orion.modules.reconnaissance.port_scanner import PortScanner


def parse_args():
    p = argparse.ArgumentParser(description="Run Orion miniframework on a target")
    p.add_argument("target", help="IP or hostname to scan")
    p.add_argument("--ports", nargs="+", type=int, default=[20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 465, 587, 993, 995, 1025, 1433, 1521, 1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 8888],
                   help="Ports to scan (default: 22 80 8080)")
    p.add_argument("--timeout", type=float, default=1.0, help="Timeout per port (s)")
    p.add_argument("--use-nmap", type=lambda s: s.lower() in ("true","1","y","yes"),
                   default=False, help="Use nmap backend if available (True/False)")
    p.add_argument("--out", default=None, help="Save JSON result to file (optional)")
    return p.parse_args()

def main():
    args = parse_args()
    target = args.target
    ports = args.ports
    timeout = args.timeout
    use_nmap = args.use_nmap

    # Crear framework y cargar módulos
    orion = Orion(show_banner=True, log_level=20)
    orion.load_module("port_scan", PortScanner)
   

    # Ejecutar port_scanner (ejemplo simple)
    print(f"[Orion] INFO - Ejecutando port_scan en {target}")
    res_port = orion.execute("port_scan", target, ports=ports, timeout=timeout, use_nmap=use_nmap)
    # pretty_print_result espera el resultado como argumento
    try:
        orion.pretty_print_result(res_port)
    except TypeError:
       
        print("==== RESULTADO RAW ====")
        print(json.dumps(res_port, indent=2, ensure_ascii=False))

    # combinar resultados si ejecutas más módulos:
    final = {
        "target": target,
        "modules": [res_port]
    }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(final, f, indent=2, ensure_ascii=False)
        print(f"[Orion] Resultado guardado en {args.out}")

if __name__ == "__main__":
    main()