# E2E

Pruebas end-to-end con BDD, DDT y Selenium usando `behave`.

## Requisitos

- Python 3.12+
- Google Chrome instalado

## Instalacion

```bash
python3 -m pip install -r requirements.txt
```

## Ejecucion

```bash
python3 -m behave e2e/features
```

## Que cubre

- Busca una universidad en Google
- Abre el primer resultado que coincide con el dominio esperado
- Verifica que el navegador este en el sitio correcto
- Hace una busqueda interna en el sitio de la universidad
- Valida contenido relacionado al termino buscado

## Universidades incluidas

- ITESO
- Tecnologico de Monterrey
- Universidad de Guadalajara

## Comprimir entrega

```bash
zip -r e2e.zip e2e
```
