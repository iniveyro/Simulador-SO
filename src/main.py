from collections import deque
import time
import os
from rich.console import Console
from rich.table import Table

console = Console()


class Proceso:
    def __init__(self, pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion):
        self.pid = pid
        self.memoria_necesaria = memoria_necesaria
        self.tiempo_de_arribo = tiempo_de_arribo
        self.tiempo_de_irrupcion = tiempo_de_irrupcion
        self.tiempo_restante = tiempo_de_irrupcion
        self.estado = None

    def __str__(self):
        return (f"Proceso {self.pid} - Tiempo restante: {self.tiempo_restante}, "
                f"Tiempo de arribo: {self.tiempo_de_arribo}, Tiempo de irrupción: {self.tiempo_de_irrupcion}")
        
    def show(self):
        print('pid: ', self.pid)
        print('memoria necesaria: ', self.memoria_necesaria)
        print('tiempo de arribo: ', self.tiempo_de_arribo)
        print('tiempo de irrupcion: ', self.tiempo_de_irrupcion)
        
class Particion:
    def __init__(self, nombre, tamano):
        self.nombre = nombre
        self.tamano = tamano
        self.ocupada = False
        self.proceso_asignado = None
        self.frag = None
    
    def info(self):
        print(self.nombre, self.tamano)

class GestorDeMemoria:
    def __init__(self):
        self.particiones = [
            Particion('Grande', 250),
            Particion('Mediano', 150),
            Particion('Pequeño', 50)
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
            mejor_bloque.frag = mejor_bloque.tamano - proceso.memoria_necesaria
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
                proceso.estado = "Terminado"
                return

class GestorDeProcesos:
    def __init__(self, quantum=3):
        self.cola_procesos = deque()
        self.quantum = quantum

    def agregar_proceso(self, proceso):
        self.cola_procesos.append(proceso)
        proceso.estado = "Listo"
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

            #print(f"Ejecutando {proceso.pid} por {tiempo_ejecucion} unidades de tiempo. Tiempo restante: {proceso.tiempo_restante}")

            mostrar_estado(procesos, gestor_memoria)

            if proceso.tiempo_restante > 0:
                self.cola_procesos.append(proceso)
            else:
                print(f"Proceso {proceso.pid} completado.")
                print(' ')
                print('---------------------------------------------------------------------')
                print(' ')
                print(' ')
                input("Presionar Enter para analizar el siguiente proceso")

                gestor_memoria.liberar_memoria(proceso)

                # Intenta cargar un proceso de listo_susp si hay espacio en memoria
                if listo_susp:
                    proceso_susp = listo_susp.popleft()
                    if gestor_memoria.asignar_memoria(proceso_susp):
                        self.agregar_proceso(proceso_susp)
        

def cargar_procesos_archivo():
    procesos = deque()
    global sumaTA
    global sumaTR
    global num_procesos
    global listafinal
    try:
        with open((os.path.abspath('')+'/procesos.csv'), 'r') as file:
            for linea in file:
                pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion = map(int, linea.strip().split(','))
                sumaTA = sumaTA + tiempo_de_arribo
                sumaTR = sumaTR + tiempo_de_irrupcion
                num_procesos = num_procesos + 1
                procesos.append(Proceso(pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion))
                listafinal.append(Proceso(pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion))
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
            proceso.estado = "Listo/Suspendido"
            listo_susp.append(proceso)

    while lista and len(listo_susp) < 2:
        proceso = lista.popleft()
        proceso.estado = "Listo/Suspendido"
        listo_susp.append(proceso)
        
def cargar_procesos_manual():
    global sumaTA
    global sumaTR
    global num_procesos
    global listafinal
    procesos = deque()
    num_procesos = int(input("Ingrese el número de procesos (máx. 10): "))
    if num_procesos > 10:
        print("Se permiten un máximo de 10 procesos.")
        return []
    for _  in range(num_procesos):
        pid = int(input("PID del proceso: "))
        memoria_necesaria = int(input("Memoria necesaria: "))
        tiempo_de_arribo = int(input("Tiempo de arribo: "))
        sumaTA = sumaTA + tiempo_de_arribo
        tiempo_de_irrupcion = int(input("Tiempo de irrupción: "))
        sumaTR = sumaTR + tiempo_de_irrupcion
        procesos.append(Proceso(pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion))
        listafinal.append(Proceso(pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion))
    return procesos
    
def discos(memo):
    print('Particion ',memo.particiones[0].nombre, ' con ',memo.particiones[0].tamano, ' de memoria disponible')
    print('Particion ',memo.particiones[1].nombre, ' con ',memo.particiones[1].tamano, ' de memoria disponible')
    print('Particion ',memo.particiones[2].nombre, ' con ',memo.particiones[2].tamano, ' de memoria disponible')

def mostrar_estado(procesos, gestor_memoria):
    # Tabla de particiones
    tabla_particiones = Table(title="Particiones de Memoria")
    tabla_particiones.add_column("Partición")
    tabla_particiones.add_column("Tamaño")
    tabla_particiones.add_column("Ocupada")
    tabla_particiones.add_column("Frag. Interna")
    tabla_particiones.add_column("Proceso Asignado")

    for particion in gestor_memoria.particiones:
        tabla_particiones.add_row(
            particion.nombre,
            str(particion.tamano),
            "Sí" if particion.ocupada else "No",
            str(particion.frag),
            str(particion.proceso_asignado.pid if particion.proceso_asignado else "Ninguno")
        )

    # Tabla de procesos
    tabla_procesos = Table(title="Procesos en Listos y Listos/Suspendidos")
    tabla_procesos.add_column("PID")
    tabla_procesos.add_column("Memoria Necesaria")
    tabla_procesos.add_column("Tiempo Restante")
    tabla_procesos.add_column("Estado")

    for proceso in list(procesos) + list(listo_susp):
        tabla_procesos.add_row(
            str(proceso.pid),
            str(proceso.memoria_necesaria),
            str(proceso.tiempo_restante),
            str(proceso.estado)
        )

    console.clear()
    console.print(tabla_particiones)
    console.print(tabla_procesos)

def calcular_tiempos(procesos, quantum):
    """
    Calcula el tiempo de espera, retorno y respuesta promedio.
    """
    tiempo_actual = 0
    tiempo_espera_total = 0
    tiempo_retorno_total = 0
    tiempo_respuesta_total = 0
    tiempos_respuesta = {}
    
    cola = deque(procesos)

    while cola:
        proceso = cola.popleft()
        if proceso.tiempo_de_arribo > tiempo_actual:
            tiempo_actual = proceso.tiempo_de_arribo

        # Respuesta
        if proceso.pid not in tiempos_respuesta:
            tiempos_respuesta[proceso.pid] = tiempo_actual - proceso.tiempo_de_arribo

        # Ejecución
        tiempo_ejecucion = min(proceso.tiempo_restante, quantum)
        proceso.tiempo_restante -= tiempo_ejecucion
        tiempo_actual += tiempo_ejecucion

        # Si el proceso termina
        if proceso.tiempo_restante == 0:
            tiempo_espera_total += tiempo_actual - proceso.tiempo_de_arribo - proceso.tiempo_de_irrupcion
            tiempo_retorno_total += tiempo_actual - proceso.tiempo_de_arribo
        else:
            cola.append(proceso)

    # Calcula promedios
    n = len(procesos)
    tiempo_respuesta_total = sum(tiempos_respuesta.values())
    tiempos = {
        "promedio_espera": tiempo_espera_total / n,
        "promedio_retorno": tiempo_retorno_total / n,
        "promedio_respuesta": tiempo_respuesta_total / n,
    }

    return tiempos


def generar_informe(procesos, tiempos, tiempo_total_ejecucion):
    """
    Genera un informe final con el estado de cada proceso, los tiempos promedio y el rendimiento del sistema.
    """
    # Crear tabla de procesos con sus tiempos de espera y retorno
    tabla_procesos = Table(title="Informe Final de Procesos")
    tabla_procesos.add_column("PID", justify="right")
    tabla_procesos.add_column("Tiempo de Arribo", justify="right")
    tabla_procesos.add_column("Tiempo de Irrupción", justify="right")
    tabla_procesos.add_column("Tiempo de Espera", justify="right")
    tabla_procesos.add_column("Tiempo de Retorno", justify="right")
    tabla_procesos.add_column("Estado Final", justify="right")

    # Calcular los tiempos de espera y retorno para cada proceso
    for proceso in procesos:
        # Tiempo de espera: tiempo de ejecución total menos el tiempo de irrupción menos el tiempo de arribo
        tiempo_espera = proceso.tiempo_restante + proceso.tiempo_de_arribo - proceso.tiempo_de_irrupcion
        # Tiempo de retorno: tiempo de ejecución total menos el tiempo de arribo
        tiempo_retorno = proceso.tiempo_restante + proceso.tiempo_de_arribo

        # Agregar los tiempos a la tabla
        tabla_procesos.add_row(
            str(proceso.pid),
            str(proceso.tiempo_de_arribo),
            str(proceso.tiempo_de_irrupcion),
            str(tiempo_espera),
            str(tiempo_retorno),
            "Terminado" if proceso.tiempo_restante == 0 else "No completado"
        )

    # Imprimir tabla de procesos
    console.print(tabla_procesos)

    # Imprimir los tiempos promedio de espera, retorno y respuesta
    print("\nEstadísticas Globales:")
    print(f"Tiempo promedio de espera: {tiempos['promedio_espera']:.2f}")
    print(f"Tiempo promedio de retorno: {tiempos['promedio_retorno']:.2f}")
    print(f"Tiempo promedio de respuesta: {tiempos['promedio_respuesta']:.2f}")

    # Cálculo del rendimiento del sistema
    trabajos_terminados = sum(1 for proceso in procesos if proceso.tiempo_restante == 0)
    rendimiento = trabajos_terminados / tiempo_total_ejecucion if tiempo_total_ejecucion > 0 else 0

    # Imprimir el rendimiento del sistema
    print(f"\nRendimiento del sistema: {rendimiento:.2f} trabajos por unidad de tiempo.")

if __name__ == "__main__":
    sumaTEP = 0
    sumaTA = 0
    sumaTR = 0
    num_procesos = 0
    listafinal= []
    inicio = time.time()
    gestor_memoria = GestorDeMemoria()
    gestor_procesos = GestorDeProcesos(quantum=3)

    listo_susp = deque()
    
    #print(gestor_memoria.particiones[0].info())
    print(' ')
    discos(gestor_memoria)
    print(' ')
    metodo = input("Seleccione el método de carga de procesos (1: manual/2: archivo): ").strip().lower()
    print('---------------------------------------------------------------------')
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
    
    fin = time.time()
    '''
    print(' ')
    print('Lista de Procesos Totales: ')
    for i in range(num_procesos):
        
        print(listafinal[i].show())
        print('____________________')
        time.sleep(1)
    '''
     # Calcular tiempos promedio
    tiempos_promedio = calcular_tiempos(listafinal, gestor_procesos.quantum)

    # Calcular tiempo total de ejecución
    tiempo_total_ejecucion = fin - inicio

    # Generar informe final con los tiempos y rendimiento
    generar_informe(listafinal, tiempos_promedio, tiempo_total_ejecucion)