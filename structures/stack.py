class Stack:
    """
    Pila LIFO (Last In, First Out).
    El último elemento que entra es el primero que sale.
    Usado para mantener historial de productos vistos.
    """
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def display(self):
        if self.is_empty():
            print("  (Historial vacío)")
        else:
            print("  (Más reciente primero)")
            for i in range(len(self.items) - 1, -1, -1):
                print(f"  {len(self.items) - i}. {self.items[i]}")
    
    def __str__(self):
        """Representación en string de la pila"""
        return f"Stack({self.size()} elementos)"


# Prueba del módulo si se ejecuta directamente
if __name__ == "__main__":
    print("=== Prueba de Pila ===\n")
    
    stack = Stack()
    
    # Apilar elementos
    print("Apilando elementos...")
    stack.push("Batman: Año Uno")
    stack.push("Superman: Red Son")
    stack.push("Spider-Man")
    
    print(f"Tamaño de la pila: {stack.size()}")
    print(f"Elemento en el tope: {stack.peek()}")
    
    # Desapilar elementos
    print("\nDesapilando elementos...")
    print(f"Desapilado: {stack.pop()}")
    print(f"Desapilado: {stack.pop()}")
    
    print(f"\nTamaño de la pila: {stack.size()}")
    print(f"Elemento en el tope: {stack.peek()}")
    
    # Mostrar pila
    print("\nContenido de la pila:")
    stack.display()