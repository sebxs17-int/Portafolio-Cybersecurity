## ORION FRAMEWORK (beta)

### Descripcion 

**Orion** es un mini framework modular para tareas de **reconocimiento** y **escaneo ofensivo** en entornos de seguridad. Esta version **Beta v1.0** introduce un nucleo base capaz de **cargar modulos dinamicos, ejecutar escaneos personalizados** y **extender facilmente** nuevas funciones para futuras fases ofensivas. (payloads,C2,Tecnologia,etc).

---

## Caracteristicas principales 
- Nucleo modular (Orion Core) para cargar y ejecutar modulos externos.
- Soporte para modulos de **escaneo de puertos** y **deteccion de servicios**.
- Compatible con Python 3.10+.
- Codigo limpio, documentado y facil de extender.
- Estructura adaptable para futuras versiones.

---

## Instalacion
```bash

1. git clone https://github.com/sebxs17-int/Portafolio-Cybersecurity.git
cd Portafolio-Cybersecurity/Orion-Framework

2.Instala dependencias del sistema:
sudo apt update
sudo apt install python3-venv python3-pip nmap -y

3.Crea y activa un entorno virtual:
python3 -m venv venv
source venv/bin/activate

4.Instala dependencias Python:
pip install -r requeriments.txt

5.Ejecuta:
Python3 run_scan.py (IP)

6.Cuando termines:
deactivate

```
---

## Dependecias
```bash
Python-namp
rich
requests
```
---

## Uso basico 
```bash 
py -3 run_scan.py (IP)
```
O desde Linux:
```bash
python3 run_scan.py (IP)
``` 
El programa ejecutara un escaneo basico de puertos comunes.

## Proximas versiones
- V.1.1 -> Escaneo de tecnologias
- V.2.0 -> Payload + C2 (evasive)
- V.3.0 -> Integracion de ML para evasion inteligente

---



## Nota del desarrollador 
Esta es una **version beta** del framework **ORION**. Puede presentar errores o comportamientos inesperados, ya que se encuentra en una fase de pruebas y mejora continua. Cada actualizacion busca optimizar la estabilidad, rendimiento y seguridad del framework. Si encuentras algun fallo o tienes sugerencias no dudes en abrir issue o dejar un comentario.

---

## Aviso Beta
**Orion Framework** esta actualmente en **fase beta,** lo que significa que aun esta en continuas mejoras y detalles para optimizacion.
Algunos componentes pueden cambiar o no funcionar al 100%. Este proyecto se encuentra en constante evolucuin y actualizacion.

---

## Agredecimiento y disculpa
Gracias por probar **Orion Framework**
Este proyecto aun esta en fase **Beta**, por lo que puede presentar eerores o limitaciones temporales. Pido disculpas por cualquier incoveniente y agradezco tu comprension mientras continuo mejorando  su rendimiento y estabilidad y capacidades.

Tu apoyo y paciencia ayudan a que **ORION** evolucione en cada version.

## Firma del proyecto
Desarrollado por **Sebastian Useche, CEO de Astheroid**
"Explorando los limites entre codigos y la seguridad"

© 2025 Astheroid. Todos los derechos reservados.
