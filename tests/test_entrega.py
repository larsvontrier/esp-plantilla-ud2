"""
Comprobaciones automaticas de la practica integradora de la UD2.

Se ejecutan en GitHub Actions tras cada push. Revisan la forma del trabajo
(script que se ejecuta, estructura, DEPURACION.md con sus tablas, historial),
no la calidad del analisis: una comprobacion superada no garantiza la
calificacion, que pone el profesorado.

Para ejecutarlas en el equipo:
    python -m pip install pytest
    python -m pytest -v tests
"""

import ast
import hashlib
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAL = RAIZ / "brechas_con_errores.py"
SCRIPT = RAIZ / "brechas_interseccionales.py"
DEPURACION = RAIZ / "DEPURACION.md"
COMMITS_PROPIOS = 3  # sin contar el commit inicial que crea la plantilla

# huella del original con finales de linea LF, para detectar cambios
HUELLA_ORIGINAL = "3344f6c803b606972faead64015a2c432035ce1e54046ef4501067e4e879da9d"

# valores que debe mostrar el script, con un decimal
INDICADORES = {
    "brecha de género": "16.1",
    "brecha por discapacidad": "16.7",
    "brecha de género entre personas con discapacidad": "6.1",
    "brecha acumulada": "19.6",
}

APARTADOS = {
    1: "Entorno",
    2: "Registro de errores",
    3: "Comprobación",
    4: "Valoración",
}

ESTRUCTURAS_PROHIBIDAS = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match,
                          ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def git(*args):
    proceso = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True)
    return proceso.stdout.strip()


def leer_script():
    assert SCRIPT.is_file(), "Falta el archivo brechas_interseccionales.py."
    return SCRIPT.read_text(encoding="utf-8")


def arbol():
    try:
        return ast.parse(leer_script())
    except SyntaxError as error:
        pytest.fail(f"brechas_interseccionales.py tiene un error de sintaxis en la línea {error.lineno}: {error.msg}")


def leer_depuracion():
    assert DEPURACION.is_file(), "Falta el archivo DEPURACION.md."
    texto = DEPURACION.read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)


def apartados():
    partes = re.split(r"^##\s+(\d+)\.", leer_depuracion(), flags=re.MULTILINE)
    return {int(partes[i]): partes[i + 1] for i in range(1, len(partes) - 1, 2)}


def filas_de_tabla(texto):
    filas = [l.strip() for l in texto.splitlines() if l.strip().startswith("|")]
    separadores = sum(1 for f in filas if re.fullmatch(r"\|[\s:|-]+\|?", f))
    return max(len(filas) - 2 * separadores, 0)


def palabras(texto):
    return len(re.findall(r"\w+", texto))


# Script original

def test_original_sin_modificar():
    assert ORIGINAL.is_file(), "Falta brechas_con_errores.py: no debe borrarse ni renombrarse."
    contenido = ORIGINAL.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(contenido).hexdigest() == HUELLA_ORIGINAL, (
        "brechas_con_errores.py ha cambiado. Debe quedar como estaba: las correcciones "
        "se hacen en brechas_interseccionales.py."
    )


# Script corregido

def test_script_se_ejecuta():
    leer_script()
    proceso = subprocess.run([sys.executable, SCRIPT.name], cwd=RAIZ, capture_output=True,
                             text=True, encoding="utf-8", timeout=30)
    assert proceso.returncode == 0, (
        "brechas_interseccionales.py termina con error:\n" + proceso.stderr[-800:]
    )


@pytest.mark.parametrize("indicador", list(INDICADORES))
def test_indicador_correcto(indicador):
    proceso = subprocess.run([sys.executable, SCRIPT.name], cwd=RAIZ, capture_output=True,
                             text=True, encoding="utf-8", timeout=30)
    numeros = set(re.findall(r"-?\d+(?:\.\d+)?", proceso.stdout))
    esperado = INDICADORES[indicador]
    assert esperado in numeros, (
        f"La salida no muestra el valor esperado para la {indicador} ({esperado}, con un decimal)."
    )


def test_docstring():
    doc = ast.get_docstring(arbol())
    assert doc, "El script debe empezar con una cadena de documentación (docstring) entre comillas triples."
    assert palabras(doc) >= 15, "El docstring es demasiado breve: debe explicar el propósito y las fuentes."
    assert "INE" in doc, "El docstring debe citar la fuente de los datos (INE)."


def test_constantes_en_mayusculas():
    nombres = [t.id for nodo in ast.walk(arbol()) if isinstance(nodo, ast.Assign)
               for t in nodo.targets if isinstance(t, ast.Name)]
    constantes = [n for n in nombres if n.isupper()]
    assert len(constantes) >= 4, "Los datos deben definirse como constantes con nombres en mayúsculas."


def test_comentarios():
    fichas = tokenize.generate_tokens(io.StringIO(leer_script()).readline)
    comentarios = [f for f in fichas if f.type == tokenize.COMMENT and not f.string.startswith("#!")]
    assert len(comentarios) >= 4, "Faltan comentarios: bloques, unidades y grupo de referencia."


def test_asserts():
    asserts = [n for n in ast.walk(arbol()) if isinstance(n, ast.Assert)]
    assert len(asserts) >= 2, "Se esperan al menos dos assert que comprueben los valores publicados por el INE."


def test_sin_estructuras_de_control():
    encontradas = sorted({type(n).__name__ for n in ast.walk(arbol()) if isinstance(n, ESTRUCTURAS_PROHIBIDAS)})
    assert not encontradas, (
        "El script solo debe usar asignaciones, expresiones y print(); se han encontrado: " + ", ".join(encontradas)
    )


# DEPURACION.md

def test_estan_los_cuatro_apartados():
    encontrados = apartados()
    faltan = [f"{n}. {t}" for n, t in APARTADOS.items() if n not in encontrados]
    assert not faltan, "Faltan apartados numerados en DEPURACION.md: " + "; ".join(faltan)


@pytest.mark.parametrize("numero", list(APARTADOS))
def test_apartado_completado(numero):
    texto = apartados().get(numero, "")
    nombre = f"{numero}. {APARTADOS[numero]}"
    assert "_Pendiente._" not in texto, f"El apartado «{nombre}» sigue marcado como pendiente."
    assert palabras(texto) >= 20, f"El apartado «{nombre}» está vacío o es demasiado breve."


def test_entorno_indica_version():
    texto = apartados().get(1, "")
    assert re.search(r"\b3\.\d{1,2}(\.\d+)?\b", texto), "El apartado 1 debe indicar la versión de Python (por ejemplo, 3.14.9)."


def test_registro_de_errores():
    filas = filas_de_tabla(apartados().get(2, ""))
    assert filas >= 5, f"El registro de errores del apartado 2 debe tener una fila por error (al menos cinco); hay {filas}."


def test_tabla_de_comprobacion():
    filas = filas_de_tabla(apartados().get(3, ""))
    assert filas >= 4, f"La tabla del apartado 3 debe tener una fila por indicador (cuatro); hay {filas}."


def test_valoracion_extension():
    n = palabras(apartados().get(4, ""))
    assert 80 <= n <= 230, f"La valoración debe tener entre 80 y 200 palabras, aproximadamente; tiene {n}."


# Historial

# marcas de un entorno virtual: pyvenv.cfg lo crea venv en la raiz del entorno;
# site-packages, conda-meta y los scripts de activacion aparecen en cualquier entorno
MARCAS_ENTORNO = ("pyvenv.cfg",)
CARPETAS_ENTORNO = (".venv", "site-packages", "conda-meta")
SCRIPTS_ACTIVACION = ("Scripts/activate", "bin/activate")


def archivos_versionados():
    proceso = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, text=True)
    return [ruta for ruta in proceso.stdout.split("\0") if ruta]


def rutas_de_entorno_virtual(rutas):
    """Devuelve las rutas versionadas que pertenecen a un entorno virtual."""
    sospechosas = []
    for ruta in rutas:
        partes = ruta.split("/")
        if (partes[-1] in MARCAS_ENTORNO
                or any(carpeta in partes[:-1] for carpeta in CARPETAS_ENTORNO)
                or any(ruta == s or ruta.endswith("/" + s) for s in SCRIPTS_ACTIVACION)):
            sospechosas.append(ruta)
    return sospechosas


def test_entorno_virtual_no_versionado():
    sospechosas = rutas_de_entorno_virtual(archivos_versionados())
    if "pyvenv.cfg" in sospechosas:
        consejo = (
            "El entorno se creó en la raíz del repositorio (python -m venv .) y el .gitignore no lo excluye. "
            "Se retira con: git rm -r --cached --ignore-unmatch Lib Scripts Include etc share bin lib lib64 pyvenv.cfg "
            "y se crea de nuevo con python -m venv .venv."
        )
    else:
        consejo = (
            "Se retira del repositorio sin borrarlo del disco con git rm -r --cached <carpeta del entorno>, "
            "y esa carpeta se añade al .gitignore (el entorno del curso es .venv)."
        )
    assert not sospechosas, (
        f"Hay {len(sospechosas)} archivos de un entorno virtual en el repositorio "
        f"(por ejemplo: {', '.join(sospechosas[:3])}). {consejo}"
    )


def test_historial():
    total = int(git("rev-list", "--count", "HEAD") or 0)
    propios = total - 1
    assert propios >= COMMITS_PROPIOS, (
        f"Se esperan al menos {COMMITS_PROPIOS} commits propios, repartidos a lo largo del trabajo; hay {propios}."
    )
