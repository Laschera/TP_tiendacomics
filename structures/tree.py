#Basado en: https://www.w3schools.com/dsa/dsa_data_trees.php

class TreeNode:
    """
    Nodo de un árbol que puede tener múltiples hijos.
    Cada nodo representa una categoría.
    """
    
    def __init__(self, name):
        """Inicializa un nodo con un nombre y lista de hijos vacía"""
        self.name = name
        self.children = []
    
    def add_child(self, child_node):
        """Agrega un nodo hijo a este nodo"""
        self.children.append(child_node)
    
    def __str__(self):
        """Representación en string del nodo"""
        return self.name


class Tree:
    """
    Árbol N-ario para representar categorías jerárquicas.
    Permite múltiples hijos por nodo (no es binario).
    """
    
    def __init__(self):
        """Inicializa un árbol vacío"""
        self.root = None
        self.nodes = {}  # Diccionario para búsqueda rápida de nodos
    
    def add(self, name, parent=None):
        """
        Agrega un nuevo nodo al árbol.
        Si parent es None, se crea como raíz.
        Si parent existe, se agrega como hijo de ese nodo.
        """
        new_node = TreeNode(name)
        self.nodes[name] = new_node
        
        if parent is None:
            # Es la raíz del árbol
            if self.root is None:
                self.root = new_node
            else:
                # Si ya hay raíz, agregarlo como hijo de la raíz
                self.root.add_child(new_node)
        else:
            # Buscar el nodo padre y agregar como hijo
            if parent in self.nodes:
                parent_node = self.nodes[parent]
                parent_node.add_child(new_node)
            else:
                print(f"Error: Categoría padre '{parent}' no existe")
    
    def search(self, name):
        """Busca un nodo por su nombre"""
        return self.nodes.get(name)
    
    def display(self, node=None, level=0):
        """
        Muestra el árbol de forma jerárquica (recursivo).
        Usa indentación para mostrar los niveles.
        """
        if node is None:
            if self.root is None:
                print("  (Árbol vacío)")
                return
            node = self.root
        
        # Imprimir el nodo actual con indentación
        indentation = "  " * level
        print(f"{indentation}├─ {node.name}")
        
        # Mostrar recursivamente todos los hijos
        for child in node.children:
            self.display(child, level + 1)
    
    def list_subcategories(self, category_name):
        """
        Lista todas las subcategorías de una categoría dada.
        Útil para buscar todos los productos de una categoría y sus hijas.
        """
        node = self.search(category_name)
        if node is None:
            return []
        
        subcategories = [node.name]
        self._collect_children(node, subcategories)
        return subcategories
    
    def _collect_children(self, node, list_result):
        """Método auxiliar recursivo para recolectar todos los hijos"""
        for child in node.children:
            list_result.append(child.name)
            self._collect_children(child, list_result)
    
    def __str__(self):
        """Representación en string del árbol"""
        return f"Tree({len(self.nodes)} categorías)"


# Prueba del módulo si se ejecuta directamente
if __name__ == "__main__":
    print("=== Prueba de Árbol ===\n")
    
    tree = Tree()
    
    # Crear estructura de categorías
    tree.add("Cómics")
    tree.add("DC Comics", "Cómics")
    tree.add("Marvel", "Cómics")
    tree.add("Batman", "DC Comics")
    tree.add("Superman", "DC Comics")
    tree.add("Spider-Man", "Marvel")
    tree.add("X-Men", "Marvel")
    
    # Mostrar árbol
    print("Estructura del árbol:")
    tree.display()
    
    # Listar subcategorías
    print("\nSubcategorías de 'DC Comics':")
    print(tree.list_subcategories("DC Comics"))
    
    print("\nSubcategorías de 'Cómics':")
    print(tree.list_subcategories("Cómics"))