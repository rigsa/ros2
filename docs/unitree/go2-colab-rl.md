---
title: "Entrenamiento RL en Google Colab"
description: "Cómo entrenar políticas de locomoción para el Go2 usando unitree_rl_mjlab en Google Colab Pro. Sin instalación local, sin GPU propia."
---

# Entrenamiento RL en Google Colab Pro

Esta guía cubre el flujo completo para entrenar una política de locomoción para el
Unitree Go2 usando Google Colab Pro, sin necesidad de GPU propia ni instalaciones
complejas de Isaac Sim.

## Colab vs. Cloud Run — no son lo mismo

Es importante entender que son herramientas para cosas distintas:

| | Cloud Run | Google Colab |
|---|---|---|
| **Qué es** | Servicio de contenedores serverless | Notebook Jupyter alojado |
| **Cómo se accede** | URL del sandbox del curso | Enlace al notebook `.ipynb` |
| **Infraestructura** | Tu imagen Docker, tus reglas | Infraestructura de Google |
| **GPU disponible** | L4 (garantizada) | T4 / V100 / A100 (best-effort) |
| **Duración de sesión** | Hasta 24h (Jobs) | 12h Pro / 24h Pro+ |
| **ROS 2** | ✅ Sí (contenedor completo) | ❌ No (no hay daemon support) |
| **Entrenamiento RL** | ✅ Sí (Cloud Run Jobs L4) | ✅ Sí (más simple) |
| **Uso en el curso** | Sandbox U1–U12 | Módulo RL avanzado |

**Resumen**: Cloud Run = ROS 2 interactivo. Colab = entrenamiento RL. No se reemplazan.

## ¿Por qué Colab Pro para RL?

Para el módulo de RL del curso, Colab Pro es la **mejor opción** por varias razones:

**Simplicidad**: los estudiantes abren un enlace, hacen clic en "Open in Colab" y
empiezan a entrenar en minutos. No hay Docker, gcloud CLI ni configuración de red.

**Costo**: $9.99/mes da acceso a A100 y T4. Un experimento típico (3 000 iteraciones
de Go2 en terreno plano) consume solo el **6–7% del presupuesto mensual** de un estudiante.

**Persistencia**: los modelos entrenados se guardan en Google Drive, que ya tienen los
estudiantes.

### ¿Por qué NO Isaac Lab en Colab?

Isaac Sim (sobre el que corre Isaac Lab) pesa ~50 GB y requiere drivers NVIDIA
específicos. Existe una solución no oficial ([j3soon/isaac-sim-colab](https://github.com/j3soon/isaac-sim-colab))
pero la instalación falla ocasionalmente y no es práctica para un curso.

**Solución**: usamos `unitree_rl_mjlab` — el framework oficial de Unitree que usa
**MuJoCo** como motor de física en lugar de Isaac Sim. La instalación completa es
`pip install -e .` (~2 minutos). Las políticas entrenadas se despliegan en el robot
real con el mismo pipeline (ONNX → C++ → SDK2).

## Precios de Google Colab

| Tier | Precio | Compute Units/mes | GPUs disponibles | Sesión máx. |
|---|---|---|---|---|
| **Free** | $0 | 30 CU | T4 (con límites) | 12h |
| **Pro** | $9.99/mes | 100 CU | T4 / V100 / A100 | 12h |
| **Pro+** | $49.99/mes | 500 CU | T4 / V100 / A100 | 24h |

### ¿Cuánto dura el crédito mensual?

| GPU | CU/hora | T4: horas/mes (Pro) | A100: horas/mes (Pro) |
|---|---|---|---|
| T4 | 1.76 CU/hr | **56.8 horas** | — |
| V100 | ~5.0 CU/hr | — | — |
| A100 | 15.0 CU/hr | — | **6.7 horas** |

Para un estudiante que solo usa Colab para RL del curso:
- 3 experimentos × 3 000 iter en T4 ≈ 3.5 hr = **6.2 CU** (6.2% del mes)
- 3 experimentos × 3 000 iter en A100 ≈ 0.5 hr = **7.5 CU** (7.5% del mes)

Un estudiante con Colab Pro puede hacer **10–15 experimentos de Go2 por mes** dentro del presupuesto.

## Tiempos de entrenamiento estimados

El entrenamiento de `unitree_rl_mjlab` usa MuJoCo (no Isaac Sim), que es más ligero
en GPU. La física paralela corre en CPU/GPU combinado. Estimaciones para 4 096 entornos:

| GPU | Terreno plano 3K iter | Terreno plano 10K iter | Terreno irregular 20K iter |
|---|---|---|---|
| RTX 4090 *(local)* | ~20 min | ~65 min | ~3.5 h |
| **A100 (Colab Pro)** | **~10 min** | **~30 min** | **~1.5 h** |
| **T4 (Colab Pro)** | **~70 min** | **~3.5 h** | **~12 h** |
| L4 (Cloud Run Jobs) | ~67 min | ~3.5 h | ~34 h |

!!! tip "T4 o A100 para el curso"
    Para experimentos de 3 000 iteraciones (suficiente para una política funcional),
    la T4 gratuita o de Pro tarda ~70 minutos — aceptable para una tarea de clase.
    Si disponible, selecciona A100 (Pro) para reducirlo a 10 minutos.

## Configuración del notebook

### Paso 1: Conseguir Google Colab Pro

Ir a [colab.research.google.com/settings](https://colab.research.google.com/) →
"Comprar unidades de procesamiento" o suscribirse a Pro ($9.99/mes).

!!! note "Free tier para experimentar"
    Puedes comenzar con la T4 gratuita (30 CU/mes). Si el entrenamiento falla por
    timeout de 12h (poco probable para 3K iter), actualiza a Pro.

### Paso 2: Abrir el notebook del curso

Abrir el notebook pre-configurado:

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TU_USUARIO/tu-repo/blob/main/notebooks/go2_rl_training.ipynb)

> Reemplaza el enlace con la URL de tu repositorio GitHub una vez que lo hayas subido.

### Paso 3: Seleccionar GPU

```
Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU → A100
```

Si A100 no está disponible (no hay cuota), selecciona T4. El notebook funciona con ambos.

### Paso 4: Ejecutar las celdas en orden

El notebook instala todo automáticamente. Solo necesitas ejecutar las celdas:

```
Celda 0 → verificar GPU         (~10 segundos)
Celda 1 → instalar deps sistema  (~60 segundos)
Celda 2 → clonar repo           (~30 segundos)
Celda 3 → pip install            (~90 segundos)
Celda 4 → verificar instalación  (~5 segundos)
Celda 5 → entrenamiento          (~10–70 min según GPU)
Celda 6 → guardar en Drive       (~30 segundos)
Celda 7 → visualizar política    (~opcional)
Celda 8 → exportar ONNX         (~10 segundos)
```

## Instalación manual (sin el notebook)

Si prefieres hacer el setup manualmente en una nueva sesión de Colab:

```python
# Celda 1: Sistema
!apt-get install -y -qq libyaml-cpp-dev libboost-all-dev libeigen3-dev \
    libspdlog-dev libfmt-dev xvfb ffmpeg

# Celda 2: Repositorio
!git clone --depth 1 https://github.com/unitreerobotics/unitree_rl_mjlab.git
%cd unitree_rl_mjlab

# Celda 3: Python
!pip install -e . --quiet

# Celda 4: Verificar
import mujoco, torch
print(f"MuJoCo {mujoco.__version__} | CUDA: {torch.cuda.is_available()}")
```

```python
# Celda 5: Entrenamiento
import subprocess, os

os.chdir("/content/unitree_rl_mjlab")
!python scripts/train.py Unitree-Go2-Flat \
    --env.scene.num-envs=2048 \
    --max_iterations=3000 \
    --headless
```

```python
# Celda 6: Guardar en Drive
from google.colab import drive
import shutil, glob
from datetime import datetime

drive.mount('/content/drive')
dest = f"/content/drive/MyDrive/unitree_rl/{datetime.now():%Y%m%d_%H%M}"
os.makedirs(dest)
shutil.copytree("logs", f"{dest}/logs", dirs_exist_ok=True)

# Copiar checkpoint
ckpts = sorted(glob.glob("logs/**/*.pt", recursive=True))
if ckpts: shutil.copy2(ckpts[-1], dest)
print(f"Guardado en Drive: {dest}")
```

## Robots soportados por unitree_rl_mjlab

El mismo framework entrena políticas para toda la línea Unitree:

| Robot | Tarea | Comando |
|---|---|---|
| Go2 | Terreno plano | `Unitree-Go2-Flat` |
| Go2 | Terreno irregular | `Unitree-Go2-Rough` |
| AS2 | Terreno plano | `Unitree-As2-Flat` |
| G1 | Terreno plano | `Unitree-G1-Flat` |
| G1 | Imitación de movimiento | `Unitree-G1-Tracking-No-State-Estimation` |
| H1_2 | Terreno plano | `Unitree-H1-2-Flat` |
| R1 | Terreno plano | `Unitree-R1-Flat` |

Para Go2 en terreno irregular (más avanzado):

```python
!python scripts/train.py Unitree-Go2-Rough \
    --env.scene.num-envs=1024 \    # menos entornos para terreno complejo
    --max_iterations=10000 \
    --headless
```

## Pipeline completo: Colab → Go2 real

```
1. Entrenar en Colab (este notebook)
   └─→ logs/.../model_3000.pt

2. Exportar a ONNX
   └─→ go2_policy.onnx

3. Copiar a Google Drive
   └─→ MyDrive/unitree_rl/go2_policy.onnx

4. Descargar en el host del robot (con Ethernet al Go2)
   └─→ scp go2_policy.onnx student@HOST:~/deploy/

5. Compilar controlador
   cd unitree_rl_mjlab/deploy && mkdir build && cd build
   cmake .. && make -j4

6. Poner Go2 en modo debug (L2 + R2 en el mando)

7. Ejecutar política
   ./unitree_go2_deploy --interface eth0 --policy ~/deploy/go2_policy.onnx
```

## Solución de problemas comunes

### OOM (sin memoria de GPU)

```python
# Reducir número de entornos paralelos:
!python scripts/train.py Unitree-Go2-Flat --env.scene.num-envs=1024 ...
# Si sigue fallando:
!python scripts/train.py Unitree-Go2-Flat --env.scene.num-envs=512  ...
```

### Sesión expirada durante el entrenamiento

El notebook guarda checkpoints automáticamente cada 50 iteraciones.
Si la sesión expira, reinicia y carga el último checkpoint:

```python
# Continuar desde checkpoint guardado en Drive
last_ckpt = "/content/drive/MyDrive/unitree_rl/go2_FECHA/logs/.../model_2500.pt"
!python scripts/train.py Unitree-Go2-Flat \
    --checkpoint_file={last_ckpt} \
    --max_iterations=3000 \
    --headless
```

### GPU no disponible (T4 en lugar de A100)

El notebook funciona con T4. El entrenamiento tardará ~70 min en lugar de ~10 min.
Puedes reducir iteraciones para una demo rápida:

```python
# Demo rápida en T4: 500 iteraciones (~12 minutos)
!python scripts/train.py Unitree-Go2-Flat --env.scene.num-envs=1024 --max_iterations=500
```

## Comparación de opciones de RL para el curso

| Opción | Setup | Costo/estudiante/semestre | Velocidad | Recomendado para |
|---|---|---|---|---|
| **Colab Pro** + mjlab | Abrir notebook | **$10/mes** | T4: 70min / A100: 10min | Curso RL (mejor opción) |
| Cloud Run Jobs L4 | Docker + gcloud | **$1.83/run** | ~67 min | Una vez, sin suscripción |
| CE Spot A100 | VM + setup | $0.18/run (flat) | ~10 min | Investigación seria |
| Local RTX 4090 | Instalación local | Solo electricidad | ~20 min | Quien tenga hardware |

**Recomendación para el curso**: Colab Pro a $9.99/mes es la opción más accesible,
más simple de gestionar como instructor, y da a cada estudiante suficientes recursos
para completar el módulo cómodamente.

---

Ver también:
- [Go2 en Isaac Lab](go2-isaac-lab.md) — para investigación avanzada con Isaac Sim
- [Go2 Hardware en profundidad](go2-hardware-profundo.md) — deployment en el robot real
- [Costos en la nube](../software/cloud-costos.md) — comparativa completa
