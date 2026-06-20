---
title: "Costos en la Nube: Sandbox + RL"
description: "Estimación detallada de costos en Google Cloud Run para el sandbox del curso y entrenamiento RL con Isaac Lab para Unitree Go2/G1."
---

# Costos del curso en la nube

Referencia de costos para operar el sandbox del curso (U1-U12) y el módulo avanzado
de RL con Isaac Lab, en Google Cloud Platform.

## Precios base de Cloud Run (us-central1, Tier 1)

| Recurso | Precio | Equivalente horario |
|---|---|---|
| CPU | $0.000024 / vCPU-segundo | $0.086 / vCPU-hora |
| Memoria | $0.0000025 / GiB-segundo | $0.009 / GiB-hora |
| GPU L4 | $0.0001867 / segundo | **$0.672 / hora** |
| GPU RTX PRO 6000 | $0.0008065 / segundo | **$2.90 / hora** |
| Requests | $0.40 / millón (primeros 2M gratis) | — |

**Contenedor sandbox del curso** (4 vCPU + 4 GiB, sin GPU):
```
4 × $0.086 + 4 × $0.009 = $0.344 + $0.036 = $0.38 / hora por estudiante activo
```

**Contenedor RL con L4** (8 vCPU + 32 GiB + 1× L4):
```
8 × $0.086 + 32 × $0.009 + $0.672 = $0.688 + $0.288 + $0.672 = $1.65 / hora
```

---

## Sandbox del curso — costo por semestre

### Supuestos de uso (estudiantes después de clases)

| Parámetro | Valor |
|---|---|
| Acceso | Después de clases (17:00–22:00 días hábiles) |
| Sesiones promedio por estudiante | 2.5 sesiones/semana |
| Duración promedio por sesión | 1.75 horas |
| Horas activas/semana/estudiante | 4.4 horas |
| Horas activas/semestre/estudiante | **61 horas** |
| Duración del semestre | 14 semanas |

### Costo estimado por semestre

| Componente | 20 estudiantes | 25 estudiantes | 30 estudiantes |
|---|---|---|---|
| Sesiones activas @ $0.38/hr | $467 | $584 | $701 |
| 1 instancia en caliente (pico) | $107 | $107 | $107 |
| Almacenamiento (código, ~10 GB/estudiante) | $4 | $5 | $6 |
| Egress y misceláneos | $5 | $5 | $5 |
| **Total semestral** | **$583** | **$701** | **$819** |
| **Por estudiante** | **$29** | **$28** | **$27** |

### Estrategia de calentamiento (warm instances)

Para evitar esperas de cold start durante el horario de clases sin pagar por
instancias inactivas todo el día:

```yaml
# cloud-run-warmup.yaml — schedule Cloud Run Job
schedules:
  - name: warm-sandbox-morning
    cron: "0 17 * * 1-5"    # 17:00 lunes a viernes
    action: ping_sandbox
  - name: stop-sandbox-midnight
    cron: "0 22 * * 1-5"    # 22:00 lunes a viernes
    action: set_min_instances_zero
```

En el horario pico (17:00-22:00 L-V): mantener 1 instancia mínima → $0.38 × 4hr × 5d × 14w = $107.
Fuera del horario: min-instances = 0, cold start ~15-20 segundos (aceptable).

---

## Estimación anual (3 cohortes)

| Cohorte | Estudiantes | Semanas | Costo | Por estudiante |
|---|---|---|---|---|
| Semestre 1 | 30 | 14 | $929 | $31 |
| Semestre 2 | 25 | 14 | $793 | $32 |
| Módulo corto | 15 | 8 | $324 | $22 |
| **Total anual** | **70** | — | **$2 046** | **$29** |

---

## Módulo RL (Isaac Lab) — requisitos y costos

### Requisitos de Isaac Sim 5.1.0

| Nivel | GPU | VRAM | RAM | Almacenamiento |
|---|---|---|---|---|
| Mínimo (RL headless) | RTX 4080 | 16 GB | 32 GB | 50 GB SSD |
| Recomendado (visual) | RTX 5080 | 16 GB | 64 GB | 500 GB SSD |
| Ideal (multi-entorno) | RTX PRO 6000 | 48 GB | 64 GB | 1 TB NVMe |

!!! note "Headless vs. visual"
    Para entrenamiento de RL (`--headless`), **no se usa RTX rendering**. El cuello de
    botella es la simulación física de PhysX en paralelo, que depende más de **ancho de
    banda de memoria** que de CUDA cores de renderizado. En headless la GPU mínima
    baja de RTX 4080 a cualquier tarjeta con ≥ 12 GB VRAM y buen ancho de banda.

### GPUs disponibles en la nube y compatibilidad

| Servicio | GPU | VRAM | Ancho de banda | Precio | Headless RL |
|---|---|---|---|---|---|
| **Cloud Run Jobs** | NVIDIA L4 | 24 GB | 300 GB/s | $0.67/hr | ✓ Funciona |
| **Cloud Run Services** | RTX PRO 6000 Blackwell | 96 GB | ~1 600 GB/s | $2.90/hr | ✓ Óptimo |
| **CE g2-standard-8** | L4 (on-demand) | 24 GB | 300 GB/s | $1.50/hr | ✓ Funciona |
| **CE a2-highgpu-1g (OD)** | A100 SXM 40 GB | 40 GB | 1 555 GB/s | $3.67/hr | ✓✓ Más rápido |
| **CE a2-highgpu-1g (Spot)** | A100 SXM 40 GB | 40 GB | 1 555 GB/s | $1.10/hr | ✓✓ Recomendado |

### Tiempos de entrenamiento estimados

El entrenamiento de locomoción en Isaac Lab con 4 096 entornos paralelos está
limitado principalmente por el **ancho de banda de memoria GPU** (simulación PhysX).

| GPU | Banda (GB/s) | Terreno plano 3 000 iter. | Curricula completo 20 000 iter. |
|---|---|---|---|
| RTX 4090 *(referencia)* | 1 008 | ~20 min | ~10 h |
| A100 SXM 40 GB | 1 555 | **~10 min** | **~5 h** |
| NVIDIA L4 | 300 | ~67 min | ~34 h |
| RTX 5080 | 1 792 | ~9 min | ~4.5 h |

### Costo por experimento de entrenamiento

| Tarea | Cloud Run L4 | CE A100 Spot | CE A100 OD |
|---|---|---|---|
| Terreno plano, 3 000 iter. *(curso básico)* | **$1.83** | **$0.18** | $0.61 |
| Curricula completa, 20 000 iter. *(investigación)* | $55 ❌ | **$5.54** ✓ | $18.50 |

!!! warning "L4 no es práctico para training largo"
    El entrenamiento completo de curricula de terreno irregular tarda ~34 horas en L4
    y costaría $55/run. Para investigación seria usa **Compute Engine Spot A100**
    ($5.54/run) o accede a través de Vertex AI.

### Presupuesto RL para el curso (módulo opcional)

30 estudiantes × 2 experimentos simples (terreno plano):

| Opción | Total | Por estudiante |
|---|---|---|
| Cloud Run Jobs L4 | $110 | $3.67 |
| Compute Engine A100 Spot | **$11** | **$0.37** |

---

## Cómo usar Cloud Run Jobs para RL

```bash
# 1. Construir imagen con Isaac Lab
# Usar imagen base oficial de NVIDIA NGC:
FROM nvcr.io/nvidia/isaac-lab:2.3.0

# Clonar unitree_rl_lab dentro de la imagen
RUN git clone https://github.com/unitreerobotics/unitree_rl_lab /unitree_rl_lab
WORKDIR /unitree_rl_lab

# 2. Subir imagen a Google Artifact Registry
docker tag mi-isaaclab-imagen gcr.io/MI_PROYECTO/isaaclab-go2:latest
docker push gcr.io/MI_PROYECTO/isaaclab-go2:latest

# 3. Lanzar Cloud Run Job con GPU L4
gcloud run jobs create go2-rl-train \
  --image gcr.io/MI_PROYECTO/isaaclab-go2:latest \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --cpu 8 \
  --memory 32Gi \
  --task-timeout 7200 \        # 2 horas máximo
  --region us-central1 \
  --command ./unitree_rl_lab.sh \
  --args "-t,--task,Unitree-Go2-Velocity-v0,--headless,--max_iterations,3000"

# 4. Ejecutar el job
gcloud run jobs execute go2-rl-train

# 5. Recuperar el checkpoint entrenado desde Cloud Storage
# (configurar output a GCS en el script de training)
```

!!! note "Cold start de Isaac Sim"
    Isaac Sim tarda 5-8 minutos en inicializar incluso en modo headless.
    Este tiempo forma parte del costo. Para experimentos de 20-67 min,
    el overhead es del 10-25% — asumido en las estimaciones de arriba.

---

## Alternativas más baratas para RL

### Google Colab Pro ($10/mes por estudiante)

Para el módulo RL del curso, Colab Pro con `unitree_rl_mjlab` es la **mejor opción**
(no Isaac Lab — requiere 50 GB y drivers no soportados en Colab):
- Acceso a A100 / V100 en Colab Pro
- ~100 compute units/mes ≈ 6.7 horas A100 / 56 horas T4
- 3 experimentos de Go2 flat (3K iter) consumen solo el 6–7% del presupuesto mensual

```python
# En Colab Pro (A100 o T4) — unitree_rl_mjlab (MuJoCo, sin Isaac Sim):
!git clone --depth 1 https://github.com/unitreerobotics/unitree_rl_mjlab.git
%cd unitree_rl_mjlab
!pip install -e . --quiet
!python scripts/train.py Unitree-Go2-Flat \
    --env.scene.num-envs=2048 --max_iterations=3000 --headless
# A100: ~10 min / T4: ~70 min — un experimento ≈ 2 CU
```

Ver guía completa: [RL en Google Colab](../unitree/go2-colab-rl.md)

### RunPod / Vast.ai (A100 spot del mercado)

Para investigación extendida fuera del ecosistema GCP:
- RunPod A100 SXM: ~$1.29-1.49/hr
- Vast.ai A100: ~$0.85-1.20/hr (mercado de spot, variable)
- Más barato que Cloud Run L4 para sessiones largas

---

## Resumen de decisiones

| Escenario | Plataforma recomendada | Costo típico |
|---|---|---|
| Curso U1-U12 completo | **Cloud Run** (sin GPU) | $27-31/estudiante/semestre |
| RL módulo del curso (3K iter) | **Google Colab Pro** + unitree_rl_mjlab | $10/mes/estudiante |
| RL investigación (20K iter) | **CE Spot A100** + Isaac Lab | $5.54/experimento |
| RL una sola vez, sin suscripción | **Cloud Run Jobs L4** | $1.83/experimento |

**El curso base (U1-U12 con sim_lite) NO requiere GPU en ningún momento.**
GPU solo se necesita para el módulo opcional de Isaac Lab (go2-isaac-lab.md).
