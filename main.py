from structures.hashtable import HashTable
from structures.queue import Queue
from structures.stack import Stack
from structures.tree import Tree, TreeNode
import os, json

script_directory = os.path.dirname(os.path.abspath(__file__))


class Product:
    def __init__(self, code, name, price, stock, category):
        self.code = code
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
    
    def __str__(self):
        return f"[{self.code}] {self.name} - ${self.price} (Stock: {self.stock})"


class Order:
    def __init__(self, order_number, customer, products):
        self.order_number = order_number
        self.customer = customer
        self.products = products
    
    def __str__(self):
        return f"Pedido #{self.order_number} - Cliente: {self.customer}"


class Store:
    def __init__(self):
        # Hash table para productos (búsqueda rápida por código)
        self.products = HashTable()
        
        # Cola para procesar pedidos en orden
        self.order_queue = Queue()
        
        # Pila para historial de productos vistos (últimos 5)
        self.view_history = Stack()
        
        # Árbol para categorías jerárquicas
        self.category_tree = Tree()
        
        # Contador para números de pedido
        self.order_counter = 1
        
        # Inicializar datos
        self._initialize_data()
    
    def _initialize_data(self):
        # Crear categorías
        self.category_tree.add("Comics")
        self.category_tree.add("DC Comics", "Comics")
        self.category_tree.add("Marvel", "Comics")
        self.category_tree.add("Manga", "Comics")
        self.category_tree.add("Independientes", "Comics")
        
        # Subcategorías
        self.category_tree.add("Batman", "DC Comics")
        self.category_tree.add("Superman", "DC Comics")
        self.category_tree.add("Wonder Woman", "DC Comics")
        self.category_tree.add("Flash", "DC Comics")
        self.category_tree.add("Justice League", "DC Comics")
        
        self.category_tree.add("Spider-Man", "Marvel")
        self.category_tree.add("X-Men", "Marvel")
        self.category_tree.add("Avengers", "Marvel")
        self.category_tree.add("Iron Man", "Marvel")
        self.category_tree.add("Captain America", "Marvel")
        self.category_tree.add("Deadpool", "Marvel")
        
        self.category_tree.add("Shonen", "Manga")
        self.category_tree.add("Seinen", "Manga")
        
        self._load_products()
    
    def _load_products(self):
        possible_files = ["products.json", "1761138984441_products.json"]
        file_path = "products/products.json"
        
        for filename in possible_files:
            if os.path.exists(filename):
                file_path = "products/" + filename
                break
        
        try:
            with open("products/products.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Iterar sobre los productos y agregarlos a la HashTable
                for product_data in data['products']:
                    product = Product(
                        product_data['code'],
                        product_data['name'],
                        product_data['price'],
                        product_data['stock'],
                        product_data['category']
                    )
                    self.products.insert(product.code, product)
                print(f"✓ {len(data['products'])} productos cargados desde {file_path}")
        except Exception as e:
            print(f"Error al cargar productos: {e}")


    
    def add_product(self, code, name, price, stock, category):
        """Agrega un nuevo producto al inventario"""
        product = Product(code, name, price, stock, category)
        self.products.insert(code, product)
        print(f"✓ Producto agregado exitosamente")
    
    def search_product(self, code):
        """Busca un producto por su código único (O(1) con hash table)"""
        product = self.products.search(code)
        if product:
            self.add_to_history(product)
            print(f"\n✓ Producto encontrado:")
            print(f"  {product}")
            return product
        else:
            print(f"✗ Producto con código '{code}' no encontrado")
            return None
    
    def update_product(self, code, new_price=None, new_stock=None):
        """Actualiza información de un producto existente"""
        product = self.products.search(code)
        if product:
            if new_price is not None:
                product.price = new_price
            if new_stock is not None:
                product.stock = new_stock
            print(f"✓ Producto actualizado exitosamente")
        else:
            print(f"✗ Producto no encontrado")
    
    def delete_product(self, code):
        """Elimina un producto del inventario"""
        if self.products.delete(code):
            print(f"✓ Producto eliminado exitosamente")
        else:
            print(f"✗ Producto no encontrado")
    
    def list_products(self):
        """Muestra todos los productos del inventario"""
        products = self.products.list_all()
        if products:
            print(f"\n{'='*70}")
            print(f"TOTAL: {len(products)} productos")
            print(f"{'='*70}")
            for prod in products:
                print(f"  {prod}")
            print(f"{'='*70}")
        else:
            print("✗ No hay productos en el inventario")
    
    # PROCESAMIENTO DE PEDIDOS
    
    def create_order(self, customer, product_codes):
        """Crea un nuevo pedido y lo agrega a la cola"""
        order_products = []
        not_found = []
        
        print(f"\nBuscando productos...")
        for code in product_codes:
            print(f"  Buscando código: {code}")
            prod = self.products.search(code)
            if prod:
                order_products.append(prod)
                print(f"    ✓ Encontrado: {prod.name}")
            else:
                not_found.append(code)
                print(f"    ✗ No encontrado: {code}")
        
        if not_found:
            print(f"\n⚠ Códigos no encontrados: {', '.join(not_found)}")
        
        if order_products:
            order = Order(self.order_counter, customer, order_products)
            self.order_queue.enqueue(order)
            print(f"\n✓ Pedido #{self.order_counter} creado exitosamente")
            print(f"  Cliente: {customer}")
            print(f"  Productos: {len(order_products)}")
            self.order_counter += 1
        else:
            print("\n✗ No se pudo crear el pedido: ningún producto válido")
    
    def process_next_order(self):
        """Procesa el siguiente pedido en la cola (FIFO)"""
        order = self.order_queue.dequeue()
        if order:
            print(f"\n{'='*70}")
            print(f"PROCESANDO: {order}")
            print(f"{'='*70}")
            print(f"Productos en el pedido:")
            for prod in order.products:
                print(f"  - {prod}")
            print(f"{'='*70}")
        else:
            print("✗ No hay pedidos pendientes")
    
    def view_pending_orders(self):
        """Muestra todos los pedidos en cola"""
        print(f"\n{'='*70}")
        print(f"PEDIDOS PENDIENTES: {self.order_queue.size()}")
        print(f"{'='*70}")
        self.order_queue.display()
        print(f"{'='*70}")
    
    # HISTORIAL DE PRODUCTOS VISTOS
    
    def add_to_history(self, product):
        """Agrega un producto al historial (máximo 5)"""
        if self.view_history.size() >= 5:
            self.view_history.items.pop(0)
        self.view_history.push(product)
    
    def view_history_list(self):
        """Muestra los últimos productos vistos"""
        print(f"\n{'='*70}")
        print(f"HISTORIAL DE BÚSQUEDAS (últimos {self.view_history.size()})")
        print(f"{'='*70}")
        self.view_history.display()
        print(f"{'='*70}")
    
    # CATEGORÍAS JERÁRQUICAS
    
    def create_category(self, name, parent=None):
        """Crea una nueva categoría en el árbol"""
        self.category_tree.add(name, parent)
        print(f"✓ Categoría '{name}' creada")
    
    def show_categories(self):
        """Muestra todas las categorías en forma jerárquica"""
        print(f"\n{'='*70}")
        print(f"ESTRUCTURA DE CATEGORÍAS")
        print(f"{'='*70}")
        self.category_tree.display()
        print(f"{'='*70}")


# PROGRAMA PRINCIPAL

def main_menu():
    """Menú principal del sistema"""
    store = Store()
    
    while True:
        print("\n" + "="*50)
        print("TIENDA NADIE SE SALVA SOLO - Sistema de Gestión")
        print("="*50)
        print("[1] Buscar producto")
        print("[2] Ver catálogo completo")
        print("[3] Agregar producto")
        print("[4] Actualizar producto")
        print("[5] Eliminar producto")
        print("[6] Crear pedido")
        print("[7] Procesar pedido")
        print("[8] Ver pedidos pendientes")
        print("[9] Historial de búsquedas")
        print("[10] Ver categorías")
        print("[0] Salir")
        print("="*50)
        
        option = input("Opción: ").strip()
        
        if option == "1":
            print("\n--- BUSCAR PRODUCTO ---")
            code = input("Código: ").strip().upper()
            store.search_product(code)
            input("\nPresione Enter para continuar...")
        
        elif option == "2":
            print("\n--- CATÁLOGO DE PRODUCTOS ---")
            store.list_products()
            input("\nPresione Enter para continuar...")
        
        elif option == "3":
            print("\n--- AGREGAR PRODUCTO ---")
            code = input("Código: ").strip().upper()
            name = input("Nombre: ").strip()
            try:
                price = float(input("Precio: "))
                stock = int(input("Stock: "))
                category = input("Categoría: ").strip()
                store.add_product(code, name, price, stock, category)
            except ValueError:
                print("✗ Error: precio o stock inválido")
            input("\nPresione Enter para continuar...")
        
        elif option == "4":
            print("\n--- ACTUALIZAR PRODUCTO ---")
            code = input("Código: ").strip().upper()
            price_input = input("Nuevo precio (Enter para omitir): ").strip()
            stock_input = input("Nuevo stock (Enter para omitir): ").strip()
            try:
                new_price = float(price_input) if price_input else None
                new_stock = int(stock_input) if stock_input else None
                store.update_product(code, new_price, new_stock)
            except ValueError:
                print("✗ Error: valor inválido")
            input("\nPresione Enter para continuar...")
        
        elif option == "5":
            print("\n--- ELIMINAR PRODUCTO ---")
            code = input("Código: ").strip().upper()
            confirm = input("¿Confirmar eliminación? (S/N): ").strip().upper()
            if confirm == 'S':
                store.delete_product(code)
            else:
                print("Operación cancelada")
            input("\nPresione Enter para continuar...")
        
        elif option == "6":
            print("\n--- CREAR PEDIDO ---")
            customer = input("Cliente: ").strip()
            codes_input = input("Códigos (separados por coma): ").strip().upper()
            codes = [c.strip() for c in codes_input.split(",")]
            store.create_order(customer, codes)
            input("\nPresione Enter para continuar...")
        
        elif option == "7":
            print("\n--- PROCESAR PEDIDO ---")
            store.process_next_order()
            input("\nPresione Enter para continuar...")
        
        elif option == "8":
            print("\n--- PEDIDOS PENDIENTES ---")
            store.view_pending_orders()
            input("\nPresione Enter para continuar...")
        
        elif option == "9":
            print("\n--- HISTORIAL DE BÚSQUEDAS ---")
            store.view_history_list()
            input("\nPresione Enter para continuar...")
        
        elif option == "10":
            print("\n--- CATEGORÍAS ---")
            store.show_categories()
            input("\nPresione Enter para continuar...")
        
        elif option == "0":
            print("\n✓ Sistema cerrado")
            break
        
        else:
            print("\n✗ Opción inválida")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main_menu()