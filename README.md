# Pronóstico de ventas y optimización de inventario

Predicción mensual de ventas para **250 productos** con **XGBoost** y pronóstico
recursivo, junto con el cálculo de stock de seguridad y punto de reorden para
reducir pérdidas por quiebres de stock.

## Objetivo

Pronosticar las ventas mensuales de 250 productos (histórico 2023–2025) para
planificar 2026 y realizar un diagnóstico retrospectivo del inventario (2025):
cuantificar pérdidas por roturas de stock y estimar el stock de seguridad y
punto de reorden teóricos por producto.

## Fuente de Datos

Fuente: [Warehouse Cost Optimization - Pharmaceutical Company](https://www.kaggle.com/datasets/kacperjarosik1/warehouse-cost-optimization-pharmaceutical-company/data) (Kaggle).

| Archivo | Descripción |
|---|---|
| `data/sales_train_2023_2024.csv` | Ventas e inventario mensual por producto (formato ancho), 2023–2024. |
| `data/sales_test_2025.csv` | Ídem, año 2025 (usado para validar el modelo). |
| `data/products_parameters.csv` | Parámetros por producto: precio, vida útil, lead time, stock de seguridad. |
| `data/financial_plan.csv` | Plan financiero anual 2023–2025 (baseline de comparación). |

## Pipeline (qué se hizo)

1. **EDA**: formato ancho → largo, separación de ventas e inventario.
2. **Stockouts**: meses con `Inventory_level == 0` → ventas perdidas en PLN.
3. **Features**: lags (1, 3, 6, 12) y media móvil de 3 meses por producto.
4. **Modelo**: `XGBRegressor` recursivo mes a mes, sin fuga de información.
5. **Inventario**: stock de seguridad y punto de reorden con demanda 2025.

## Resultados

- Validación del modelo para 2025: **MAE 24.43 / RMSE 56.62 unidades**.
- Pérdida estimada por quiebres de stock en 2025: **23.973 PLN**.
- Pronóstico 2026 exportado en `predicciones_2026.csv` (unidades y PLN por producto/mes).

## Comparación con el plan de la compañía (2025)

| Métrica | Plan | Modelo |
|---|---|---|
| Sesgo (unid/producto) | −84.7 | +11.5 |
| MAE (unid/producto) | 129.4 | 147.1 |

El plan subestima aprox 21,000 unidades por debajo del total real (280,919). El modelo es
insesgado y acierta el total con aprox 1% de error, aunque es más ruidoso por
producto.

## Limitaciones

- El modelo no usa variables de inventario (importancia casi nula).
- Datos ruidosos y con poca estacionalidad (el lag 12 aporta poca señal).
- El plan financiero llega solo hasta 2025, no hay plan 2026.
