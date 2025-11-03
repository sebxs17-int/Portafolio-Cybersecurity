from typing import Any, Dict
from pathlib import Path
import json
import logging
import sys

class Orion:
    def __init__(self, show_banner: bool = True, log_level: int = logging.INFO):
        self.modules: Dict[str, Any] = {}
        self.logger = logging.getLogger("Orion")
        if not self.logger.handlers:
            h = logging.StreamHandler(sys.stdout)
            fmt = logging.Formatter("[Orion] %(levelname)s - %(message)s")
            h.setFormatter(fmt)
            self.logger.addHandler(h)
        self.logger.setLevel(log_level)
        if show_banner:
            try:
                self.show_banner()
            except Exception as e:
                self.logger.debug(f"No se pudo mostrar banner: {e}")

    def _get_repo_root(self) -> Path:
        return Path(__file__).resolve().parents[1]

    def show_banner(self, banner_filename: str = "assets/banner.txt"):
        root = self._get_repo_root()
        banner_path = root.joinpath(banner_filename)
        if banner_path.exists():
            banner_text = banner_path.read_text(encoding="utf-8")
            print(banner_text)
            print("Orión — Mini framework modular de security\n")
        else:
            self.logger.debug(f"Banner no encontrado en: {banner_path}")

    def pretty_print_result(self, result: Dict[str, Any]):
        print("\n===== RESULTADO =====")
        try:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception:
            print(result)
        print("=====================\n")

    def load_module(self, name: str, module_cls_or_instance):
        """
        Acepta una clase o una instancia:
        - si recibe una clase, intenta instanciarla y guarda la instancia.
        - si no puede instanciar, guarda la referencia.
        """
        if isinstance(module_cls_or_instance, type):
            try:
                instance = module_cls_or_instance()
                self.modules[name] = instance
                self.logger.debug(f"Instanciado y cargado: {name}")
                return instance
            except Exception as e:
                self.modules[name] = module_cls_or_instance
                self.logger.warning(f"No se pudo instanciar {module_cls_or_instance}: {e}. Guardado referencia.")
                return module_cls_or_instance
        else:
            self.modules[name] = module_cls_or_instance
            self.logger.debug(f"Cargado módulo: {name}")
            return module_cls_or_instance

    def execute(self, module_name: str, *args, **kwargs):
        """
        Ejecuta el módulo:
        - si el objeto cargado es callable lo llama directo
        - si tiene método .execute() lo llama
        - si es clase, intenta instanciarla y llamar a execute()
        """
        module = self.modules.get(module_name)
        if module is None:
            raise ValueError(f"Module '{module_name}' not loaded")
        if callable(module):
            self.logger.debug(f"Ejecutando callable directo: {module_name}")
            return module(*args, **kwargs)
        exec_fn = getattr(module, "execute", None)
        if callable(exec_fn):
            self.logger.debug(f"Ejecutando .execute() de instancia: {module_name}")
            return exec_fn(*args, **kwargs)
        if isinstance(module, type):
            try:
                inst = module()
                exec_fn = getattr(inst, "execute", None)
                if callable(exec_fn):
                    self.logger.debug(f"Instanciada clase y ejecutado execute(): {module_name}")
                    return exec_fn(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error instanciando clase de módulo {module_name}: {e}")
                raise
        raise TypeError(f"Module '{module_name}' is not executable")