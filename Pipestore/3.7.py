import pickle
import os
from datetime import datetime

class Producto:
    def __init__(self, nombre, peso, altura, anchura, categoria, unidades=1):
        self.nombre = nombre
        self.peso = peso
        self.altura = altura
        self.anchura = anchura
        self.categoria = categoria
        self.unidades = unidades

    def __str__(self):
        return (f"{self.nombre} (Peso: {self.peso} kg, Altura: {self.altura} m, Anchura: {self.anchura} m, "
                f"Categoría: {self.categoria}, Unidades: {self.unidades})")

class Almacen:
    def __init__(self, nombre, capacidad_peso, capacidad_altura, capacidad_anchura, categoria):
        self.nombre = nombre
        self.capacidad_peso = capacidad_peso
        self.capacidad_altura = capacidad_altura
        self.capacidad_anchura = capacidad_anchura
        self.categoria = categoria
        self.peso_utilizado = 0
        self.altura_utilizada = 0
        self.anchura_utilizada = 0
        self.productos = []

    def almacenar_producto(self, producto):
        total_peso = producto.peso * producto.unidades
        total_altura = producto.altura * producto.unidades
        total_anchura = producto.anchura * producto.unidades

        if (self.peso_utilizado + total_peso <= self.capacidad_peso and
            self.altura_utilizada + total_altura <= self.capacidad_altura and
            self.anchura_utilizada + total_anchura <= self.capacidad_anchura):
            self.peso_utilizado += total_peso
            self.altura_utilizada += total_altura
            self.anchura_utilizada += total_anchura

            for p in self.productos:
                if p.nombre == producto.nombre:
                    p.unidades += producto.unidades
                    return True

            self.productos.append(producto)
            return True
        return False

    def eliminar_producto(self, nombre_producto, unidades):
        for producto in self.productos:
            if producto.nombre == nombre_producto:
                if producto.unidades >= unidades:
                    total_peso = producto.peso * unidades
                    total_altura = producto.altura * unidades
                    total_anchura = producto.anchura * unidades

                    self.peso_utilizado -= total_peso
                    self.altura_utilizada -= total_altura
                    self.anchura_utilizada -= total_anchura
                    producto.unidades -= unidades
                    if producto.unidades == 0:
                        self.productos.remove(producto)
                    return True
                else:
                    print(f"No hay suficientes unidades de {nombre_producto} en el almacén.")
        return False

    def peso_disponible(self):
        return self.capacidad_peso - self.peso_utilizado

    def altura_disponible(self):
        return self.capacidad_altura - self.altura_utilizada

    def anchura_disponible(self):
        return self.capacidad_anchura - self.anchura_utilizada

    def __str__(self):
        return (f"{self.nombre} (Categoría: {self.categoria}, "
                f"Capacidad de Peso: {self.capacidad_peso} kg, Utilizado: {self.peso_utilizado} kg, Disponible: {self.peso_disponible()} kg, "
                f"Capacidad de Altura: {self.capacidad_altura} m, Utilizado: {self.altura_utilizada} m, Disponible: {self.altura_disponible()} m, "
                f"Capacidad de Anchura: {self.capacidad_anchura} m, Utilizado: {self.anchura_utilizada} m, Disponible: {self.anchura_disponible()} m)")

    def mostrar_productos(self):
        for producto in self.productos:
            print(producto)

    def buscar_producto(self, nombre_producto):
        for producto in self.productos:
            if producto.nombre == nombre_producto:
                return producto
        return None

class NodoArbol:
    def __init__(self, almacen):
        self.almacen = almacen
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, almacen):
        if self.raiz is None:
            self.raiz = NodoArbol(almacen)
        else:
            self._insertar(self.raiz, almacen)

    def _insertar(self, nodo, almacen):
        if almacen.nombre < nodo.almacen.nombre:
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbol(almacen)
            else:
                self._insertar(nodo.izquierda, almacen)
        else:
            if nodo.derecha is None:
                nodo.derecha = NodoArbol(almacen)
            else:
                self._insertar(nodo.derecha, almacen)

    def encontrar_almacen(self, categoria, peso, altura, anchura):
        return self._encontrar_almacen(self.raiz, categoria, peso, altura, anchura)

    def _encontrar_almacen(self, nodo, categoria, peso, altura, anchura):
        if nodo is None:
            return None

        mejor_ajuste = None

        if (nodo.almacen.categoria == categoria and 
            nodo.almacen.peso_disponible() >= peso and
            nodo.almacen.altura_disponible() >= altura and
            nodo.almacen.anchura_disponible() >= anchura):
            mejor_ajuste = nodo.almacen

        ajuste_izquierda = self._encontrar_almacen(nodo.izquierda, categoria, peso, altura, anchura)
        ajuste_derecha = self._encontrar_almacen(nodo.derecha, categoria, peso, altura, anchura)

        if ajuste_izquierda and (mejor_ajuste is None or ajuste_izquierda.peso_disponible() > mejor_ajuste.peso_disponible()):
            mejor_ajuste = ajuste_izquierda

        if ajuste_derecha and (mejor_ajuste is None or ajuste_derecha.peso_disponible() > mejor_ajuste.peso_disponible()):
            mejor_ajuste = ajuste_derecha

        return mejor_ajuste

    def mostrar_todos_almacenes(self):
        almacenes = []
        self._recorrido_inorden(self.raiz, almacenes)
        for almacen in almacenes:
            print(almacen)

    def _recorrido_inorden(self, nodo, almacenes):
        if nodo is not None:
            self._recorrido_inorden(nodo.izquierda, almacenes)
            almacenes.append(nodo.almacen)
            self._recorrido_inorden(nodo.derecha, almacenes)

    def mostrar_productos_en_almacen(self, nombre_almacen):
        almacen = self._encontrar_almacen_por_nombre(self.raiz, nombre_almacen)
        if almacen:
            almacen.mostrar_productos()
        else:
            print(f"No se encontró el almacén con nombre {nombre_almacen}")

    def _encontrar_almacen_por_nombre(self, nodo, nombre_almacen):
        if nodo is None:
            return None
        if nodo.almacen.nombre == nombre_almacen:
            return nodo.almacen
        elif nombre_almacen < nodo.almacen.nombre:
            return self._encontrar_almacen_por_nombre(nodo.izquierda, nombre_almacen)
        else:
            return self._encontrar_almacen_por_nombre(nodo.derecha, nombre_almacen)

    def eliminar_almacen(self, nombre_almacen):
        self.raiz = self._eliminar_almacen(self.raiz, nombre_almacen)

    def _eliminar_almacen(self, nodo, nombre_almacen):
        if nodo is None:
            return nodo

        if nombre_almacen < nodo.almacen.nombre:
            nodo.izquierda = self._eliminar_almacen(nodo.izquierda, nombre_almacen)
        elif nombre_almacen > nodo.almacen.nombre:
            nodo.derecha = self._eliminar_almacen(nodo.derecha, nombre_almacen)
        else:
            if nodo.izquierda is None:
                temp = nodo.derecha
                nodo = None
                return temp
            elif nodo.derecha is None:
                temp = nodo.izquierda
                nodo = None
                return temp

            temp = self._min_value_node(nodo.derecha)
            nodo.almacen = temp.almacen
            nodo.derecha = self._eliminar_almacen(nodo.derecha, temp.almacen.nombre)
        return nodo

    def _min_value_node(self, nodo):
        current = nodo
        while current.izquierda is not None:
            current = current.izquierda
        return current

    def buscar_producto(self, nombre_producto):
        resultados = []
        self._buscar_producto(self.raiz, nombre_producto, resultados)
        return resultados

    def _buscar_producto(self, nodo, nombre_producto, resultados):
        if nodo is not None:
            self._buscar_producto(nodo.izquierda, nombre_producto, resultados)
            producto = nodo.almacen.buscar_producto(nombre_producto)
            if producto:
                resultados.append((nodo.almacen.nombre, producto))
            self._buscar_producto(nodo.derecha, nombre_producto, resultados)

class GestorAlmacen:
    def __init__(self):
        self.arbol = ArbolBinario()
        self.registro_movimientos = []
        self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists("almacenes.pkl"):
            with open("almacenes.pkl", "rb") as f:
                self.arbol = pickle.load(f)
        if os.path.exists("movimientos.pkl"):
            with open("movimientos.pkl", "rb") as f:
                self.registro_movimientos = pickle.load(f)

    def guardar_datos(self):
        with open("almacenes.pkl", "wb") as f:
            pickle.dump(self.arbol, f)
        with open("movimientos.pkl", "wb") as f:
            pickle.dump(self.registro_movimientos, f)

    def registrar_movimiento(self, tipo, producto, almacen, unidades):
        registro = {
            "tipo": tipo,
            "producto": producto.nombre,
            "unidades": unidades,
            "almacen": almacen.nombre,
            "timestamp": datetime.now()
        }
        self.registro_movimientos.append(registro)
        self.guardar_datos()

    def agregar_almacen(self):
        nombre = input("Ingrese el nombre del almacén: ")
        capacidad_peso = float(input("Ingrese la capacidad de peso del almacén (kg): "))
        capacidad_altura = float(input("Ingrese la capacidad de altura del almacén (m): "))
        capacidad_anchura = float(input("Ingrese la capacidad de anchura del almacén (m): "))
        categoria = input("Ingrese la categoría del almacén: ")

        almacen = Almacen(nombre, capacidad_peso, capacidad_altura, capacidad_anchura, categoria)
        self.arbol.insertar(almacen)
        self.guardar_datos()
        print("Almacén agregado correctamente.")

    def agregar_producto(self):
        nombre = input("Ingrese el nombre del producto: ")
        peso = float(input("Ingrese el peso del producto (kg): "))
        altura = float(input("Ingrese la altura del producto (m): "))
        anchura = float(input("Ingrese la anchura del producto (m): "))
        categoria = input("Ingrese la categoría del producto: ")
        unidades = int(input("Ingrese la cantidad de unidades del producto: "))

        producto = Producto(nombre, peso, altura, anchura, categoria, unidades)
        almacen = self.arbol.encontrar_almacen(categoria, peso * unidades, altura * unidades, anchura * unidades)
        if almacen:
            if almacen.almacenar_producto(producto):
                self.registrar_movimiento("Ingreso", producto, almacen, unidades)
                self.guardar_datos()
                print(f"Producto almacenado en el almacén {almacen.nombre}.")
            else:
                print("No hay suficiente espacio en el almacén seleccionado.")
        else:
            print("No se encontró un almacén adecuado para el producto.")

    def eliminar_almacen(self):
        nombre_almacen = input("Ingrese el nombre del almacén a eliminar: ")
        self.arbol.eliminar_almacen(nombre_almacen)
        self.guardar_datos()
        print("Almacén eliminado correctamente.")

    def eliminar_producto(self):
        nombre_almacen = input("Ingrese el nombre del almacén: ")
        nombre_producto = input("Ingrese el nombre del producto a eliminar: ")
        unidades = int(input("Ingrese la cantidad de unidades a eliminar: "))

        almacen = self.arbol._encontrar_almacen_por_nombre(self.arbol.raiz, nombre_almacen)
        if almacen:
            if almacen.eliminar_producto(nombre_producto, unidades):
                producto = Producto(nombre_producto, 0, 0, 0, almacen.categoria, unidades)  # Producto ficticio para el registro
                self.registrar_movimiento("Salida", producto, almacen, unidades)
                self.guardar_datos()
                print(f"Producto {nombre_producto} eliminado del almacén {nombre_almacen}.")
            else:
                print(f"No se encontró el producto {nombre_producto} en el almacén {nombre_almacen}.")
        else:
            print(f"No se encontró el almacén con nombre {nombre_almacen}.")

    def sacar_producto(self):
        nombre_almacen = input("Ingrese el nombre del almacén: ")
        nombre_producto = input("Ingrese el nombre del producto a sacar: ")
        unidades = int(input("Ingrese la cantidad de unidades a sacar: "))

        almacen = self.arbol._encontrar_almacen_por_nombre(self.arbol.raiz, nombre_almacen)
        if almacen:
            if almacen.eliminar_producto(nombre_producto, unidades):
                producto = Producto(nombre_producto, 0, 0, 0, almacen.categoria, unidades)  # Producto ficticio para el registro
                self.registrar_movimiento("Salida", producto, almacen, unidades)
                self.guardar_datos()
                print(f"Producto {nombre_producto} sacado del almacén {nombre_almacen}.")
            else:
                print(f"No se encontró el producto {nombre_producto} en el almacén {nombre_almacen}.")
        else:
            print(f"No se encontró el almacén con nombre {nombre_almacen}.")

    def mostrar_todos_almacenes(self):
        self.arbol.mostrar_todos_almacenes()

    def mostrar_productos_en_almacen(self):
        nombre_almacen = input("Ingrese el nombre del almacén: ")
        self.arbol.mostrar_productos_en_almacen(nombre_almacen)

    def buscar_producto(self):
        nombre_producto = input("Ingrese el nombre del producto a buscar: ")
        resultados = self.arbol.buscar_producto(nombre_producto)
        if resultados:
            for nombre_almacen, producto in resultados:
                print(f"Producto encontrado en el almacén {nombre_almacen}: {producto}")
        else:
            print("No se encontró el producto en ningún almacén.")

    def registrar_movimientos(self):
        print("Registro de Movimientos:")
        for movimiento in self.registro_movimientos:
            tipo = movimiento["tipo"]
            producto = movimiento["producto"]
            unidades = movimiento["unidades"]
            almacen = movimiento["almacen"]
            timestamp = movimiento["timestamp"]
            print(f"{tipo} - Producto: {producto}, Unidades: {unidades}, Almacén: {almacen}, Fecha y Hora: {timestamp}")

def menu():
    gestor = GestorAlmacen()
    while True:
        print("\nGestión de Almacenes")
        print("1. Agregar almacén")
        print("2. Agregar producto")
        print("3. Eliminar almacén")
        print("4. Eliminar producto")
        print("5. Sacar producto del almacén")
        print("6. Mostrar todos los almacenes")
        print("7. Mostrar productos en un almacén")
        print("8. Buscar producto por nombre")
        print("9. Mostrar registro de movimientos")
        print("10. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestor.agregar_almacen()
        elif opcion == "2":
            gestor.agregar_producto()
        elif opcion == "3":
            gestor.eliminar_almacen()
        elif opcion == "4":
            gestor.eliminar_producto()
        elif opcion == "5":
            gestor.sacar_producto()
        elif opcion == "6":
            gestor.mostrar_todos_almacenes()
        elif opcion == "7":
            gestor.mostrar_productos_en_almacen()
        elif opcion == "8":
            gestor.buscar_producto()
        elif opcion == "9":
            gestor.registrar_movimientos()
        elif opcion == "10":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
