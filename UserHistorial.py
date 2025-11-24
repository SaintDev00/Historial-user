"""
================================================================================
SISTEMA DE GESTIÓN DE INVENTARIO - MÓDULO 1 COMPLETO
Integración de Semanas 1, 2 y 3
================================================================================
SEMANA 1: Registro básico de productos con validación
SEMANA 2: Control de flujo, listas, múltiples productos y estadísticas
SEMANA 3: Persistencia con archivos CSV (guardar/cargar)
================================================================================
"""

import csv
import os

# ============================================================================
# VARIABLES GLOBALES
# ============================================================================

# Lista global para almacenar todos los productos del inventario
inventario = []


# ============================================================================
# FUNCIONES DE VALIDACIÓN (SEMANA 1)
# ============================================================================

def validar_numero(mensaje, tipo="float", minimo=0):
    """
    Solicita y valida entrada numérica del usuario.
    
    Parámetros:
        mensaje (str): Mensaje a mostrar al usuario
        tipo (str): Tipo de dato esperado ("float" o "int")
        minimo (float/int): Valor mínimo aceptable
    
    Retorna:
        float o int: Valor validado según el tipo especificado
    """
    while True:
        try:
            entrada = input(mensaje)
            
            # Convertir según el tipo solicitado
            if tipo == "float":
                valor = float(entrada)
            else:
                valor = int(entrada)
            
            # Validar que sea mayor o igual al mínimo
            if valor < minimo:
                print(f"ERROR: El valor debe ser mayor o igual a {minimo}")
                continue
            
            return valor
            
        except ValueError:
            print(f"ERROR: Ingrese un valor numérico válido")


# ============================================================================
# FUNCIONES CRUD - OPERACIONES BÁSICAS (SEMANA 2)
# ============================================================================

def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto
        precio (float): Precio unitario del producto
        cantidad (int): Cantidad de unidades
    
    Retorna:
        bool: True si se agregó exitosamente, False si ya existe
    """
    # Verificar si el producto ya existe
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            print(f"ERROR: El producto '{nombre}' ya existe en el inventario.")
            return False
    
    # Crear y agregar nuevo producto
    producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }
    inventario.append(producto)
    print(f"EXITO: Producto '{nombre}' agregado exitosamente.")
    return True


def mostrar_inventario(inventario):
    """
    Muestra todos los productos del inventario en formato tabla.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
    """
    if len(inventario) == 0:
        print("\nADVERTENCIA: El inventario está vacío.")
        return
    
    print("\n" + "="*80)
    print(f"{'PRODUCTO':<30} {'PRECIO':>12} {'CANTIDAD':>12} {'SUBTOTAL':>15}")
    print("="*80)
    
    for producto in inventario:
        subtotal = producto["precio"] * producto["cantidad"]
        print(f"{producto['nombre']:<30} ${producto['precio']:>10.2f} "
            f"{producto['cantidad']:>12} ${subtotal:>13.2f}")
    
    print("="*80)


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre en el inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto a buscar
    
    Retorna:
        dict o None: Diccionario del producto si existe, None si no se encuentra
        """
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o cantidad de un producto existente.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto a actualizar
        nuevo_precio (float, opcional): Nuevo precio unitario
        nueva_cantidad (int, opcional): Nueva cantidad
    
    Retorna:
        bool: True si se actualizó, False si no se encontró
    """
    producto = buscar_producto(inventario, nombre)
    
    if producto is None:
        print(f"ERROR: Producto '{nombre}' no encontrado.")
        return False
    
    # Actualizar los campos proporcionados
    if nuevo_precio is not None:
        producto["precio"] = nuevo_precio
    if nueva_cantidad is not None:
        producto["cantidad"] = nueva_cantidad
    
    print(f"EXITO: Producto '{nombre}' actualizado exitosamente.")
    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        nombre (str): Nombre del producto a eliminar
    
    Retorna:
        bool: True si se eliminó, False si no se encontró
    """
    producto = buscar_producto(inventario, nombre)
    
    if producto is None:
        print(f"ERROR: Producto '{nombre}' no encontrado.")
        return False
    
    inventario.remove(producto)
    print(f"EXITO: Producto '{nombre}' eliminado exitosamente.")
    return True


# ============================================================================
# FUNCIONES DE ESTADÍSTICAS (SEMANA 2)
# ============================================================================

def calcular_estadisticas(inventario):
    """
    Calcula estadísticas del inventario.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
    
    Retorna:
        dict: Diccionario con las estadísticas calculadas o None si está vacío
    """
    if len(inventario) == 0:
        return None
    
    # Función lambda para calcular subtotal de cada producto
    subtotal = lambda p: p["precio"] * p["cantidad"]
    
    # Calcular unidades totales
    unidades_totales = sum(p["cantidad"] for p in inventario)
    
    # Calcular valor total del inventario
    valor_total = sum(subtotal(p) for p in inventario)
    
    # Producto más caro
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    
    # Producto con mayor stock
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])
    
    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock
    }


def mostrar_estadisticas(inventario):
    """
    Muestra las estadísticas del inventario en formato legible.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
    """
    stats = calcular_estadisticas(inventario)
    
    if stats is None:
        print("\nADVERTENCIA: No hay productos para calcular estadísticas.")
        return
    
    print("\n" + "="*70)
    print("ESTADÍSTICAS DEL INVENTARIO")
    print("="*70)
    print(f"Total de productos diferentes: {len(inventario)}")
    print(f"Unidades totales en stock: {stats['unidades_totales']}")
    print(f"Valor total del inventario: ${stats['valor_total']:.2f}")
    print(f"\nProducto más caro:")
    print(f"   - {stats['producto_mas_caro']['nombre']}: "
        f"${stats['producto_mas_caro']['precio']:.2f}")
    print(f"\nProducto con mayor stock:")
    print(f"   - {stats['producto_mayor_stock']['nombre']}: "
        f"{stats['producto_mayor_stock']['cantidad']} unidades")
    print("="*70)


# ============================================================================
# FUNCIONES DE PERSISTENCIA - CSV (SEMANA 3)
# ============================================================================

def guardar_csv(inventario, ruta="inventario.csv", incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.
    
    Parámetros:
        inventario (list): Lista de diccionarios con los productos
        ruta (str): Ruta del archivo CSV donde guardar
        incluir_header (bool): Si se debe incluir encabezado
    
    Retorna:
        bool: True si se guardó exitosamente, False en caso de error
    """
    # Validar que el inventario no esté vacío
    if len(inventario) == 0:
        print("\nERROR: El inventario está vacío. No hay nada que guardar.")
        return False
    
    try:
        # Abrir archivo en modo escritura
        with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            
            # Escribir encabezado si se solicita
            if incluir_header:
                writer.writerow(['nombre', 'precio', 'cantidad'])
            
            # Escribir cada producto
            for producto in inventario:
                writer.writerow([
                    producto['nombre'],
                    producto['precio'],
                    producto['cantidad']
                ])
        
        print(f"\nEXITO: Inventario guardado exitosamente en: {ruta}")
        return True
    
    except PermissionError:
        print(f"\nERROR: No se tienen permisos para escribir en '{ruta}'")
        return False
    except IOError as e:
        print(f"\nERROR de escritura: {e}")
        return False
    except Exception as e:
        print(f"\nERROR inesperado al guardar: {e}")
        return False


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV.
    
    Parámetros:
        ruta (str): Ruta del archivo CSV a cargar
    
    Retorna:
        tuple: (lista_productos, filas_invalidas)
            lista_productos: lista de diccionarios con productos válidos
            filas_invalidas: número de filas que no se pudieron procesar
    """
    productos = []
    filas_invalidas = 0
    
    try:
        # Verificar si el archivo existe
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"El archivo '{ruta}' no existe")
        
        with open(ruta, 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            
            # Leer encabezado
            try:
                header = next(reader)
                # Validar encabezado
                if header != ['nombre', 'precio', 'cantidad']:
                    print(f"\nERROR: Formato de encabezado inválido. "
                        f"Se esperaba: nombre,precio,cantidad")
                    return productos, -1
            except StopIteration:
                print(f"\nERROR: El archivo está vacío")
                return productos, -1
            
            # Leer cada fila
            for num_fila, fila in enumerate(reader, start=2):
                try:
                    # Validar que tenga exactamente 3 columnas
                    if len(fila) != 3:
                        filas_invalidas += 1
                        continue
                    
                    nombre, precio_str, cantidad_str = fila
                    
                    # Validar y convertir precio
                    precio = float(precio_str)
                    if precio < 0:
                        filas_invalidas += 1
                        continue
                    
                    # Validar y convertir cantidad
                    cantidad = int(cantidad_str)
                    if cantidad < 0:
                        filas_invalidas += 1
                        continue
                    
                    # Validar nombre no vacío
                    if not nombre.strip():
                        filas_invalidas += 1
                        continue
                    
                    # Agregar producto válido
                    productos.append({
                        "nombre": nombre.strip(),
                        "precio": precio,
                        "cantidad": cantidad
                    })
                
                except ValueError:
                    filas_invalidas += 1
                    continue
                except Exception:
                    filas_invalidas += 1
                    continue
        
        return productos, filas_invalidas
    
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        return productos, -1
    except UnicodeDecodeError:
        print(f"\nERROR: El archivo no tiene codificación válida (UTF-8)")
        return productos, -1
    except Exception as e:
        print(f"\nERROR inesperado al cargar archivo: {e}")
        return productos, -1


def fusionar_inventarios(inventario_actual, productos_nuevos):
    """
    Fusiona productos nuevos con el inventario actual.
    
    Política de fusión:
    - Si el producto existe: suma cantidades y actualiza precio al nuevo
    - Si el producto no existe: lo agrega
    
    Parámetros:
        inventario_actual (list): Inventario actual
        productos_nuevos (list): Productos a fusionar
    
    Retorna:
        int: Número de productos fusionados/agregados
    """
    productos_procesados = 0
    
    for nuevo in productos_nuevos:
        producto_existente = buscar_producto(inventario_actual, nuevo["nombre"])
        
        if producto_existente:
            # Actualizar producto existente
            producto_existente["cantidad"] += nuevo["cantidad"]
            producto_existente["precio"] = nuevo["precio"]
            productos_procesados += 1
        else:
            # Agregar nuevo producto
            inventario_actual.append(nuevo)
            productos_procesados += 1
    
    return productos_procesados


# ============================================================================
# FUNCIONES DE MENÚ (SEMANA 2)
# ============================================================================

def menu_agregar(inventario):
    """Menú para agregar un producto (SEMANA 1 integrada)."""
    print("\n" + "="*70)
    print("AGREGAR PRODUCTO")
    print("="*70)
    
    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print("ERROR: El nombre no puede estar vacío")
        return
    
    precio = validar_numero("Precio unitario: $", "float", 0.01)
    cantidad = validar_numero("Cantidad: ", "int", 1)
    
    agregar_producto(inventario, nombre, precio, cantidad)


def menu_mostrar(inventario):
    """Menú para mostrar el inventario completo."""
    print("\n" + "="*70)
    print("INVENTARIO COMPLETO")
    print("="*70)
    mostrar_inventario(inventario)


def menu_buscar(inventario):
    """Menú para buscar un producto específico."""
    print("\n" + "="*70)
    print("BUSCAR PRODUCTO")
    print("="*70)
    
    nombre = input("Nombre del producto a buscar: ").strip()
    producto = buscar_producto(inventario, nombre)
    
    if producto:
        print("\nEXITO: Producto encontrado:")
        print(f"   - Nombre: {producto['nombre']}")
        print(f"   - Precio: ${producto['precio']:.2f}")
        print(f"   - Cantidad: {producto['cantidad']} unidades")
        print(f"   - Subtotal: ${producto['precio'] * producto['cantidad']:.2f}")
    else:
        print(f"\nERROR: Producto '{nombre}' no encontrado")


def menu_actualizar(inventario):
    """Menú para actualizar un producto existente."""
    print("\n" + "="*70)
    print("ACTUALIZAR PRODUCTO")
    print("="*70)
    
    nombre = input("Nombre del producto a actualizar: ").strip()
    producto = buscar_producto(inventario, nombre)
    
    if not producto:
        print(f"\nERROR: Producto '{nombre}' no encontrado")
        return
    
    print(f"\nProducto actual: {producto['nombre']}")
    print(f"Precio actual: ${producto['precio']:.2f}")
    print(f"Cantidad actual: {producto['cantidad']}")
    
    print("\n(Presiona Enter para mantener el valor actual)")
    
    # Actualizar precio
    precio_input = input("Nuevo precio (Enter para no cambiar): $").strip()
    nuevo_precio = None
    if precio_input != "":
        try:
            nuevo_precio = float(precio_input)
            if nuevo_precio < 0:
                print("ERROR: Precio inválido, se mantendrá el actual")
                nuevo_precio = None
        except ValueError:
            print("ERROR: Precio inválido, se mantendrá el actual")
            nuevo_precio = None
    
    # Actualizar cantidad
    cantidad_input = input("Nueva cantidad (Enter para no cambiar): ").strip()
    nueva_cantidad = None
    if cantidad_input != "":
        try:
            nueva_cantidad = int(cantidad_input)
            if nueva_cantidad < 0:
                print("ERROR: Cantidad inválida, se mantendrá la actual")
                nueva_cantidad = None
        except ValueError:
            print("ERROR: Cantidad inválida, se mantendrá la actual")
            nueva_cantidad = None
    
    actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)


def menu_eliminar(inventario):
    """Menú para eliminar un producto."""
    print("\n" + "="*70)
    print("ELIMINAR PRODUCTO")
    print("="*70)
    
    nombre = input("Nombre del producto a eliminar: ").strip()
    
    # Buscar y mostrar el producto antes de eliminar
    producto = buscar_producto(inventario, nombre)
    if producto:
        print(f"\nProducto: {producto['nombre']}")
        print(f"Precio: ${producto['precio']:.2f}")
        print(f"Cantidad: {producto['cantidad']}")
        
        confirmacion = input(f"\n¿Está seguro de eliminar '{nombre}'? (S/N): ").strip().upper()
        if confirmacion == "S":
            eliminar_producto(inventario, nombre)
        else:
            print("ERROR: Eliminación cancelada")
    else:
        print(f"\nERROR: Producto '{nombre}' no encontrado")


def menu_guardar_csv(inventario):
    """Menú para guardar el inventario en CSV (SEMANA 3)."""
    print("\n" + "="*70)
    print("GUARDAR INVENTARIO EN CSV")
    print("="*70)
    
    ruta = input("Nombre del archivo (Enter para 'inventario.csv'): ").strip()
    if not ruta:
        ruta = "inventario.csv"
    
    if not ruta.endswith('.csv'):
        ruta += '.csv'
    
    guardar_csv(inventario, ruta)


def menu_cargar_csv(inventario):
    """Menú para cargar el inventario desde CSV (SEMANA 3)."""
    print("\n" + "="*70)
    print("CARGAR INVENTARIO DESDE CSV")
    print("="*70)
    
    ruta = input("Nombre del archivo a cargar (ej: inventario.csv): ").strip()
    
    productos_cargados, filas_invalidas = cargar_csv(ruta)
    
    if filas_invalidas == -1:
        return  # Error crítico, ya se mostró mensaje
    
    if len(productos_cargados) == 0:
        print("\nADVERTENCIA: No se cargaron productos válidos del archivo")
        return
    
    print(f"\nEXITO: Se leyeron {len(productos_cargados)} productos válidos")
    if filas_invalidas > 0:
        print(f"ADVERTENCIA: {filas_invalidas} filas inválidas fueron omitidas")
    
    # Preguntar acción: sobrescribir o fusionar
    if len(inventario) > 0:
        print(f"\nADVERTENCIA: El inventario actual tiene {len(inventario)} productos")
        print("Política de fusión:")
        print("  - Si el producto existe: suma cantidades y actualiza precio")
        print("  - Si el producto no existe: lo agrega\n")
        
        accion = input("¿Sobrescribir inventario actual? (S/N): ").strip().upper()
        
        if accion == "S":
            inventario.clear()
            inventario.extend(productos_cargados)
            print(f"\nEXITO: Inventario reemplazado. {len(inventario)} productos cargados.")
        else:
            procesados = fusionar_inventarios(inventario, productos_cargados)
            print(f"\nEXITO: Inventario fusionado. {procesados} productos procesados.")
            print(f"Total de productos en inventario: {len(inventario)}")
    else:
        inventario.extend(productos_cargados)
        print(f"\nEXITO: {len(productos_cargados)} productos cargados al inventario.")


def mostrar_menu_principal():
    """Muestra el menú principal del sistema."""
    print("\n" + "="*70)
    print("SISTEMA DE GESTIÓN DE INVENTARIO - MÓDULO 1 COMPLETO")
    print("="*70)
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Estadísticas")
    print("7. Guardar CSV")
    print("8. Cargar CSV")
    print("9. Salir")
    print("="*70)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta el programa con un menú interactivo.
    Integra todas las funcionalidades de las 3 semanas.
    """
    print("\n" + "="*70)
    print("BIENVENIDO AL SISTEMA DE GESTIÓN DE INVENTARIO")
    print("Módulo 1 - Semanas 1, 2 y 3 integradas")
    print("="*70)
    
    while True:
        try:
            mostrar_menu_principal()
            opcion = input("Seleccione una opción (1-9): ").strip()
            
            if opcion == "1":
                menu_agregar(inventario)
            
            elif opcion == "2":
                menu_mostrar(inventario)
            
            elif opcion == "3":
                menu_buscar(inventario)
            
            elif opcion == "4":
                menu_actualizar(inventario)
            
            elif opcion == "5":
                menu_eliminar(inventario)
            
            elif opcion == "6":
                mostrar_estadisticas(inventario)
            
            elif opcion == "7":
                menu_guardar_csv(inventario)
            
            elif opcion == "8":
                menu_cargar_csv(inventario)
            
            elif opcion == "9":
                print("\n" + "="*70)
                print("Gracias por usar el Sistema de Gestión de Inventario")
                print("="*70 + "\n")
                break
            
            else:
                print("\nERROR: Opción inválida. Por favor, seleccione un número del 1 al 9.")
        
        except KeyboardInterrupt:
            print("\n\nADVERTENCIA: Programa interrumpido por el usuario")
            break
        except Exception as e:
            print(f"\nERROR inesperado: {e}")
            print("El programa continuará ejecutándose...")


# ============================================================================
# EJECUCIÓN DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    main()


# ============================================================================
# DOCUMENTACIÓN FINAL DEL SISTEMA COMPLETO
# ============================================================================
"""
RESUMEN DEL SISTEMA INTEGRADO - 3 SEMANAS:

SEMANA 1 - FUNDAMENTOS:
- Validación de entrada de datos (nombre, precio, cantidad)
- Variables y tipos de datos (string, float, int)
- Operaciones matemáticas (costo total)
- Manejo de errores con try-except
- Conversión de tipos

SEMANA 2 - CONTROL DE FLUJO Y ESTRUCTURAS:
- Menú interactivo con 9 opciones
- Estructuras condicionales (if/elif/else)
- Bucles (while y for)
- Listas de diccionarios para almacenar productos
- Operaciones CRUD completas:
      * Agregar productos
      * Mostrar inventario
      * Buscar productos
      * Actualizar productos
      * Eliminar productos
- Estadísticas del inventario:
      * Unidades totales
      * Valor total
      * Producto más caro
      * Producto con mayor stock
- Uso de funciones lambda

SEMANA 3 - PERSISTENCIA Y ARCHIVOS:
- Guardar inventario en archivos CSV
- Cargar inventario desde archivos CSV
- Validación completa de formato CSV
- Manejo de errores de archivos:
      * FileNotFoundError
      * UnicodeDecodeError
      * PermissionError
      * IOError
- Opciones de sobrescribir o fusionar inventarios
- Política de fusión clara
- Reporte de filas inválidas

CARACTERÍSTICAS GENERALES:
- Código modular con funciones documentadas
- Docstrings completos para cada función
- Comentarios explicativos
- Validaciones robustas
- Manejo de excepciones
- Interfaz de usuario amigable
- Mensajes claros de éxito/error
- Sistema que no se cierra ante errores

FORMATO DE ARCHIVO CSV:
nombre,precio,cantidad
Laptop,1200.50,5
Mouse,25.99,20
Teclado,85.00,15

USO DEL SISTEMA:
1. Ejecutar: python inventario.py
2. Seleccionar opción del menú (1-9)
3. Seguir las instrucciones en pantalla
4. Guardar/Cargar CSV según necesidad
5. Opción 9 para salir

CONCEPTOS DE PYTHON APLICADOS:
- Variables y tipos de datos
- Funciones con parámetros y retorno
- Listas y diccionarios
- Bucles (while, for)
- Condicionales (if/elif/else)
- Manejo de excepciones (try/except)
- Funciones lambda
- Módulo CSV
- Módulo OS
- Docstrings
- Validación de datos
- Entrada/Salida de archivos
"""
