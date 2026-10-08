class Miembro:
    def __init__(self, dni: str, nombre: str):
        self.setDni(dni)
        self.__nombre = nombre
        self.libros_prestados = []

    def agregarLibroPrestado(self, libro):
        self.libros_prestados.append(libro)

    def quitarLibroPrestado(self, libro):
        if libro in self.libros_prestados:
            self.libros_prestados.remove(libro)

    def getDni(self):
        return self.__dni

    def setDni(self, dni):
        if dni.isdigit() and len(dni) >= 6:
            self.__dni = dni
        else:
            print("Error: el DNI debe contener solamente números y tener al menos 6 dígitos.")
            self.__dni = ""

    def getNombre(self):
        return self.__nombre


class Libro:
    def __init__(self, titulo: str, autor: str, isbn: str, ejemplar: int):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ejemplar = ejemplar
        self.prestado_a = []

    def prestar_libro(self, miembro: Miembro):
        if self.estaDisponible():
            self.prestado_a.append(miembro)
            return True
        return False

    def estaDisponible(self):
        return len(self.prestado_a) < self.ejemplar

    def devolver_libro(self, miembro):
        if miembro in self.prestado_a:
            self.prestado_a.remove(miembro)
            return True
        return False


class Biblioteca:
    def __init__(self):
        self.libros = []
        self.miembros = []

    def agregarLibro(self):
        titulo = input("Ingrese el título del libro: ")
        autor = input("Ingrese el autor del libro: ")
        isbn = input("Ingrese el ISBN del libro: ")

        if not isbn.isdigit():
            print("Error: el ISBN debe contener solamente números.")
            return

        cantidad = self._leer_entero_positivo("¿Cuántos ejemplares desea agregar?: ")
        if cantidad is None:
            return

        libro = self.getLibro(isbn)
        if libro:
            libro.ejemplar += cantidad
            print("Ejemplares agregados correctamente.")
        else:
            nuevo_libro = Libro(titulo, autor, isbn, cantidad)
            self.libros.append(nuevo_libro)
            print("Libro agregado correctamente.")

    def getLibro(self, isbn):
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None

    def getMiembro(self, dni):
        for miembro in self.miembros:
            if miembro.getDni() == dni:
                return miembro
        return None

    def quitarLibro(self):
        isbn = input("Ingrese el ISBN del libro a quitar: ")
        libro = self.getLibro(isbn)

        if not libro:
            print("Error: el libro no existe.")
            return

        disponibles = libro.ejemplar - len(libro.prestado_a)
        ejemplares_a_quitar = self._leer_entero_positivo(
            f"¿Cuántos ejemplares desea quitar? (Disponibles: {disponibles}): "
        )
        
        if ejemplares_a_quitar is None:
            return

        if ejemplares_a_quitar > disponibles:
            print("Error: no puede quitar tantos ejemplares porque están prestados.")
            return

        if ejemplares_a_quitar == libro.ejemplar:
            self.libros.remove(libro)
            print("Libro eliminado completamente de la biblioteca.")
        else:
            libro.ejemplar -= ejemplares_a_quitar
            print(f"Ejemplares eliminados correctamente. Quedan {libro.ejemplar} en total.")

    def agregarMiembro(self):
        nombre = input("Ingrese el nombre del socio: ")
        dni = input("Ingrese el DNI del socio: ")

        if not dni.isdigit() or len(dni) < 6:
            print("Error: el DNI debe contener solamente números y al menos 6 dígitos.")
            return

        if self.getMiembro(dni):
            print("Error: ya existe un miembro con ese DNI.")
            return

        miembro = Miembro(dni, nombre)
        self.miembros.append(miembro)
        print("Miembro agregado correctamente.")

    def quitarMiembro(self):
        dni = input("Ingrese el DNI de la persona a borrar: ")
        miembro = self.getMiembro(dni)

        if not miembro:
            print("Error: el miembro no existe.")
            return

        if miembro.libros_prestados:
            print("Error: no se puede borrar un miembro que tiene libros pendientes de devolución.")
            return

        self.miembros.remove(miembro)
        print("Miembro eliminado correctamente.")

    def prestar_libro(self):
        dni = input("Ingrese el DNI del socio: ")
        isbn = input("Ingrese el ISBN del libro: ")

        if not dni.isdigit() or not isbn.isdigit():
            print("Error: el DNI y el ISBN deben ser numéricos.")
            return

        libro = self.getLibro(isbn)
        miembro = self.getMiembro(dni)

        if not libro:
            print("Error: el libro no existe.")
            return
        if not miembro:
            print("Error: el miembro no existe.")
            return

        if libro.prestar_libro(miembro):
            miembro.agregarLibroPrestado(libro)
            print("¡Libro prestado correctamente!")
        else:
            print("Error: no hay ejemplares disponibles de este libro.")

    def devolver_libro(self):
        dni = input("Ingrese el DNI del socio: ")
        isbn = input("Ingrese el ISBN del libro: ")

        if not dni.isdigit() or not isbn.isdigit():
            print("Error: el DNI y el ISBN deben ser numéricos.")
            return

        libro = self.getLibro(isbn)
        miembro = self.getMiembro(dni)

        if not libro or not miembro:
            print("Error: libro o miembro no encontrados.")
            return

        if libro.devolver_libro(miembro):
            miembro.quitarLibroPrestado(libro)
            print("¡Libro devuelto correctamente!")
        else:
            print("Error: este miembro no tiene registrado este libro como prestado.")

    def mostrarLibros(self):
        if not self.libros:
            print("No hay libros registrados.")
            return

        print("\n----- CATÁLOGO DE LIBROS -----")
        for libro in self.libros:
            disponibles = libro.ejemplar - len(libro.prestado_a)
            print(f"\nTítulo: {libro.titulo} | Autor: {libro.autor}")
            print(f"ISBN: {libro.isbn} | Total: {libro.ejemplar} | Disponibles: {disponibles}")
            
            if libro.prestado_a:
                print("Prestado a:")
                for m in libro.prestado_a:
                    print(f"  - {m.getNombre()} (DNI: {m.getDni()})")

    def mostrarMiembros(self):
        if not self.miembros:
            print("No hay miembros registrados.")
            return

        print("\n----- LISTADO DE MIEMBROS -----")
        for miembro in self.miembros:
            print(f"\nNombre: {miembro.getNombre()} | DNI: {miembro.getDni()}")
            if miembro.libros_prestados:
                print("Libros prestados:")
                for libro in miembro.libros_prestados:
                    print(f"  - {libro.titulo} (ISBN: {libro.isbn})")
            else:
                print("Libros prestados: Ninguno")

    def mostrarLibrosPrestadosAMiembro(self):
        dni = input("Ingrese el DNI del miembro: ")
        if not dni.isdigit():
            print("Error: el DNI debe contener solamente números.")
            return

        miembro = self.getMiembro(dni)
        if not miembro:
            print("Error: el miembro no existe.")
            return

        print(f"\n----- PRÉSTAMOS DE {miembro.getNombre().upper()} -----")
        if not miembro.libros_prestados:
            print("Este miembro no tiene libros prestados actualmente.")
        else:
            for libro in miembro.libros_prestados:
                print(f"- {libro.titulo} | ISBN: {libro.isbn}")

    def _leer_entero_positivo(self, mensaje):
        """Método auxiliar interno para evitar repetir validaciones de números enteros."""
        valor = input(mensaje)
        if not valor.isdigit():
            print("Error: debe ingresar un número entero válido.")
            return None
        numero = int(valor)
        if numero <= 0:
            print("Error: el valor debe ser mayor a 0.")
            return None
        return numero


def menu():
    print("\n=== Sistema de Gestión de Biblioteca ===")
    print("1. Agregar Libro")
    print("2. Quitar Libro")
    print("3. Agregar Miembro")
    print("4. Borrar Miembro")
    print("5. Prestar Libro")
    print("6. Devolver Libro")
    print("7. Mostrar Libros")
    print("8. Mostrar Miembros")
    print("9. Mostrar Libros Prestados a Miembro")
    print("10. Salir")
    return input("Seleccione una opción: ")


def main():
    biblioteca = Biblioteca()

    while True:
        opcion = menu()

        if opcion == "10":
            print("¡Hasta luego!")
            break
        elif opcion == "1":
            biblioteca.agregarLibro()
        elif opcion == "2":
            biblioteca.quitarLibro()
        elif opcion == "3":
            biblioteca.agregarMiembro()
        elif opcion == "4":
            biblioteca.quitarMiembro()
        elif opcion == "5":
            biblioteca.prestar_libro()
        elif opcion == "6":
            biblioteca.devolver_libro()
        elif opcion == "7":
            biblioteca.mostrarLibros()
        elif opcion == "8":
            biblioteca.mostrarMiembros()
        elif opcion == "9":
            biblioteca.mostrarLibrosPrestadosAMiembro()
        else:
            print("Error: opción no válida. Intente del 1 al 10.")


if __name__ == "__main__":
    main()