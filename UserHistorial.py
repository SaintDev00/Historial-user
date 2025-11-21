inventario = []

def agregar_producto ():


print("\n" + "="*60)
print("AGREGAR NUEVO PRODUCTO")
print("="*60)

nombre=input("Ingrese el nombre del producto ")
if not nombre:
    print("El nombre no puede estar vacio")
    return


while True:

    precio = input("Ingrese el precio unitario del producto ")
    if not precio.isdigit():
          print("Ingrese un valor correcto")
          continue
    precio = float(precio)
    if precio <= 0:
         print("La cantidad debe ser mayor a cero")
         continue
    break
        
while True:
    cantidad = input("Ingrese la cantidad de unidades ")
    if not cantidad.isdigit():
          print("Ingrese un valor correcto")
          continue
    cantidad = int(cantidad)
    if cantidad <= 0:
         print("La cantidad debe ser mayor a cero")
         continue
    break

    
    
costo_total = precio*cantidad
    
producto = {
     "nombre": nombre,
     "precio": precio,
     "cantidad": cantidad,
     "costo_total": costo_total
}
inventario.append(producto)
      
print("\n PRODUCTO REGISTRADO CORRECTAMENTE")
print(f"producto: {nombre}")
print(f"precio unitario: {precio:.2f}")       
print(f"cantidad: {cantidad:.2f}")  
print(f"costo_total: {costo_total:.2f}")       
print("="*60)
 
def mostrar_inventario (): 


 
 
 
 
 
 
    #Separador visual
print("\n" + "="*60)
print("INFORMACION DEL PRODUCTO REGISTRADO")
print("="*60)

#Mostrar toda la informacion del producto

print(f"Producto: {nombre}")
print(f"Precio unitario: {precio:.2f}")
print(f"Cantidad: {cantidad} unidades")
print(f"costo_total:  {costo_total:.2f}")

print("="*60)
print("\n Producto registrado correctamente")