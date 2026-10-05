from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# JERARQUÍA DE PERSONAS (Administrador, Mecánico, Propietario)

class Persona(ABC):
    """Clase base abstracta que representa a una persona en el sistema."""

    def __init__(self, cedula_id: str, nombre_completo: str, telefono: str):
        self.cedula_id = cedula_id
        self.nombre_completo = nombre_completo
        self.telefono = telefono

    def obtener_datos(self) -> str:
        """Devuelve los datos generales de la persona."""
        return f"Cédula/ID: {self.cedula_id} | Nombre: {self.nombre_completo} | Teléfono: {self.telefono}"


class Propietario(Persona):
    """Representa al dueño de un vehículo registrado en el taller."""

    def __init__(self, cedula_id: str, nombre_completo: str, telefono: str, direccion: str):
        super().__init__(cedula_id, nombre_completo, telefono)
        self.direccion = direccion

    def obtener_datos(self) -> str:
        return f"[Propietario / Dueño] {super().obtener_datos()} | Dirección: {self.direccion}"


class Mecanico(Persona):
    """Representa a un mecánico encargado de diagnosticar y reparar vehículos."""

    def __init__(self, cedula_id: str, nombre_completo: str, telefono: str, especialidad: str, codigo_empleado: str):
        super().__init__(cedula_id, nombre_completo, telefono)
        self.especialidad = especialidad
        self.codigo_empleado = codigo_empleado

    def obtener_datos(self) -> str:
        return (f"[Mecánico] {super().obtener_datos()} | Código: {self.codigo_empleado} | "
                f"Especialidad: {self.especialidad}")


class Administrador(Persona):
    """Representa al administrador del taller con nivel de acceso total."""

    def __init__(self, cedula_id: str, nombre_completo: str, telefono: str, nivel_acceso: str = "Total"):
        super().__init__(cedula_id, nombre_completo, telefono)
        self.nivel_acceso = nivel_acceso

    def obtener_datos(self) -> str:
        return f"[Administrador] {super().obtener_datos()} | Nivel de Acceso: {self.nivel_acceso}"


# JERARQUÍA DE VEHÍCULOS (Polimorfismo Dinámico)

class Vehiculo(ABC):
    """Clase padre abstracta común para automóviles y motocicletas."""

    def __init__(self, placa: str, marca: str, modelo: str, anio_fabricacion: int, propietario: Propietario,
                 color: str = "Gris", kilometraje: float = 0.0, vin_chasis: str = "SIN_VIN"):
        self.placa = placa.upper().strip()
        self.marca = marca
        self.modelo = modelo
        self.anio_fabricacion = anio_fabricacion
        self.propietario = propietario
        self.color = color
        self.kilometraje = kilometraje
        self.estado = "Registrado"  # Estados: "Registrado", "En Mantenimiento", "Listo"
        self.fecha_ingreso = "2026-10-04"
        self.vin_chasis = vin_chasis

    @abstractmethod
    def realizar_mantenimiento(self) -> str:
        """Método abstracto implementado por cada tipo de vehículo (Polimorfismo)."""
        pass

    def obtener_informacion(self) -> str:
        """Retorna un resumen de los atributos técnicos del vehículo."""
        dueno_nom = self.propietario.nombre_completo if self.propietario else "Sin Propietario"
        return (f"Placa: {self.placa} | Marca/Mod: {self.marca} {self.modelo} ({self.anio_fabricacion}) | "
                f"Propietario: {dueno_nom} | Estado: {self.estado}")

    def set_estado(self, nuevo_estado: str) -> None:
        self.estado = nuevo_estado


class Automovil(Vehiculo):
    """Representa un automóvil de pasajeros."""

    def __init__(self, placa: str, marca: str, modelo: str, anio: int, propietario: Propietario,
                 numero_puertas: int, tipo_combustible: str, tipo_transmision: str = "Mecánica",
                 capacidad_maletero: int = 400, tiene_aire_acondicionado: bool = True):
        super().__init__(placa, marca, modelo, anio, propietario)
        self.numero_puertas = numero_puertas
        self.tipo_combustible = tipo_combustible
        self.tipo_transmision = tipo_transmision
        self.capacidad_maletero = capacidad_maletero
        self.tiene_aire_acondicionado = tiene_aire_acondicionado

    def realizar_mantenimiento(self) -> str:
        return (f"Ejecutando mantenimiento de Automóvil para [{self.placa}]:\n"
                f" - Inspección de {self.numero_puertas} puertas, inyección ({self.tipo_combustible})\n"
                f" - Revisión de transmisión {self.tipo_transmision} y sistema de aire acondicionado.")

    def obtener_informacion(self) -> str:
        return f"[Automóvil] {super().obtener_informacion()} | Puertas: {self.numero_puertas} | Combustible: {self.tipo_combustible}"


class Motocicleta(Vehiculo):
    """Representa una motocicleta."""

    def __init__(self, placa: str, marca: str, modelo: str, anio: int, propietario: Propietario,
                 cilindraje: int, tipo_freno: str, tipo_moto: str = "Urbana", tipo_arranque: str = "Eléctrico"):
        super().__init__(placa, marca, modelo, anio, propietario)
        self.cilindraje = cilindraje
        self.tipo_freno = tipo_freno
        self.tipo_moto = tipo_moto
        self.tipo_arranque = tipo_arranque

    def realizar_mantenimiento(self) -> str:
        return (f"Ejecutando mantenimiento de Motocicleta para [{self.placa}]:\n"
                f" - Calibración de motor {self.cilindraje}cc ({self.tipo_moto})\n"
                f" - Chequeo de frenos ({self.tipo_freno}), kit de arrastre y arranque {self.tipo_arranque}.")

    def obtener_informacion(self) -> str:
        return f"[Motocicleta] {super().obtener_informacion()} | Cilindraje: {self.cilindraje}cc | Frenos: {self.tipo_freno}"


# CLASE REPUESTO (Gestión de Inventario)

class Repuesto:
    """Representa un repuesto o insumo en el inventario del taller."""

    def __init__(self, codigo_repuesto: str, nombre: str, precio: float, stock: int,
                 categoria: str = "General", stock_minimo: int = 2):
        self.codigo_repuesto = codigo_repuesto.strip().upper()
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.stock_minimo = stock_minimo

    def actualizar_stock(self, cantidad: int) -> bool:
        """Actualiza el stock disponible sumando o deduciendo inventario."""
        if self.stock + cantidad < 0:
            return False
        self.stock += cantidad
        return True

    def __str__(self) -> str:
        return (f"Código: {self.codigo_repuesto} | Nombre: {self.nombre} | Precio: ${self.precio:,.2f} | "
                f"Stock: {self.stock} (Mín: {self.stock_minimo}) | Cat: {self.categoria}")


# CLASE ORDEN DE MANTENIMIENTO

class OrdenMantenimiento:
    """Representa una orden de servicio o diagnóstico asignada."""

    def __init__(self, id_orden: int, vehiculo: Vehiculo, mecanico: Mecanico, diagnostico_inicial: str):
        self.id_orden = id_orden
        self.vehiculo = vehiculo
        self.mecanico = mecanico
        self.diagnostico_inicial = diagnostico_inicial
        self.fecha_ingreso = "2026-10-04"
        self.fecha_salida = "Pendiente"
        self.costo_total = 0.0
        self.estado = "Creada"  # "Creada", "En Proceso", "Pausada", "Finalizada", "Cancelada"
        self.repuestos_asignados: Dict[Repuesto, int] = {}

    def agregar_repuesto(self, repuesto: Repuesto, cantidad: int) -> bool:
        """Asigna una cantidad de repuesto descontándolo del inventario del taller."""
        if cantidad <= 0:
            return False
        if repuesto.actualizar_stock(-cantidad):
            self.repuestos_asignados[repuesto] = self.repuestos_asignados.get(repuesto, 0) + cantidad
            self.calcular_costo_total()
            return True
        return False

    def quitar_repuesto(self, repuesto: Repuesto, cantidad: int) -> bool:
        """Quita repuestos de la orden y los reintegra al inventario."""
        if repuesto in self.repuestos_asignados:
            cant_actual = self.repuestos_asignados[repuesto]
            cant_a_quitar = min(cant_actual, cantidad)
            self.repuestos_asignados[repuesto] -= cant_a_quitar
            repuesto.actualizar_stock(cant_a_quitar)
            if self.repuestos_asignados[repuesto] == 0:
                del self.repuestos_asignados[repuesto]
            self.calcular_costo_total()
            return True
        return False

    def calcular_costo_total(self) -> float:
        """Calcula el valor acumulado de los repuestos empleados."""
        self.costo_total = sum(rep.precio * cant for rep, cant in self.repuestos_asignados.items())
        return self.costo_total

    def cambiar_estado(self, nuevo_estado: str) -> None:
        self.estado = nuevo_estado
        if nuevo_estado == "Finalizada":
            self.fecha_salida = "2026-10-05"
            if self.vehiculo:
                self.vehiculo.set_estado("Listo")

    def resumen(self) -> str:
        rep_str = ", ".join(f"{r.nombre} (x{c})" for r, c in self.repuestos_asignados.items()) or "Sin repuestos"
        placa = self.vehiculo.placa if self.vehiculo else "Vehículo Eliminado"
        mec_nom = self.mecanico.nombre_completo if self.mecanico else "Sin Mecánico"
        return (f"Orden #{self.id_orden} | Vehículo: {placa} | Mecánico: {mec_nom} | "
                f"Estado: {self.estado} | Repuestos: [{rep_str}] | Costo Total: ${self.costo_total:,.2f}")


# CONTROLADOR PRINCIPAL DEL TALLER (CRUD + SIMULADOR DE MANTENIMIENTO)

class TallerMantenimiento:
    """Gestiona el inventario, repuestos, órdenes, personal y el simulador en consola."""

    def __init__(self, nombre_taller: str = "Taller Mecánico Central"):
        self.nombre_taller = nombre_taller
        self.lista_vehiculos: List[Vehiculo] = []
        self.inventario_repuestos: List[Repuesto] = []
        self.ordenes_mantenimiento: List[OrdenMantenimiento] = []
        self.lista_personal: List[Persona] = []
        self.contador_ordenes = 1000

        # Estado del simulador
        self.estado_simulador = "Detenido"  # "En proceso", "Pausado", "Detenido"
        self.indice_cola_mantenimiento = 0

        # Cargar información inicial por defecto
        self._cargar_datos_defecto()

    def _cargar_datos_defecto(self):
        """Carga datos de ejemplo obligatorios al iniciar el programa."""
        admin = Administrador("101010", "Carlos Perez", "555-0100", "Total")
        mecanico1 = Mecanico("202020", "Juan Gomez", "555-0200", "Motores y Mecánica General", "MEC-01")
        mecanico2 = Mecanico("303030", "Luis Martinez", "555-0300", "Electricidad e Inyección", "MEC-02")
        propietario1 = Propietario("404040", "Ana Rodriguez", "555-0400", "Av. Principal 123")
        propietario2 = Propietario("505050", "Pedro Sanchez", "555-0500", "Calle 45 #12-34")

        self.lista_personal.extend([admin, mecanico1, mecanico2, propietario1, propietario2])

        auto1 = Automovil("ABC1234", "Toyota", "Corolla", 2021, propietario1, 4, "Gasolina", "Automática")
        moto1 = Motocicleta("XYZ987", "Yamaha", "MT-07", 2023, propietario2, 689, "Disco ABS", "Naked")
        self.lista_vehiculos.extend([auto1, moto1])

        r1 = Repuesto("REP-01", "Filtro de Aceite", 15.50, 20, "Filtros")
        r2 = Repuesto("REP-02", "Pastillas de Freno", 45.00, 15, "Frenos")
        r3 = Repuesto("REP-03", "Bujía Iridium", 12.00, 30, "Encendido")
        self.inventario_repuestos.extend([r1, r2, r3])

        ord1 = self.crear_orden(auto1, mecanico1, "Revisión periódica de 20,000 km")
        ord1.agregar_repuesto(r1, 1)
        ord1.agregar_repuesto(r3, 4)

        ord2 = self.crear_orden(moto1, mecanico2, "Mantenimiento del sistema de frenos y purga de líquido")
        ord2.agregar_repuesto(r2, 2)

    # --- Operaciones CRUD ---

    def registrar_vehiculo(self, v: Vehiculo) -> None:
        self.lista_vehiculos.append(v)

    def registrar_repuesto(self, r: Repuesto) -> None:
        self.inventario_repuestos.append(r)

    def registrar_mecanico(self, m: Mecanico) -> None:
        self.lista_personal.append(m)

    def registrar_propietario(self, p: Propietario) -> None:
        self.lista_personal.append(p)

    def obtener_mecanicos(self) -> List[Mecanico]:
        return [p for p in self.lista_personal if isinstance(p, Mecanico)]

    def obtener_propietarios(self) -> List[Propietario]:
        return [p for p in self.lista_personal if isinstance(p, Propietario)]

    def crear_orden(self, vehiculo: Vehiculo, mecanico: Mecanico, diagnostico: str) -> OrdenMantenimiento:
        self.contador_ordenes += 1
        orden = OrdenMantenimiento(self.contador_ordenes, vehiculo, mecanico, diagnostico)
        vehiculo.set_estado("En Mantenimiento")
        self.ordenes_mantenimiento.append(orden)
        return orden

    def eliminar_vehiculo(self, placa: str) -> bool:
        v = next((v for v in self.lista_vehiculos if v.placa == placa.upper().strip()), None)
        if not v:
            return False

        # Regla: Si se elimina el vehículo en mantenimiento activo, la simulación pasa a detenido
        orden_activa = self.get_orden_simulacion_actual()
        if orden_activa and orden_activa.vehiculo == v:
            self.estado_simulador = "Detenido"

        for orden in self.ordenes_mantenimiento:
            if orden.vehiculo == v:
                orden.vehiculo = None

        self.lista_vehiculos.remove(v)
        return True

    def eliminar_repuesto(self, codigo: str) -> bool:
        codigo = codigo.upper().strip()
        rep = next((r for r in self.inventario_repuestos if r.codigo_repuesto == codigo), None)
        if not rep:
            return False

        for orden in self.ordenes_mantenimiento:
            if rep in orden.repuestos_asignados:
                del orden.repuestos_asignados[rep]
                orden.calcular_costo_total()

        self.inventario_repuestos.remove(rep)
        return True

    # --- Simulador de Mantenimiento ---

    def get_ordenes_activas(self) -> List[OrdenMantenimiento]:
        return [o for o in self.ordenes_mantenimiento if o.estado in ["Creada", "En Proceso", "Pausada"]]

    def get_orden_simulacion_actual(self) -> Optional[OrdenMantenimiento]:
        activas = self.get_ordenes_activas()
        if not activas:
            return None
        if self.indice_cola_mantenimiento >= len(activas):
            self.indice_cola_mantenimiento = 0
        return activas[self.indice_cola_mantenimiento]

    def iniciar_simulacion(self) -> str:
        orden = self.get_orden_simulacion_actual()
        if not orden:
            return "Error: No hay órdenes activas en la cola."
        if not orden.vehiculo:
            return "Error: La orden activa no tiene un vehículo asignado."
        if not orden.repuestos_asignados:
            return "Aviso/Error: La orden no cuenta con repuestos asignados en stock."

        self.estado_simulador = "En proceso"
        orden.cambiar_estado("En Proceso")
        # Invocación polimórfica dinámica
        return f"Simulación Iniciada con Éxito:\n{orden.vehiculo.realizar_mantenimiento()}"

    def pausar_simulacion(self) -> str:
        if self.estado_simulador != "En proceso":
            return "Acción No Válida: Solo se puede pausar una simulación 'En proceso'."
        self.estado_simulador = "Pausado"
        orden = self.get_orden_simulacion_actual()
        if orden:
            orden.cambiar_estado("Pausada")
        return "Simulación PAUSADA correctamente."

    def reanudar_simulacion(self) -> str:
        if self.estado_simulador != "Pausado":
            return "Acción No Válida: Solo se puede reanudar una simulación 'Pausada'."
        self.estado_simulador = "En proceso"
        orden = self.get_orden_simulacion_actual()
        if orden:
            orden.cambiar_estado("En Proceso")
        return "Simulación REANUDADA correctamente."

    def detener_simulacion(self) -> str:
        if self.estado_simulador not in ["En proceso", "Pausado"]:
            return "Acción No Válida: Solo se puede detener una simulación 'En proceso' o 'Pausada'."
        self.estado_simulador = "Detenido"
        orden = self.get_orden_simulacion_actual()
        if orden:
            orden.cambiar_estado("Finalizada")
        return "Simulación DETENIDA. La orden de trabajo fue marcada como Finalizada."

    def siguiente_vehiculo_cola(self) -> str:
        activas = self.get_ordenes_activas()
        if not activas:
            return "No hay órdenes activas en la cola."
        self.indice_cola_mantenimiento = (self.indice_cola_mantenimiento + 1) % len(activas)
        self.estado_simulador = "Detenido"
        return f"Avanzado al siguiente vehículo en cola (Posición {self.indice_cola_mantenimiento + 1}/{len(activas)})."

    def anterior_vehiculo_cola(self) -> str:
        activas = self.get_ordenes_activas()
        if not activas:
            return "No hay órdenes activas en la cola."
        self.indice_cola_mantenimiento = (self.indice_cola_mantenimiento - 1) % len(activas)
        self.estado_simulador = "Detenido"
        return f"Retrocedido al vehículo anterior en cola (Posición {self.indice_cola_mantenimiento + 1}/{len(activas)})."

# MENÚ INTERACTIVO EN CONSOLA

def ejecutar_menu_consola():
    taller = TallerMantenimiento("Taller Mecánico Central")

    while True:
        print("\n" + "=" * 80)
        print(f"      SISTEMA DE INVENTARIO Y MANTENIMIENTO - {taller.nombre_taller.upper()}")
        print("=" * 80)

        # Mostrar contadores de inicio del sistema
        cant_vehiculos = len(taller.lista_vehiculos)
        cant_duenos = len(taller.obtener_propietarios())
        cant_mecanicos = len(taller.obtener_mecanicos())
        cant_ordenes_activas = len(taller.get_ordenes_activas())

        print(f"  [ESTADO DEL TALLER] Vehículos: {cant_vehiculos} | Dueños: {cant_duenos} | "
              f"Mecánicos: {cant_mecanicos} | Órdenes Activas: {cant_ordenes_activas}")

        # Muestra permanente del estado de la simulación
        orden_actual = taller.get_orden_simulacion_actual()
        vehiculo_str = orden_actual.vehiculo.placa if (orden_actual and orden_actual.vehiculo) else "N/A"
        print(f"  [SIMULADOR] Estado: {taller.estado_simulador.upper()} | Vehículo Activo: {vehiculo_str}")
        print("-" * 80)

        print("  1. Resumen General (Vehículos, Repuestos, Órdenes y Personal)")
        print("  2. Controles del Simulador (Iniciar / Pausar / Reanudar / Detener)")
        print("  3. Gestionar Vehículos (Ver Lista / Crear / Eliminar)")
        print("  4. Gestionar Inventario de Repuestos (Ver Stock / Agregar / Editar / Eliminar)")
        print("  5. Crear y Asignar Orden de Mantenimiento")
        print("  6. Gestionar Personal (Ver Lista / Crear Mecánico / Crear Dueño)")
        print("  7. Navegar en Cola del Simulador (Siguiente / Anterior)")
        print("  0. Salir")
        print("-" * 80)

        opcion = input(" Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n" + "=" * 50)
            print("         RESUMEN GENERAL DEL TALLER")
            print("=" * 50)
            print("\n--- VEHÍCULOS REGISTRADOS ---")
            if taller.lista_vehiculos:
                for v in taller.lista_vehiculos:
                    print(" ", v.obtener_informacion())
            else:
                print("  (Sin vehículos registrados)")

            print("\n--- INVENTARIO DE REPUESTOS ---")
            if taller.inventario_repuestos:
                for r in taller.inventario_repuestos:
                    print(" ", r)
            else:
                print("  (Sin repuestos en inventario)")

            print("\n--- ÓRDENES DE MANTENIMIENTO ---")
            if taller.ordenes_mantenimiento:
                for o in taller.ordenes_mantenimiento:
                    print(" ", o.resumen())
            else:
                print("  (Sin órdenes de mantenimiento)")

            print("\n--- PERSONAL DEL TALLER ---")
            for p in taller.lista_personal:
                print(" ", p.obtener_datos())

        elif opcion == "2":
            print("\n--- CONTROLES DEL SIMULADOR ---")
            print(" 1. Iniciar Simulación")
            print(" 2. Pausar Simulación")
            print(" 3. Reanudar Simulación")
            print(" 4. Detener / Finalizar Mantenimiento")
            sub_op = input(" Comando: ").strip()

            if sub_op == "1":
                print("\n", taller.iniciar_simulacion())
            elif sub_op == "2":
                print("\n", taller.pausar_simulacion())
            elif sub_op == "3":
                print("\n", taller.reanudar_simulacion())
            elif sub_op == "4":
                print("\n", taller.detener_simulacion())

        elif opcion == "3":
            print("\n" + "=" * 50)
            print("         GESTIÓN DE VEHÍCULOS")
            print("=" * 50)
            print(" --- VEHÍCULOS ACTUALMENTE REGISTRADOS EN EL SISTEMA ---")
            if taller.lista_vehiculos:
                for idx, v in enumerate(taller.lista_vehiculos, 1):
                    print(f"  {idx}. {v.obtener_informacion()}")
            else:
                print("  (No hay vehículos registrados actualmente)")
            print("-" * 50)

            print(" 1. Crear Automóvil")
            print(" 2. Crear Motocicleta")
            print(" 3. Eliminar Vehículo por Placa")
            print(" 0. Volver al menú principal")
            sub_op = input(" Seleccione una opción: ").strip()

            if sub_op in ["1", "2"]:
                placa = input(" Placa del vehículo: ").strip()
                marca = input(" Marca: ").strip()
                modelo = input(" Modelo: ").strip()
                try:
                    anio = int(input(" Año de fabricación: "))
                except ValueError:
                    print(" Error: El año debe ser un número entero.")
                    continue

                # Selección o creación de Propietario
                propietarios = taller.obtener_propietarios()
                prop_seleccionado = None
                if propietarios:
                    print("\n Propietarios registrados:")
                    for idx, p in enumerate(propietarios, 1):
                        print(f"  {idx}. {p.nombre_completo} (Cédula: {p.cedula_id})")
                    print("  0. Registrar un nuevo propietario ahora")
                    try:
                        sel_p = int(input(" Seleccione propietario #: "))
                        if 1 <= sel_p <= len(propietarios):
                            prop_seleccionado = propietarios[sel_p - 1]
                    except ValueError:
                        pass

                if not prop_seleccionado:
                    print("\n [Registro de Nuevo Propietario]")
                    c_id = input(" Cédula/ID: ").strip()
                    nom = input(" Nombre completo: ").strip()
                    tel = input(" Teléfono: ").strip()
                    dir_p = input(" Dirección: ").strip()
                    prop_seleccionado = Propietario(c_id, nom, tel, dir_p)
                    taller.registrar_propietario(prop_seleccionado)
                    print(f" Propietario [{nom}] registrado exitosamente.")

                if sub_op == "1":
                    try:
                        puertas = int(input(" Número de puertas [4]: ") or 4)
                    except ValueError:
                        puertas = 4
                    comb = input(" Tipo de combustible (Gasolina/Diésel/Híbrido/Eléctrico): ").strip() or "Gasolina"
                    auto = Automovil(placa, marca, modelo, anio, prop_seleccionado, puertas, comb)
                    taller.registrar_vehiculo(auto)
                    print(f" ¡Automóvil [{auto.placa}] registrado correctamente en la gestión de vehículos!")
                else:
                    try:
                        cilin = int(input(" Cilindraje (cc) [150]: ") or 150)
                    except ValueError:
                        cilin = 150
                    freno = input(" Tipo de freno (Disco/Tambor/ABS): ").strip() or "Disco"
                    moto = Motocicleta(placa, marca, modelo, anio, prop_seleccionado, cilin, freno)
                    taller.registrar_vehiculo(moto)
                    print(f" ¡Motocicleta [{moto.placa}] registrada correctamente en la gestión de vehículos!")

            elif sub_op == "3":
                placa = input(" Ingrese la placa del vehículo a eliminar: ").strip()
                if taller.eliminar_vehiculo(placa):
                    print(f" ¡Vehículo con placa [{placa.upper()}] eliminado del taller!")
                else:
                    print(" Error: No se encontró ningún vehículo registrado con esa placa.")

        elif opcion == "4":
            print("\n" + "=" * 50)
            print("     GESTIÓN DE INVENTARIO DE REPUESTOS")
            print("=" * 50)
            print(" --- ESTADO ACTUAL DEL INVENTARIO EN BODEGA ---")
            if taller.inventario_repuestos:
                for idx, r in enumerate(taller.inventario_repuestos, 1):
                    print(f"  {idx}. {r}")
            else:
                print("  (El inventario se encuentra vacío)")
            print("-" * 50)

            print(" 1. Registrar Nuevo Repuesto")
            print(" 2. Actualizar Stock (Entrada / Salida de Repuesto)")
            print(" 3. Eliminar Repuesto del Inventario")
            print(" 0. Volver al menú principal")
            sub_op = input(" Seleccione una opción: ").strip()

            if sub_op == "1":
                cod = input(" Código del repuesto (ej. REP-04): ").strip()
                nom = input(" Nombre del repuesto: ").strip()
                try:
                    precio = float(input(" Precio unitario ($): "))
                    stock = int(input(" Stock inicial: "))
                except ValueError:
                    print(" Error: El precio y el stock deben ser numéricos.")
                    continue
                cat = input(" Categoría [General]: ").strip() or "General"
                rep = Repuesto(cod, nom, precio, stock, cat)
                taller.registrar_repuesto(rep)
                print(f" ¡Repuesto [{rep.nombre}] agregado al inventario!")

            elif sub_op == "2":
                cod = input(" Código del repuesto a actualizar: ").strip()
                rep = next((r for r in taller.inventario_repuestos if r.codigo_repuesto == cod.upper()), None)
                if rep:
                    try:
                        cant = int(input(" Cantidad a agregar (positiva) o deducir (negativa): "))
                    except ValueError:
                        print(" Error: Ingrese un entero válido.")
                        continue
                    if rep.actualizar_stock(cant):
                        print(f" ¡Stock de [{rep.nombre}] actualizado con éxito! Nuevo stock: {rep.stock}")
                    else:
                        print(" Error: No hay suficiente stock disponible para realizar esa deducción.")
                else:
                    print(" Error: Repuesto no encontrado con ese código.")

            elif sub_op == "3":
                cod = input(" Código del repuesto a eliminar: ").strip()
                if taller.eliminar_repuesto(cod):
                    print(f" ¡Repuesto [{cod.upper()}] eliminado del inventario!")
                else:
                    print(" Error: No se encontró ningún repuesto con ese código.")

        elif opcion == "5":
            print("\n--- CREAR Y ASIGNAR ORDEN DE MANTENIMIENTO ---")
            if not taller.lista_vehiculos:
                print(" Error: No hay vehículos registrados. Registre uno primero.")
                continue

            mecanicos = taller.obtener_mecanicos()
            if not mecanicos:
                print(" Error: No hay mecánicos disponibles. Registre un mecánico primero.")
                continue

            print("\n Seleccione el vehículo para la orden de trabajo:")
            for i, v in enumerate(taller.lista_vehiculos, 1):
                print(f"  {i}. {v.placa} - {v.marca} {v.modelo} ({v.estado})")

            try:
                idx_v = int(input(" Número de vehículo: ")) - 1
                v_sel = taller.lista_vehiculos[idx_v]
            except (ValueError, IndexError):
                print(" Selección de vehículo no válida.")
                continue

            print("\n Seleccione el mecánico asignado:")
            for i, m in enumerate(mecanicos, 1):
                print(f"  {i}. {m.nombre_completo} (Especialidad: {m.especialidad})")

            try:
                idx_m = int(input(" Número de mecánico: ")) - 1
                m_sel = mecanicos[idx_m]
            except (ValueError, IndexError):
                print(" Selección de mecánico no válida.")
                continue

            diag = input(" Diagnóstico inicial / Trabajo a realizar: ").strip() or "Mantenimiento Preventivo"
            orden = taller.crear_orden(v_sel, m_sel, diag)
            print(f" ¡Orden #{orden.id_orden} creada con éxito para [{v_sel.placa}] asignada a [{m_sel.nombre_completo}]!")

            # Opción para asignar repuestos inmediatamente
            if taller.inventario_repuestos:
                asig = input(" ¿Desea asignar repuestos del inventario a esta orden ahora? (s/n): ").strip().lower()
                if asig == 's':
                    while True:
                        print("\n Repuestos en bodega:")
                        for r in taller.inventario_repuestos:
                            print(f"  - [{r.codigo_repuesto}] {r.nombre} (Disponible: {r.stock}, Precio: ${r.precio})")
                        cod_r = input(" Código del repuesto (o presione Enter para terminar): ").strip()
                        if not cod_r:
                            break
                        rep_obj = next((r for r in taller.inventario_repuestos if r.codigo_repuesto == cod_r.upper()), None)
                        if rep_obj:
                            try:
                                cant_r = int(input(f" Cantidad de [{rep_obj.nombre}] a usar: "))
                                if orden.agregar_repuesto(rep_obj, cant_r):
                                    print(f"  -> Asignados {cant_r} x {rep_obj.nombre}. Costo acumulado: ${orden.costo_total:,.2f}")
                                else:
                                    print("  -> Stock insuficiente o cantidad no válida.")
                            except ValueError:
                                print("  -> Cantidad no válida.")
                        else:
                            print("  -> Código no encontrado.")

        elif opcion == "6":
            print("\n" + "=" * 50)
            print("         GESTIÓN DE PERSONAL DEL TALLER")
            print("=" * 50)
            print(" --- PERSONAL REGISTRADO ACTUALMENTE ---")
            for idx, p in enumerate(taller.lista_personal, 1):
                print(f"  {idx}. {p.obtener_datos()}")
            print("-" * 50)

            print(" 1. Registrar Nuevo Mecánico")
            print(" 2. Registrar Nuevo Propietario / Dueño de Vehículo")
            print(" 3. Ver lista completa de personal")
            print(" 0. Volver al menú principal")
            sub_op = input(" Seleccione una opción: ").strip()

            if sub_op == "1":
                print("\n [REGISTRO DE NUEVO MECÁNICO]")
                c_id = input(" Cédula/ID: ").strip()
                nom = input(" Nombre completo: ").strip()
                tel = input(" Teléfono: ").strip()
                esp = input(" Especialidad (ej. Frenos, Inyección, General): ").strip() or "Mecánica General"
                cod = input(" Código de empleado (ej. MEC-03): ").strip() or f"MEC-0{len(taller.obtener_mecanicos())+1}"

                mec = Mecanico(c_id, nom, tel, esp, cod)
                taller.registrar_mecanico(mec)
                print(f" ¡Mecánico [{nom}] registrado con éxito en el sistema!")

            elif sub_op == "2":
                print("\n [REGISTRO DE NUEVO PROPIETARIO / DUEÑO]")
                c_id = input(" Cédula/ID: ").strip()
                nom = input(" Nombre completo: ").strip()
                tel = input(" Teléfono: ").strip()
                dir_p = input(" Dirección de residencia: ").strip()

                prop = Propietario(c_id, nom, tel, dir_p)
                taller.registrar_propietario(prop)
                print(f" ¡Propietario [{nom}] registrado con éxito en el sistema!")

            elif sub_op == "3":
                print("\n --- LISTADO COMPLETO ---")
                print(" Mecánicos:")
                for m in taller.obtener_mecanicos():
                    print("  -", m.obtener_datos())
                print("\n Propietarios / Dueños:")
                for p in taller.obtener_propietarios():
                    print("  -", p.obtener_datos())

        elif opcion == "7":
            print("\n--- NAVEGACIÓN EN COLA DE SIMULACIÓN ---")
            print(" 1. Siguiente vehículo en cola")
            print(" 2. Vehículo anterior en cola")
            sub_op = input(" Opción: ").strip()
            if sub_op == "1":
                print("\n", taller.siguiente_vehiculo_cola())
            elif sub_op == "2":
                print("\n", taller.anterior_vehiculo_cola())

        elif opcion == "0":
            print("\n ¡Saliendo del Sistema de Inventario y Mantenimiento del Taller!")
            print("\n Trabajar y trabajar")
            break


if __name__ == "__main__":
    ejecutar_menu_consola()
