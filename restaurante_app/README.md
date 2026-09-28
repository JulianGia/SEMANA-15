# restaurante_app — Semana 15

Nombre:JOSE JULIAN GIA NARANJO

## Propósito

Esta semana se agrega la sección de **Ventas** a la aplicación gráfica de la
Semana 14 y se trabaja el manejo de eventos: el usuario presiona un botón,
`command=` ejecuta un callback, el callback le pide la operación al servicio
y la pantalla se actualiza con el resultado. También se incorporó la carpeta
`assets/` con el logo y los íconos del sistema.

## Qué se agregó respecto a la Semana 14

- Modelo `Venta` (usuario, producto, cantidad y fecha).
- Archivo `ventas.json` para guardar las ventas.
- Pestaña **Ventas** en la ventana principal.
- Logo en el login y en el encabezado, e íconos en las pestañas y botones.
- Login, gestión de productos y consulta de usuarios se mantienen igual.

## Estructura

```
restaurante_app/
├── assets/
│   ├── logo.png
│   ├── productos.png
│   ├── usuarios.png
│   ├── ventas.png
│   ├── registrar.png
│   └── salir.png
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── login_view.py
│   └── main_view.py
└── main.py
```

- **venta.py**: clase Venta, valida que la cantidad sea mayor que cero y
  guarda la fecha en que se hizo la venta.
- **archivo_servicio.py**: ahora también lee y guarda `ventas.json`.
- **restaurante_servicio.py**: tiene `registrar_venta()`, que revisa que el
  usuario y el producto existan y que alcance el stock; si todo está bien,
  descuenta el stock, agrega la venta y guarda `ventas.json` y
  `productos.json`.
- **main_view.py**: la pestaña Ventas tiene dos listas desplegables
  (usuario y producto), la cantidad, el botón **Registrar venta** y la tabla
  de ventas registradas.
- **ui/__init__.py**: función pequeña para cargar las imágenes de `assets/`.

## Eventos: command= y callback

El botón se crea así:

```python
ttk.Button(formulario, text="Registrar venta", command=self._registrar_venta)
```

Se pasa `self._registrar_venta` sin paréntesis, porque Tkinter es quien lo
llama cuando se presiona el botón. Ese callback:

1. Lee el usuario, el producto y la cantidad seleccionados.
2. Llama a `restaurante_servicio.registrar_venta(...)`.
3. Si el servicio lanza un `ValueError` (usuario o producto inexistente,
   cantidad inválida, stock insuficiente), muestra el mensaje en pantalla.
4. Si todo sale bien, recarga la tabla de ventas y la de productos (porque
   el stock cambió) y muestra el mensaje de éxito.

Las reglas y el guardado están en el servicio, no en la vista.

Flujo: botón → `command=` → callback → `RestauranteServicio` → JSON →
tabla actualizada.

## Persistencia

Las ventas se guardan en `datos/ventas.json` cada vez que se registra una.
Al abrir la aplicación se cargan junto con productos y usuarios.

## Cómo ejecutarlo

Desde la carpeta `restaurante_app/`:

```bash
python main.py
```

Usuario de prueba: `ana` / contraseña `1234`.

## Pruebas realizadas

- Ingreso con las credenciales de prueba y revisión de las tres pestañas.
- Venta sin seleccionar usuario o producto: muestra un aviso.
- Venta válida: aparece en la tabla, el stock baja y queda en `ventas.json`.
- Cantidad mayor al stock y cantidad 0: se rechazan sin cambiar nada.
- Se cerró y se volvió a abrir la aplicación: las ventas y el stock
  actualizado se recuperaron correctamente.
- Se comprobó que la gestión de productos y la consulta de usuarios siguen
  funcionando.
