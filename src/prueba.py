from collections import deque
import os

class Proceso:
    def __init__(self, pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion):
        # Inicializa un proceso con su ID, memoria necesaria, tiempo de arribo y tiempo de irrupción.
        self.pid = pid  # ID del proceso
        self.memoria_necesaria = memoria_necesaria  # Memoria que necesita el proceso
        self.tiempo_de_arribo = tiempo_de_arribo  # Momento en el que el proceso está listo
        self.tiempo_de_irrupcion = tiempo_de_irrupcion  # Tiempo total de CPU que necesita
        self.tiempo_restante = tiempo_de_irrupcion  # Tiempo que queda para completar la ejecución

    def __str__(self):
        return (f"Proceso {self.pid} - Tiempo restante: {self.tiempo_restante}, "
                f"Tiempo de arribo: {self.tiempo_de_arribo}, Tiempo de irrupción: {self.tiempo_de_irrupcion}")


class GestorDeMemoria:
    def __init__(self):
        # Particiones fijas definidas según los requisitos.
        self.particiones = {
            'grande': 250,  # Para trabajos grandes
            'mediano': 150, # Para trabajos medianos
            'pequeño': 50   # Para trabajos pequeños
        }
        self.procesos_en_memoria = []  # Lista para mantener los procesos asignados

    def asignar_memoria(self, proceso):
        # Verifica si hay espacio suficiente según Worst-Fit
        mejor_bloque = None
        mejor_bloque_index = -1

        # Busca la partición más grande que pueda albergar el proceso
        for i, (nombre, bloque) in enumerate(self.particiones.items()):
            if bloque >= proceso.memoria_necesaria:
                if mejor_bloque is None or bloque > mejor_bloque:
                    mejor_bloque = bloque
                    mejor_bloque_index = i


        # Asigna el bloque encontrado si es válido
        
        if proceso.memoria_necesaria <= 250:
            if mejor_bloque_index != -1:
                self.particiones[list(self.particiones.keys())[mejor_bloque_index]] -= proceso.memoria_necesaria
                self.procesos_en_memoria.append(proceso)
                print(f"Memoria asignada a {proceso.pid}: {proceso.memoria_necesaria} unidades en bloque de tamaño {mejor_bloque}.")
                return True
            else:
                print(f"Memoria insuficiente para {proceso.pid}.")
                listo_susp.append(proceso)
                procesos.remove(proceso)
                return False

    def liberar_memoria(self, proceso):
        # Libera la memoria ocupada por el proceso
        self.procesos_en_memoria.remove(proceso)
        # Devolver la memoria al bloque correspondiente
        for nombre in self.particiones.keys():
            self.particiones[nombre] += proceso.memoria_necesaria
            print(f"Memoria liberada de {proceso.pid}: {proceso.memoria_necesaria} unidades.")
            return


class GestorDeProcesos:
    def __init__(self, quantum=3):
        self.cola_procesos = deque() #Lista de procesos Corriendo
        self.quantum = quantum

    def agregar_proceso(self, proceso):
        self.cola_procesos.append(proceso)
        print(f"Proceso {proceso.pid} agregado a la cola.")

    #!!!!
    def mover_proceso(self, proceso):
        self.cola_procesos.append(listo_susp(0))
        listo_susp.remove()

    def ejecutar_procesos(self, gestor_memoria):
        # Ejecuta los procesos en la cola usando Round-Robin
        tiempo_actual = 0  # Mantiene el tiempo total de ejecución
        while self.cola_procesos:
            proceso = self.cola_procesos.popleft()
            # Esperar hasta que el proceso llegue
            if tiempo_actual < proceso.tiempo_de_arribo:
                tiempo_actual = proceso.tiempo_de_arribo

            tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
            proceso.tiempo_restante -= tiempo_ejecucion
            tiempo_actual += tiempo_ejecucion  # Actualiza el tiempo total

            print(f"Ejecutando {proceso.pid} por {tiempo_ejecucion} unidades de tiempo. Tiempo restante: {proceso.tiempo_restante}")

            if proceso.tiempo_restante > 0:
                self.cola_procesos.append(proceso)  # Si no ha terminado, agregar de nuevo a la cola
            else:
                print(f"Proceso {proceso.pid} completado.")
                gestor_memoria.liberar_memoria(proceso)  # Liberar memoria del proceso completado
    

def cargar_procesos_manual():
    procesos = []
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
    procesos = []
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


if __name__ == "__main__":
    gestor_memoria = GestorDeMemoria()
    gestor_procesos = GestorDeProcesos(quantum=3)

    listo_susp = []
    suspendidos = []

    metodo = input("Seleccione el método de carga de procesos (1: manual/2: archivo): ").strip().lower()
    if metodo == '1':
        procesos = cargar_procesos_manual()
    elif metodo == '2':
        procesos = cargar_procesos_archivo()
    else:
        print("Método no reconocido.")
        exit()

    while len(procesos) != 0:
        for proceso in procesos:
            # Asignar memoria y agregar a la cola de procesos
            if gestor_memoria.asignar_memoria(proceso):
                gestor_procesos.agregar_proceso(proceso)
                procesos.remove(proceso) 

        gestor_procesos.ejecutar_procesos(gestor_memoria)
        #print (f" --- Procesos en listo y suspendido = {listo_susp.getattr(pid)} --- ")
    
    # Listado de elementos en lista Listos-Suspendidos
    #for proceso in listo_susp:
    #    print(proceso.pid)
