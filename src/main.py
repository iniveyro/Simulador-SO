import tkinter as tk
from tkinter import filedialog
import os
import time
from collections import deque
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from os import system

#configuración de la consola con `rich` para generar tablas y texto con formato
console = Console()

#mensaje de bienvenida con formato y colores personalizados
def mostrar_bienvenida():
    bienvenida = Panel(
        """[bold magenta]¡Bienvenido al Simulador de Procesos del equipo [violet]Lil Tux[/violet]![/bold magenta]

Para comenzar, por favor seleccione el método de carga de procesos ([bold cyan]máximo 10 procesos[/bold cyan]):

[bold white][magenta]1.[/magenta][/bold white] [cyan]Cargar procesos manualmente[/cyan]  
[bold white][magenta]2.[/magenta][/bold white] [cyan]Cargar procesos desde un archivo[/cyan]

[bold green]¡Disfruta utilizando nuestro simulador![/bold green]
""",
        title="[bold green]Simulador de Procesos[/bold green]",
        subtitle="[bold yellow]Seleccione una opción para comenzar[/bold yellow]",
        border_style="bright_magenta",
    )

    console.print(bienvenida)

class Proceso:
    def __init__(self, pid, memoria_necesaria, tiempo_de_arribo, tiempo_de_irrupcion):
        self.pid = pid
        self.memoria_necesaria = memoria_necesaria
        self.tiempo_de_arribo = tiempo_de_arribo
        self.tiempo_de_irrupcion = tiempo_de_irrupcion
        self.tiempo_restante = tiempo_de_irrupcion
        self.estado = None
        self.momento_terminacion = 0

    def __str__(self):
        return (f"Proceso {self.pid} - Tiempo restante: {self.tiempo_restante}, "
                f"Tiempo de arribo: {self.tiempo_de_arribo}, Tiempo de irrupción: {self.tiempo_de_irrupcion}")
        
    def show(self):
        print('pid: ', self.pid)
        print('memoria necesaria: ', self.memoria_necesaria)
        print('tiempo de arribo: ', self.tiempo_de_arribo)
        print('tiempo de irrupcion: ', self.tiempo_de_irrupcion)
        
class Particion:
    def __init__(self, nombre, tamano, direccion_base):
        self.nombre = nombre
        self.tamano = tamano
        self.direccion_base = direccion_base
        self.ocupada = False
        self.proceso_asignado = None
        self.frag = None
    
    def info(self):
        print(self.nombre, self.tamano)

class GestorDeMemoria:
    def __init__(self):
        self.memoria_so = 100  # 100K para SO
        self.direccion_base = self.memoria_so  # Comenzamos después del SO
        self.particiones = [
            Particion('Grande', 250, self.direccion_base),
            Particion('Mediano', 150, self.direccion_base + 250),
            Particion('Pequeño', 50, self.direccion_base + 400)
        ]

    def asignar_memoria(self, proceso):
        mejor_bloque = None
        mayor_fragmentacion = -1
        global ini
        # Busca la partición que genere la mayor fragmentación interna (Worst-Fit)
        for particion in self.particiones:
            if not particion.ocupada and particion.tamano >= proceso.memoria_necesaria:
                fragmentacion_interna = particion.tamano - proceso.memoria_necesaria
                if fragmentacion_interna > mayor_fragmentacion:
                    mejor_bloque = particion
                    mayor_fragmentacion = fragmentacion_interna

        if mejor_bloque:
            mejor_bloque.ocupada = True
            mejor_bloque.proceso_asignado = proceso
            mejor_bloque.frag = mayor_fragmentacion
            print(' ')
            print(f"Memoria asignada a {proceso.pid}: {proceso.memoria_necesaria} unidades en bloque '{mejor_bloque.nombre}' de tamaño {mejor_bloque.tamano}.")
            return True
        else:
            print(f"Memoria insuficiente para {proceso.pid}.")
            if (len(listo_susp)<2) and (ini == True):
                listo_susp.append(proceso)
                ini = False
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
        #Agrega un proceso a la cola de listos.
        self.cola_procesos.append(proceso)
        proceso.estado = "Listo"
        print(f"Proceso {proceso.pid} agregado a la cola de Listos.")
        print(' ')

    def obtener_proceso_ejecutando(self):
        # Devuelve el proceso que se está ejecutando actualmente
        if self.cola_procesos:
            return self.cola_procesos[0]  # El primer proceso en la cola es el que se está ejecutando
        return None

    def ejecutar_procesos(self, gestor_memoria, lista):
        global ini
        tiempo_actual = 0
        
        while self.cola_procesos or listo_susp or procesos:
            if self.cola_procesos:
                proceso = self.cola_procesos.popleft()
                if tiempo_actual < proceso.tiempo_de_arribo:
                    tiempo_actual = proceso.tiempo_de_arribo

                tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
                proceso.tiempo_restante -= tiempo_ejecucion
                tiempo_actual += tiempo_ejecucion

                if proceso.tiempo_restante > 0:
                    self.cola_procesos.append(proceso)
                    mostrar_estado(procesos, gestor_memoria, proceso)
                    quantums_procesados = min(3, proceso.tiempo_restante)
                    print(f"Proceso {proceso.pid} terminó de procesar {quantums_procesados} quantums. (Tiempo restante {proceso.tiempo_restante})")
                    if self.cola_procesos:  # Verificar que haya procesos en la cola
                        print(f"El siguiente proceso es --> Proceso {self.cola_procesos[0].pid}")
                    input("Presionar Enter para analizar el siguiente proceso")
                    ini = True
                    system("cls")
                    # Modificación aquí: Solo intentar mover un proceso si hay espacio en memoria
                    if listo_susp and len(self.cola_procesos) < 3:
                        proceso_susp = listo_susp[0]
                        if gestor_memoria.asignar_memoria(proceso_susp):
                            listo_susp.popleft()
                            self.agregar_proceso(proceso_susp)
                else:
                    gestor_memoria.liberar_memoria(proceso)
                    proceso_ejecutando = proceso
                    mostrar_estado(procesos, gestor_memoria, proceso_ejecutando)
                    print(f"Proceso {proceso.pid} completado.")
                    proceso.momento_terminacion = tiempo_actual
                    print(' ')
                    print('---------------------------------------------------------------------')
                    print(' ')
                    print(' ')
                    input("Presionar Enter para analizar el siguiente proceso")
                    ini = True
                    system("cls")
                    # Modificación aquí: Similar a la anterior
                    if listo_susp and len(self.cola_procesos) < 3:
                        proceso_susp = listo_susp[0]
                        if gestor_memoria.asignar_memoria(proceso_susp):
                            listo_susp.popleft()
                            self.agregar_proceso(proceso_susp)

            # Asignar nuevos procesos si hay espacio disponible
            if len(lista) > 0:
                if ((len(gestor_procesos.cola_procesos) + len(listo_susp)) <5):
                    proceso = lista.popleft()
                    proceso.estado = "Listo/Suspendido"
                    listo_susp.append(proceso)

    def llenar_particiones_vacias(self, gestor_memoria, lista):
        particiones_vacias = sum(1 for p in gestor_memoria.particiones if not p.ocupada)
        
        while particiones_vacias > 0 and (len(self.cola_procesos) + len(listo_susp) < 5):
            proceso_asignado = False
            max_listo_susp = 5 - len(self.cola_procesos)  # Dinámico basado en procesos en memoria
            
            # Primero intentamos con procesos en listo/suspendido
            if listo_susp:
                for particion in gestor_memoria.particiones:
                    if not particion.ocupada:
                        cola_temp = deque()
                        proceso_encontrado = None
                        
                        while listo_susp:
                            proceso = listo_susp.popleft()
                            if not proceso_encontrado and proceso.memoria_necesaria <= particion.tamano:
                                if gestor_memoria.asignar_memoria(proceso):
                                    proceso_encontrado = proceso
                                    proceso_asignado = True
                                    particiones_vacias -= 1
                            else:
                                cola_temp.append(proceso)
                        
                        listo_susp.extend(cola_temp)
                        
                        if proceso_encontrado:
                            self.agregar_proceso(proceso_encontrado)
                            break
            
            # Similar para la lista de procesos nuevos
            if not proceso_asignado and lista and len(self.cola_procesos) < 3:
                for particion in gestor_memoria.particiones:
                    if not particion.ocupada:
                        cola_temp = deque()
                        proceso_encontrado = None
                        
                        while lista:
                            proceso = lista.popleft()
                            if not proceso_encontrado and proceso.memoria_necesaria <= particion.tamano:
                                if gestor_memoria.asignar_memoria(proceso):
                                    proceso_encontrado = proceso
                                    proceso_asignado = True
                                    particiones_vacias -= 1
                            else:
                                # Solo agregamos a listo/susp si hay espacio
                                if len(listo_susp) < max_listo_susp:
                                    proceso.estado = "Listo/Suspendido"
                                    listo_susp.append(proceso)
                                else:
                                    lista.append(proceso)
                        
                        if proceso_encontrado:
                            self.agregar_proceso(proceso_encontrado)
                            break
            
            if not proceso_asignado:
                break

#ventana emergente con Tkinter

def seleccionar_archivo_csv():
    root = tk.Tk()
    root.attributes('-topmost', True)  # Asegura que la ventana aparezca encima
    root.withdraw()  # Oculta la ventana principal pero después de configurar topmost
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    root.destroy()  # Destruye la ventana root después de seleccionar
    return archivo

#Carga de procesos con archivo

def cargar_procesos_archivo(archivo):
    procesos = deque()
    global sumaTA
    global sumaTR
    global num_procesos
    global listafinal
    try:
        with open(archivo, 'r') as file:  # Aquí ya pasa el argumento archivo
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

#Función para asignar los procesos a los diferentes estados

def asignacionProcesos(lista):
    while lista and (len(gestor_procesos.cola_procesos) + len(listo_susp) < 5):  # Total máximo de 5
        proceso = lista.popleft()
        if len(gestor_procesos.cola_procesos) < 3:  # Máximo 3 en memoria
            if gestor_memoria.asignar_memoria(proceso):
                gestor_procesos.agregar_proceso(proceso)
            else:
                # El máximo en listo/suspendido es 5 menos los que están en memoria
                max_listo_susp = 5 - len(gestor_procesos.cola_procesos)
                if len(listo_susp) < max_listo_susp:
                    proceso.estado = "Listo/Suspendido"
                    listo_susp.append(proceso)
                else:
                    proceso.estado = "Nuevo"
                    lista.appendleft(proceso)
                    break
        else:
            # Similar al caso anterior
            max_listo_susp = 5 - len(gestor_procesos.cola_procesos)
            if len(listo_susp) < max_listo_susp:
                proceso.estado = "Listo/Suspendido"
                listo_susp.append(proceso)
            else:
                proceso.estado = "Nuevo"
                lista.appendleft(proceso)
                break

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

#Printeo por pantalla de las particiones
def discos(memo):
    print('Particion ',memo.particiones[0].nombre, ' con ',memo.particiones[0].tamano, ' de memoria disponible')
    print('Particion ',memo.particiones[1].nombre, ' con ',memo.particiones[1].tamano, ' de memoria disponible')
    print('Particion ',memo.particiones[2].nombre, ' con ',memo.particiones[2].tamano, ' de memoria disponible')

def mostrar_estado(procesos, gestor_memoria, proceso_ejecutando):
    print("\n")
    #Tabla de particiones
    tabla_particiones = Table(title="\nParticiones de Memoria (Listos)")  
    tabla_particiones.add_column("Partición")
    tabla_particiones.add_column("Dir. Base")
    tabla_particiones.add_column("Tamaño")
    tabla_particiones.add_column("Ocupada")
    tabla_particiones.add_column("Frag. Interna")
    tabla_particiones.add_column("Proceso Asignado")
    tabla_particiones.add_column("Tiempo Restante")
    tabla_particiones.add_column("Ejecutando")

    # Primero mostrar info del SO
    

    for particion in gestor_memoria.particiones:
        tabla_particiones.add_row(
            particion.nombre,
            f"{particion.direccion_base}K",
            f"{particion.tamano}K",
            "Sí" if particion.ocupada else "No",
            f"{particion.frag}K" if particion.frag is not None else "0",
            str(particion.proceso_asignado.pid if particion.proceso_asignado else "Ninguno"),
            str(particion.proceso_asignado.tiempo_restante if particion.proceso_asignado else "0"),
            "Sí" if particion.proceso_asignado and particion.proceso_asignado.pid == proceso_ejecutando.pid else "No"
        )

    #Tabla de procesos en Listo/Suspendidos
    tabla_procesos = Table(title="\nProcesos en Listos/Suspendidos")
    tabla_procesos.add_column("PID")
    tabla_procesos.add_column("Memoria Necesaria")
    tabla_procesos.add_column("Tiempo Restante")
    tabla_procesos.add_column("Estado")

    for proceso in list(listo_susp):
        tabla_procesos.add_row(
            str(proceso.pid),
            str(proceso.memoria_necesaria),
            str(proceso.tiempo_restante),
            str(proceso.estado)
        )
    
    #Tabla de procesos Nuevos
    tabla_procesosnuev = Table(title="\nProcesos Nuevos")
    tabla_procesosnuev.add_column("PID")
    tabla_procesosnuev.add_column("Memoria Necesaria")
    tabla_procesosnuev.add_column("Tiempo Restante")
    tabla_procesosnuev.add_column("Estado")

    for proceso in list(procesos):
        tabla_procesosnuev.add_row(
            str(proceso.pid),
            str(proceso.memoria_necesaria),
            str(proceso.tiempo_restante),
            str("Nuevo")
        )

    console.clear()
    console.print(tabla_particiones)
    console.print(tabla_procesos)
    console.print(tabla_procesosnuev)
    #print(f"Ejecutando proceso {proceso_ejecutando} por {tiempo_ejecucion} unidades de tiempo. Tiempo restante: {proceso.tiempo_restante}")

def calcular_tiempos(procesos, quantum):
    
    #Calcula el tiempo de espera y retorno promedio.
    tiempo_actual = 0
    tiempo_espera_total = 0
    tiempo_retorno_total = 0
    
    cola = deque(procesos)

    while cola:
        proceso = cola.popleft()
        if proceso.tiempo_de_arribo > tiempo_actual:
            tiempo_actual = proceso.tiempo_de_arribo

        #Ejecución
        tiempo_ejecucion = min(proceso.tiempo_restante, quantum)
        proceso.tiempo_restante -= tiempo_ejecucion
        tiempo_actual += tiempo_ejecucion

        #Si el proceso termina
        if proceso.tiempo_restante == 0:
            #Asignar momento de terminación al proceso
            proceso.momento_terminacion = tiempo_actual

            #Calcular tiempo de retorno (TR) para cada proceso
            tr = proceso.momento_terminacion - proceso.tiempo_de_arribo
            tiempo_retorno_total += tr

            #Calcular tiempo de espera (TE) para cada proceso
            te = tr - proceso.tiempo_de_irrupcion
            tiempo_espera_total += te
        else:
            cola.append(proceso)

    #Calcula promedios
    n = len(procesos)
    tiempos = {
        "promedio_espera": tiempo_espera_total / n,
        "promedio_retorno": tiempo_retorno_total / n,
    }

    return tiempos


def generar_informe(procesos, tiempos, tiempo_total_ejecucion):
    
    #Genera un informe final con el estado de cada proceso y los tiempos promedio.
    tabla_procesos = Table(title="\nInforme Final de Procesos")
    tabla_procesos.add_column("PID", justify="right")
    tabla_procesos.add_column("Tiempo de Arribo", justify="right")
    tabla_procesos.add_column("Tiempo de Irrupción", justify="right")
    tabla_procesos.add_column("Tiempo de Retorno", justify="right")
    tabla_procesos.add_column("Tiempo de Espera", justify="right")
    tabla_procesos.add_column("Estado Final", justify="right")

    for proceso in procesos:
        # Calcular TR (Tiempo de Retorno) y TE (Tiempo de Espera)
        tr = proceso.momento_terminacion - proceso.tiempo_de_arribo  # Esto puede ajustarse según cómo manejas el tiempo
        te = tr - proceso.tiempo_de_irrupcion
        tabla_procesos.add_row(
            str(proceso.pid),
            str(proceso.tiempo_de_arribo),
            str(proceso.tiempo_de_irrupcion),
            str(tr),
            str(te),
            "Terminado" if proceso.tiempo_restante == 0 else "No completado"
        )

    console.print(tabla_procesos)

    # Imprimir tiempos promedio
    print("\nEstadísticas Globales:")
    print(f"Tiempo promedio de espera: {tiempos['promedio_espera']:.2f} unidades de tiempo.")
    print(f"Tiempo promedio de retorno: {tiempos['promedio_retorno']:.2f} unidades de tiempo.")

    # Calcular y mostrar el rendimiento del sistema
    trabajos_terminados = len([p for p in procesos if p.tiempo_restante == 0])
    rendimiento = trabajos_terminados / tiempo_total_ejecucion
    print(f"Rendimiento del sistema: {rendimiento:.2f} trabajos por unidad de tiempo.")
    input("Presionar Enter para finalizar el programa")

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
    ini = bool
    ini = False
    mostrar_bienvenida()

    metodo = input("Ingrese su opción: ").strip().lower()
    system("cls")

    print('---------------------------------------------------------------------')

    if metodo == '1':
        procesos = cargar_procesos_manual()
    elif metodo == '2':
        archivo_seleccionado = seleccionar_archivo_csv()
        if archivo_seleccionado:  # Verifica si se seleccionó un archivo
            procesos = cargar_procesos_archivo(archivo_seleccionado)
            if not procesos:  # Verifica si se cargaron procesos
                print("No se pudieron cargar procesos del archivo.")
                exit()
        else:
            print("No se seleccionó ningún archivo.")
            exit()
    else:
        print("Método no reconocido.")
        exit()


    while len(procesos) != 0 or len(gestor_procesos.cola_procesos) != 0 or len(listo_susp) != 0:
        asignacionProcesos(procesos)
        gestor_procesos.ejecutar_procesos(gestor_memoria, procesos)
        proceso_ejecutando = gestor_procesos.obtener_proceso_ejecutando()
    
    fin = time.time()
    print(' ')
    print('Lista de Procesos Totales: ')
    # Calcular tiempos promedio
    tiempos_promedio = calcular_tiempos(listafinal, gestor_procesos.quantum)

    # Calcular tiempo total de ejecución
    tiempo_total_ejecucion = fin - inicio

    # Generar informe final con los tiempos y rendimiento
    generar_informe(listafinal, tiempos_promedio, tiempo_total_ejecucion)