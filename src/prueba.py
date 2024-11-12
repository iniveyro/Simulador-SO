from collections import deque
import os

class Proceso:
    def __init__(self, pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion):
        self.pid = pid
        self.memoria_necesaria = memoria_necesaria
        self.tiempo_de_arribo = tiempo_de_arribo
        self.tiempo_de_irrupcion = tiempo_de_irrupcion
        self.tiempo_restante = tiempo_de_irrupcion

    def __str__(self):
        return (f"Proceso {self.pid} - Tiempo restante: {self.tiempo_restante}, "
                f"Tiempo de arribo: {self.tiempo_de_arribo}, Tiempo de irrupción: {self.tiempo_de_irrupcion}")

class Particion:
    def __init__(self, nombre, tamano):
        self.nombre = nombre
        self.tamano = tamano
        self.ocupada = False
        self.proceso_asignado = None

class GestorDeMemoria:
    def __init__(self):
        self.particiones = [
            Particion('grande', 250),
            Particion('mediano', 150),
            Particion('pequeño', 50)
        ]

    def asignar_memoria(self, proceso):
        mejor_bloque = None

        # Busca la partición más grande (Worst-Fit) que pueda albergar el proceso y que esté libre
        for particion in self.particiones:
            if not particion.ocupada and particion.tamano >= proceso.memoria_necesaria:
                if mejor_bloque is None or particion.tamano > mejor_bloque.tamano:
                    mejor_bloque = particion

        if mejor_bloque:
            mejor_bloque.ocupada = True
            mejor_bloque.proceso_asignado = proceso
            print(f"Memoria asignada a {proceso.pid}: {proceso.memoria_necesaria} unidades en bloque '{mejor_bloque.nombre}' de tamaño {mejor_bloque.tamano}.")
            return True
        else:
            print(f"Memoria insuficiente para {proceso.pid}.")
            return False

    def liberar_memoria(self, proceso):
        for particion in self.particiones:
            if particion.proceso_asignado == proceso:
                particion.ocupada = False
                particion.proceso_asignado = None
                print(f"Memoria liberada de {proceso.pid}: {proceso.memoria_necesaria} unidades en bloque '{particion.nombre}'.")
                return

class GestorDeProcesos:
    def __init__(self, quantum=3):
        self.cola_procesos = deque()
        self.quantum = quantum

    def agregar_proceso(self, proceso):
        self.cola_procesos.append(proceso)
        print(f"Proceso {proceso.pid} agregado a la cola.")

    def ejecutar_procesos(self, gestor_memoria):
        tiempo_actual = 0
        while self.cola_procesos:
            proceso = self.cola_procesos.popleft()
            if tiempo_actual < proceso.tiempo_de_arribo:
                tiempo_actual = proceso.tiempo_de_arribo

            tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
            proceso.tiempo_restante -= tiempo_ejecucion
            tiempo_actual += tiempo_ejecucion

            print(f"Ejecutando {proceso.pid} por {tiempo_ejecucion} unidades de tiempo. Tiempo restante: {proceso.tiempo_restante}")

            if proceso.tiempo_restante > 0:
                self.cola_procesos.append(proceso)
            else:
                print(f"Proceso {proceso.pid} completado.")
                gestor_memoria.liberar_memoria(proceso)

                # Intenta cargar un proceso de listo_susp si hay espacio en memoria
                if listo_susp:
                    proceso_susp = listo_susp.popleft()
                    if gestor_memoria.asignar_memoria(proceso_susp):
                        self.agregar_proceso(proceso_susp)

def cargar_procesos_archivo():
    procesos = deque()
    try:
        with open((os.path.abspath('')+'/procesos.csv'), 'r') as file:
            for linea in file:
                pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion = map(int, linea.strip().split(','))
                procesos.append(Proceso(pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion))
    except FileNotFoundError:
        print("El archivo no se encontró. Asegúrate de ingresar la ruta correcta.")
    except PermissionError:
        print("Permiso denegado. Asegúrate de que el archivo no esté en uso o que tengas permiso para acceder.")
    return procesos

def asignacionProcesos(lista):
    while lista and len(gestor_memoria.particiones) > len([p for p in gestor_memoria.particiones if p.ocupada]):
        proceso = lista.popleft()
        if gestor_memoria.asignar_memoria(proceso):
            gestor_procesos.agregar_proceso(proceso)
        else:
            listo_susp.append(proceso)

    while lista and len(listo_susp) < 2:
        listo_susp.append(lista.popleft())

if __name__ == "__main__":
    gestor_memoria = GestorDeMemoria()
    gestor_procesos = GestorDeProcesos(quantum=3)

    listo_susp = deque()

    metodo = input("Seleccione el método de carga de procesos (1: manual/2: archivo): ").strip().lower()
    if metodo == '1':
        procesos = cargar_procesos_manual()
    elif metodo == '2':
        procesos = cargar_procesos_archivo()
    else:
        print("Método no reconocido.")
        exit()

    while len(procesos) != 0:
        asignacionProcesos(procesos)
        gestor_procesos.ejecutar_procesos(gestor_memoria)
