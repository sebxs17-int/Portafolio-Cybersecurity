"""Modulo Port Scanner para Orion"""

import socket
from datetime import datetime
from ...base import Basemodule

class PortScanner(Basemodule):
    def __init__(self):
        super().__init__(
            name="port_scanner",
            description="Escaner basico de puertos TCP"
        )
        # Puertos comunes para escanear
        self.common_ports = [21, 22, 23, 80, 443, 445, 3389, 8080, 8443]

    def execute(self, target, ports=None, timeout=2, use_nmap=False, **kwargs):
        """
        Ejecuta el escaneo.
        - target: IP/host
        - ports: lista de puertos (si None usa self.common_ports)
        - timeout: timeout por socket
        - use_nmap: flag opcional que por ahora se ignora (placeholder para integración nmap)
        - **kwargs: acepta argumentos extra que el framework pueda pasar
        """
        print(f"[PortScanner] Iniciando escaneo en: {target} (use_nmap={use_nmap})")

        # Si quieres, cuando use_nmap == True aqui llamas a python-nmap (más adelante).
        # Por ahora seguimos con la implementación por sockets.

        if ports is None:
            ports = self.common_ports

        print(f"Escaneando {len(ports)} puertos en {target}...")

        open_ports = []
        total = len(ports)

        for port in ports:
            try:
                if self._check_port(target, port, timeout):
                    open_ports.append(port)
                    print(f"Puerto {port} en {target} -> ABIERTO")
                else:
                    print(f"Puerto {port} en {target} -> CERRADO")
            except Exception as e:
                print(f"[PortScanner] Error al comprobar {target}:{port} -> {e}")

        results = {
            "module": self.name,
            "target": target,
            "open_ports": open_ports,
            "open_count": len(open_ports),
            "total_scanned": total,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backend": "socket"
        }

        print(f"[PortScanner] escaneo completado")
        print(f"Puertos abiertos: {open_ports}")

        return results

    def _check_port(self, target, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except socket.gaierror:
            print(f"Error: No se puede resolver el host {target}")
            return False
        except socket.error as e:
            print(f"Error de socket: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False