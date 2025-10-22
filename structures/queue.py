class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def display(self):
        if self.is_empty():
            print("  (Cola vacía)")
        else:
            for i, item in enumerate(self.items, 1):
                print(f"  {i}. {item}")
    
    def __str__(self):
        return f"Queue({self.size()} elementos)"

if __name__ == "__main__":
    print("=== Prueba de Cola ===\n")
    
    queue = Queue()
    
    print("Encolando elementos...")
    queue.enqueue("Pedido #1")
    queue.enqueue("Pedido #2")
    queue.enqueue("Pedido #3")
    
    print(f"Tamaño de la cola: {queue.size()}")
    print(f"Elemento al frente: {queue.front()}")
    
    print("\nDesencolando elementos...")
    print(f"Desencolado: {queue.dequeue()}")
    print(f"Desencolado: {queue.dequeue()}")
    
    print(f"\nTamaño de la cola: {queue.size()}")
    print(f"Elemento al frente: {queue.front()}")
    
    print("\nContenido de la cola:")
    queue.display()
    