# UD2. Práctica: brechas salariales interseccionales

* Módulo 5098. Entornos y sintaxis en Python.
* _Pepe Calo_

Este repositorio procede de la plantilla de la tarea.
Los archivos **`ENUNCIADO.md` y `brechas_con_errores.py` y las carpetas `.github` y `tests` forman parte de la plantilla y no deben modificarse**.

El trabajo de la **tarea debe escribirse en `brechas_interseccionales.py` (que hay que crear) y en `DEPURACION.md`**.


## 1. Requisitos previos

1. Se debe comprobar que este **repositorio** es **privado** y que está en la cuenta personal, con el nombre`5098-ud2-<usuario>` (donde `<usuario>` es el nombre de la cuenta de GitHub).
2. **Invitar como colaborador a la cuenta del profesorado** que he indicado en los apuntes y en el aula virtual: **Settings**, **Collaborators**, **Add people**.
3. **Clonar el repositorio en el equipo local** para trabajar siempre dentro de la carpeta clonada.



## 2. Enunciado

El **script `brechas_con_errores.py` calcula cuatro indicadores de brecha salarial** con datos del INE de 2024, pero **contiene varios errores** de sintaxis, de ejecución y lógicos. La tarea consiste en **depurarlo, mejorar su estructura y documentar el proceso**.

| Indicador | Grupo de referencia | Grupo comparado |
|---|---|---|
| Brecha de género | Hombres | Mujeres |
| Brecha por discapacidad | Personas sin discapacidad | Personas con discapacidad |
| Brecha de género entre personas con discapacidad | Hombres con discapacidad | Mujeres con discapacidad |
| Brecha acumulada | Personas sin discapacidad | Mujeres con discapacidad |

En todos los casos, la brecha es la diferencia de salarios dividida entre el salario del grupo de referencia, en porcentaje. Valores publicados por el INE para comprobar: brecha de género del **16,1 %**; las personas con discapacidad cobran un **16,7 %** menos.

### 2.1. Tareas

1. Ejecutar `brechas_con_errores.py` y **corregir los errores de uno en uno**, en el orden en que aparecen, anotando cada uno en el apartado 2 de `DEPURACION.md`. Para no modificar el original, se trabaja sobre una copia llamada `brechas_interseccionales.py`.
2. Mejorar la estructura de `brechas_interseccionales.py`: docstring con el propósito y las fuentes, constantes con comentarios de unidades, bloques de entrada, proceso y salida, y mensajes claros con un decimal.
3. Añadir al final, como mínimo, **dos `assert`** que comprueben los indicadores con los valores del INE.
4. Completar los cuatro apartados de `DEPURACION.md`: entorno, registro de errores, comprobación y valoración.

Como en el resto de la unidad, el script usa solo **asignaciones, expresiones y `print()`**, sin estructuras de control (`if`, `for`, `while`) ni funciones propias.

### 2.2. Historial

- Al menos **tres commits propios**, repartidos a lo largo del trabajo y con mensajes descriptivos (por ejemplo, uno tras corregir los errores de sintaxis y de ejecución, otro tras los lógicos y otro con la documentación). Esta vez, **un único commit final no se considera válido**.

## 3. Comprobaciones automáticas

Tras cada `git push`, **GitHub Actions ejecuta las comprobaciones de la carpeta `tests`**. El resultado aparece junto a cada commit en la página del repositorio: marca verde si se superan todas y cruz roja si alguna falla. La pestaña **Actions** indica cuál y por qué.

Las comprobaciones revisan la **forma** **del trabajo** (que el script se ejecute y muestre los cuatro indicadores, que tenga docstring, constantes y `assert`, que `DEPURACION.md` tenga sus apartados y tablas), no es la validación del análisis: La idea es **orientar, pero no evaluar** la tarea. También pueden ejecutarse en el equipo:

```bash
python -m pip install pytest
python -m pytest -v tests
```

## 4. Evaluación

La práctica se evaluará con una de estas tres notas, igual que el resto de tareas opcionales del módulo:

| Nota | Criterio |
|:--:|---|
| **10** | Completa y correcta en lo esencial, aunque tenga detalles mejorables |
| **5** | Entregada y corregible, pero incompleta o con errores de fondo en algún apartado |
| **0** | No entregada, entregada fuera de plazo, imposible de corregir (repositorio inaccesible o hash que no figura en GitHub) o con copia |

Para decidir la nota se revisarán, principalmente, estos puntos::

| Aspecto que se revisa | CE |
|---|:--:|
| Entorno: versión, implementación y modelo de ejecución | b, d |
| Estructura del script: docstring, constantes, bloques, comentarios y nombres | a, c |
| Identificación y clasificación de los errores | e |
| Registro de errores antes y después, y versión corregida con resultados correctos | g |
| Comprobación con valores de referencia y `assert` | e, g |
| Valoración de la depuración | f |
| Presentación, Markdown y uso de Git | |

Reitero, las comprobaciones automáticas ayudan con la parte formal, pero no deciden la nota. Cómo se suman las tareas a la nota final está explicdoa en la página de evaluación del aula virtual.

## 5. Entrega

1. Enviar **todo el trabajo con `git push` y comprobar con `git status` que la rama está al día con `origin/main`**.
2. Abrir la **página del repositorio en GitHub y copiar el hash abreviado del último commit (siete caracteres)**. Si aparece en GitHub, está enviado.
3. **Entregar en la tarea del aula virtual**, antes de la fecha de cierre, un texto con estas dos líneas:

```text
Repositorio: https://github.com/usuario/5098-ud2-usuario
Commit: a1b2c3d
```

La versión corregida es la del commit indicado en la entrega dela tarea, aunque después se añadan otros. Si el plazo sigue abierto, la entrega se puede actualizar con un hash nuevo.
