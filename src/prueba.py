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

class GestorDeMemoria:
    def __init__(self):
        self.particiones = {
            'grande': 250,
            'mediano': 150,
            'pequeño': 50
        }
        self.procesos_en_memoria = []

    def asignar_memoria(self, proceso):
        mejor_bloque = None
        mejor_bloque_index = -1

        for i, (nombre, bloque) in enumerate(self.particiones.items()):
            if bloque >= proceso.memoria_necesaria:
                if mejor_bloque is None or bloque > mejor_bloque:
                    mejor_bloque = bloque
                    mejor_bloque_index = i

        if mejor_bloque_index != -1:
            self.particiones[list(self.particiones.keys())[mejor_bloque_index]] -= proceso.memoria_necesaria
            self.procesos_en_memoria.append(proceso)
            print(f"Memoria asignada a {proceso.pid}: {proceso.memoria_necesaria} unidades en bloque de tamaño {mejor_bloque}.")
            return True
        else:
            print(f"Memoria insuficiente para {proceso.pid}.")
            return False

    def liberar_memoria(self, proceso):
        self.procesos_en_memoria.remove(proceso)
        for nombre in self.particiones.keys():
            self.particiones[nombre] += proceso.memoria_necesaria
            print(f"Memoria liberada de {proceso.pid}: {proceso.memoria_necesaria} unidades.")
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

def cargar_procesos_manual():
    procesos = deque()
    num_procesos = int(input("Ingrese el número de procesos (máx. 10): "))
    if num_procesos > 10:
        print("Se permiten un máximo de 10 procesos.")
        return []
    for _ in range(num_procesos):
        pid = int(input("PID del proceso: "))
        memoria_necesaria = int(input("Memoria necesaria: "))
        tiempo_de_arribo = int(input("Tiempo de arribo: "))
        tiempo_de_irrupcion = int(input("Tiempo de irrupción: "))
        procesos.append(Proceso(pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion))
    return procesos

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
    while lista and len(gestor_memoria.procesos_en_memoria) < 3:
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

