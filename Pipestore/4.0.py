import tkinter as tk
from tkinter import ttk, messagebox
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
        return "\n".join(str(producto) for producto in self.productos)

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
        return "\n".join(str(almacen) for almacen in almacenes)

    def _recorrido_inorden(self, nodo, almacenes):
        if nodo is not None:
            self._recorrido_inorden(nodo.izquierda, almacenes)
            almacenes.append(nodo.almacen)
            self._recorrido_inorden(nodo.derecha, almacenes)

    def mostrar_productos_en_almacen(self, nombre_almacen):
        almacen = self._encontrar_almacen_por_nombre(self.raiz, nombre_almacen)
        if almacen:
            return almacen.mostrar_productos()
        else:
            return f"No se encontró el almacén con nombre {nombre_almacen}"

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

    def agregar_almacen(self, nombre, capacidad_peso, capacidad_altura, capacidad_anchura, categoria):
        almacen = Almacen(nombre, capacidad_peso, capacidad_altura, capacidad_anchura, categoria)
        self.arbol.insertar(almacen)
        self.guardar_datos()
        return "Almacén agregado correctamente."

    def agregar_producto(self, nombre, peso, altura, anchura, categoria, unidades):
        producto = Producto(nombre, peso, altura, anchura, categoria, unidades)
        almacen = self.arbol.encontrar_almacen(categoria, peso * unidades, altura * unidades, anchura * unidades)
        if almacen:
            if almacen.almacenar_producto(producto):
                self.registrar_movimiento("Ingreso", producto, almacen, unidades)
                self.guardar_datos()
                return f"Producto almacenado en el almacén {almacen.nombre}."
            else:
                return "No hay suficiente espacio en el almacén seleccionado."
        else:
            return "No se encontró un almacén adecuado para el producto."

    def eliminar_almacen(self, nombre_almacen):
        self.arbol.eliminar_almacen(nombre_almacen)
        self.guardar_datos()
        return "Almacén eliminado correctamente."

    def eliminar_producto(self, nombre_almacen, nombre_producto, unidades):
        almacen = self.arbol._encontrar_almacen_por_nombre(self.arbol.raiz, nombre_almacen)
        if almacen:
            if almacen.eliminar_producto(nombre_producto, unidades):
                producto = Producto(nombre_producto, 0, 0, 0, almacen.categoria, unidades)  # Producto ficticio para el registro
                self.registrar_movimiento("Salida", producto, almacen, unidades)
                self.guardar_datos()
                return f"Producto {nombre_producto} eliminado del almacén {nombre_almacen}."
            else:
                return f"No se encontró el producto {nombre_producto} en el almacén {nombre_almacen}."
        else:
            return f"No se encontró el almacén con nombre {nombre_almacen}."

    def sacar_producto(self, nombre_almacen, nombre_producto, unidades):
        return self.eliminar_producto(nombre_almacen, nombre_producto, unidades)

    def mostrar_todos_almacenes(self):
        return self.arbol.mostrar_todos_almacenes()

    def mostrar_productos_en_almacen(self, nombre_almacen):
        return self.arbol.mostrar_productos_en_almacen(nombre_almacen)

    def buscar_producto(self, nombre_producto):
        resultados = self.arbol.buscar_producto(nombre_producto)
        if resultados:
            return "\n".join(f"Producto encontrado en el almacén {nombre_almacen}: {producto}" for nombre_almacen, producto in resultados)
        else:
            return "No se encontró el producto en ningún almacén."

    def registrar_movimientos(self):
        return "\n".join(f"{movimiento['tipo']} - Producto: {movimiento['producto']}, Unidades: {movimiento['unidades']}, Almacén: {movimiento['almacen']}, Fecha y Hora: {movimiento['timestamp']}" for movimiento in self.registro_movimientos)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Almacenes")
        self.root.geometry("800x600")  # Tamaño inicial de la ventana
        self.root.state('zoomed')  # Maximiza la ventana al abrir
        self.gestor = GestorAlmacen()

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)

        self.frame_almacen = ttk.Frame(notebook)
        self.frame_producto = ttk.Frame(notebook)
        self.frame_movimientos = ttk.Frame(notebook)

        notebook.add(self.frame_almacen, text="Almacenes")
        notebook.add(self.frame_producto, text="Productos")
        notebook.add(self.frame_movimientos, text="Movimientos")

        notebook.pack(expand=1, fill="both")

        self.create_almacen_widgets()
        self.create_producto_widgets()
        self.create_movimientos_widgets()

    def create_almacen_widgets(self):
        ttk.Label(self.frame_almacen, text="Nombre").grid(column=0, row=0, padx=5, pady=5)
        self.nombre_almacen = ttk.Entry(self.frame_almacen)
        self.nombre_almacen.grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(self.frame_almacen, text="Capacidad Peso (kg)").grid(column=0, row=1, padx=5, pady=5)
        self.capacidad_peso = ttk.Entry(self.frame_almacen)
        self.capacidad_peso.grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(self.frame_almacen, text="Capacidad Altura (m)").grid(column=0, row=2, padx=5, pady=5)
        self.capacidad_altura = ttk.Entry(self.frame_almacen)
        self.capacidad_altura.grid(column=1, row=2, padx=5, pady=5)

        ttk.Label(self.frame_almacen, text="Capacidad Anchura (m)").grid(column=0, row=3, padx=5, pady=5)
        self.capacidad_anchura = ttk.Entry(self.frame_almacen)
        self.capacidad_anchura.grid(column=1, row=3, padx=5, pady=5)

        ttk.Label(self.frame_almacen, text="Categoría").grid(column=0, row=4, padx=5, pady=5)
        self.categoria_almacen = ttk.Entry(self.frame_almacen)
        self.categoria_almacen.grid(column=1, row=4, padx=5, pady=5)

        self.btn_agregar_almacen = ttk.Button(self.frame_almacen, text="Agregar Almacén", command=self.agregar_almacen)
        self.btn_agregar_almacen.grid(column=0, row=5, padx=5, pady=5, columnspan=2)

        self.btn_mostrar_almacenes = ttk.Button(self.frame_almacen, text="Mostrar Todos los Almacenes", command=self.mostrar_todos_almacenes)
        self.btn_mostrar_almacenes.grid(column=0, row=6, padx=5, pady=5, columnspan=2)

        self.almacenes_text = tk.Text(self.frame_almacen, width=80, height=10)
        self.almacenes_text.grid(column=0, row=7, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame_almacen, text="Eliminar Almacén (Nombre)").grid(column=0, row=8, padx=5, pady=5)
        self.eliminar_nombre_almacen = ttk.Entry(self.frame_almacen)
        self.eliminar_nombre_almacen.grid(column=1, row=8, padx=5, pady=5)

        self.btn_eliminar_almacen = ttk.Button(self.frame_almacen, text="Eliminar Almacén", command=self.eliminar_almacen)
        self.btn_eliminar_almacen.grid(column=0, row=9, padx=5, pady=5, columnspan=2)

    def create_producto_widgets(self):
        ttk.Label(self.frame_producto, text="Nombre").grid(column=0, row=0, padx=5, pady=5)
        self.nombre_producto = ttk.Entry(self.frame_producto)
        self.nombre_producto.grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Peso (kg)").grid(column=0, row=1, padx=5, pady=5)
        self.peso_producto = ttk.Entry(self.frame_producto)
        self.peso_producto.grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Altura (m)").grid(column=0, row=2, padx=5, pady=5)
        self.altura_producto = ttk.Entry(self.frame_producto)
        self.altura_producto.grid(column=1, row=2, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Anchura (m)").grid(column=0, row=3, padx=5, pady=5)
        self.anchura_producto = ttk.Entry(self.frame_producto)
        self.anchura_producto.grid(column=1, row=3, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Categoría").grid(column=0, row=4, padx=5, pady=5)
        self.categoria_producto = ttk.Entry(self.frame_producto)
        self.categoria_producto.grid(column=1, row=4, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Unidades").grid(column=0, row=5, padx=5, pady=5)
        self.unidades_producto = ttk.Entry(self.frame_producto)
        self.unidades_producto.grid(column=1, row=5, padx=5, pady=5)

        self.btn_agregar_producto = ttk.Button(self.frame_producto, text="Agregar Producto", command=self.agregar_producto)
        self.btn_agregar_producto.grid(column=0, row=6, padx=5, pady=5, columnspan=2)

        self.btn_mostrar_productos = ttk.Button(self.frame_producto, text="Mostrar Productos en Almacén", command=self.mostrar_productos_en_almacen)
        self.btn_mostrar_productos.grid(column=0, row=7, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame_producto, text="Nombre del Almacén").grid(column=0, row=8, padx=5, pady=5)
        self.nombre_almacen_producto = ttk.Entry(self.frame_producto)
        self.nombre_almacen_producto.grid(column=1, row=8, padx=5, pady=5)

        self.productos_text = tk.Text(self.frame_producto, width=80, height=10)
        self.productos_text.grid(column=0, row=9, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame_producto, text="Eliminar Producto (Nombre del Almacén)").grid(column=0, row=10, padx=5, pady=5)
        self.eliminar_nombre_almacen_producto = ttk.Entry(self.frame_producto)
        self.eliminar_nombre_almacen_producto.grid(column=1, row=10, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Nombre del Producto").grid(column=0, row=11, padx=5, pady=5)
        self.eliminar_nombre_producto = ttk.Entry(self.frame_producto)
        self.eliminar_nombre_producto.grid(column=1, row=11, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Unidades a Eliminar").grid(column=0, row=12, padx=5, pady=5)
        self.eliminar_unidades_producto = ttk.Entry(self.frame_producto)
        self.eliminar_unidades_producto.grid(column=1, row=12, padx=5, pady=5)

        self.btn_eliminar_producto = ttk.Button(self.frame_producto, text="Eliminar Producto", command=self.eliminar_producto)
        self.btn_eliminar_producto.grid(column=0, row=13, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame_producto, text="Sacar Producto (Nombre del Almacén)").grid(column=0, row=14, padx=5, pady=5)
        self.sacar_nombre_almacen_producto = ttk.Entry(self.frame_producto)
        self.sacar_nombre_almacen_producto.grid(column=1, row=14, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Nombre del Producto").grid(column=0, row=15, padx=5, pady=5)
        self.sacar_nombre_producto = ttk.Entry(self.frame_producto)
        self.sacar_nombre_producto.grid(column=1, row=15, padx=5, pady=5)

        ttk.Label(self.frame_producto, text="Unidades a Sacar").grid(column=0, row=16, padx=5, pady=5)
        self.sacar_unidades_producto = ttk.Entry(self.frame_producto)
        self.sacar_unidades_producto.grid(column=1, row=16, padx=5, pady=5)

        self.btn_sacar_producto = ttk.Button(self.frame_producto, text="Sacar Producto", command=self.sacar_producto)
        self.btn_sacar_producto.grid(column=0, row=17, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame_producto, text="Buscar Producto (Nombre)").grid(column=0, row=18, padx=5, pady=5)
        self.buscar_nombre_producto = ttk.Entry(self.frame_producto)
        self.buscar_nombre_producto.grid(column=1, row=18, padx=5, pady=5)

        self.btn_buscar_producto = ttk.Button(self.frame_producto, text="Buscar Producto", command=self.buscar_producto)
        self.btn_buscar_producto.grid(column=0, row=19, padx=5, pady=5, columnspan=2)

        self.resultados_busqueda_text = tk.Text(self.frame_producto, width=80, height=10)
        self.resultados_busqueda_text.grid(column=0, row=20, padx=5, pady=5, columnspan=2)

    def create_movimientos_widgets(self):
        self.btn_mostrar_movimientos = ttk.Button(self.frame_movimientos, text="Mostrar Movimientos", command=self.mostrar_movimientos)
        self.btn_mostrar_movimientos.grid(column=0, row=0, padx=5, pady=5)

        self.movimientos_text = tk.Text(self.frame_movimientos, width=80, height=20)
        self.movimientos_text.grid(column=0, row=1, padx=5, pady=5)

    def agregar_almacen(self):
        nombre = self.nombre_almacen.get()
        capacidad_peso = float(self.capacidad_peso.get())
        capacidad_altura = float(self.capacidad_altura.get())
        capacidad_anchura = float(self.capacidad_anchura.get())
        categoria = self.categoria_almacen.get()

        resultado = self.gestor.agregar_almacen(nombre, capacidad_peso, capacidad_altura, capacidad_anchura, categoria)
        messagebox.showinfo("Resultado", resultado)

    def agregar_producto(self):
        nombre = self.nombre_producto.get()
        peso = float(self.peso_producto.get())
        altura = float(self.altura_producto.get())
        anchura = float(self.anchura_producto.get())
        categoria = self.categoria_producto.get()
        unidades = int(self.unidades_producto.get())

        resultado = self.gestor.agregar_producto(nombre, peso, altura, anchura, categoria, unidades)
        messagebox.showinfo("Resultado", resultado)

    def mostrar_todos_almacenes(self):
        almacenes = self.gestor.mostrar_todos_almacenes()
        self.almacenes_text.delete(1.0, tk.END)
        self.almacenes_text.insert(tk.END, almacenes)

    def mostrar_productos_en_almacen(self):
        nombre_almacen = self.nombre_almacen_producto.get()
        productos = self.gestor.mostrar_productos_en_almacen(nombre_almacen)
        self.productos_text.delete(1.0, tk.END)
        self.productos_text.insert(tk.END, productos)

    def eliminar_almacen(self):
        nombre_almacen = self.eliminar_nombre_almacen.get()
        resultado = self.gestor.eliminar_almacen(nombre_almacen)
        messagebox.showinfo("Resultado", resultado)

    def eliminar_producto(self):
        nombre_almacen = self.eliminar_nombre_almacen_producto.get()
        nombre_producto = self.eliminar_nombre_producto.get()
        unidades = int(self.eliminar_unidades_producto.get())
        resultado = self.gestor.eliminar_producto(nombre_almacen, nombre_producto, unidades)
        messagebox.showinfo("Resultado", resultado)

    def sacar_producto(self):
        nombre_almacen = self.sacar_nombre_almacen_producto.get()
        nombre_producto = self.sacar_nombre_producto.get()
        unidades = int(self.sacar_unidades_producto.get())
        resultado = self.gestor.sacar_producto(nombre_almacen, nombre_producto, unidades)
        messagebox.showinfo("Resultado", resultado)

    def buscar_producto(self):
        nombre_producto = self.buscar_nombre_producto.get()
        resultados = self.gestor.buscar_producto(nombre_producto)
        self.resultados_busqueda_text.delete(1.0, tk.END)
        self.resultados_busqueda_text.insert(tk.END, resultados)

    def mostrar_movimientos(self):
        movimientos = self.gestor.registrar_movimientos()
        self.movimientos_text.delete(1.0, tk.END)
        self.movimientos_text.insert(tk.END, movimientos)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
