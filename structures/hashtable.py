class HashTable:
    def __init__(self, size=100):
        """
        Inicializa la tabla hash con un tamaño fijo.
        Usa una lista de listas para manejar colisiones (chaining).
        """
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        """
        Función hash simple: suma los valores ASCII y aplica módulo.
        Esto convierte la clave en un índice válido de la tabla.
        """
        sum_val = 0
        for char in str(key):
            sum_val += ord(char)
        return sum_val % self.size
    
    def insert(self, key, value):
        """
        Inserta un par clave-valor en la tabla hash.
        Si la clave ya existe, actualiza el valor.
        """
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        
        self.table[index].append((key, value))
    
    def search(self, key):
        """
        Busca un valor por su clave.
        Retorna el valor si existe, None si no se encuentra.
        Complejidad: O(1) promedio
        """
        index = self._hash(key)
        
        for k, v in self.table[index]:
            if k == key:
                return v
        
        return None
    
    def delete(self, key):
        """
        Elimina un par clave-valor de la tabla.
        Retorna True si se eliminó, False si no existía.
        """
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        
        return False
    
    def list_all(self):
        """
        Retorna una lista con todos los valores almacenados.
        Útil para mostrar el inventario completo.
        """
        values = []
        for list_item in self.table:
            for key, value in list_item:
                values.append(value)
        return values
    
    def __str__(self):
        """Representación en string de la tabla hash"""
        return f"HashTable(elements={len(self.list_all())})"

if __name__ == "__main__":
    print("=== Prueba de Hash Table ===\n")
    
    table = HashTable()
    
    table.insert("BAT001", "Batman: Año Uno")
    table.insert("SUP001", "Superman: Red Son")
    table.insert("MAR001", "Spider-Man")
    
    print("Buscar BAT001:", table.search("BAT001"))
    print("Buscar SUP001:", table.search("SUP001"))
    print("Buscar XXX999:", table.search("XXX999"))
    
    print("\nEliminar SUP001:", table.delete("SUP001"))
    print("Buscar SUP001 después de eliminar:", table.search("SUP001"))
    
    print("\nTodos los elementos:", table.list_all())