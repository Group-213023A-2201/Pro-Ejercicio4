import logging
from abc import ABC, abstractmethod
import re
from datetime import datetime

# =====================================================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS (Archivos)
# =====================================================================
# Se configura el registro para no usar bases de datos, solo un archivo local
logging.basicConfig(
    filename='registro_eventos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =====================================================================
# 2. MANEJO AVANZADO DE EXCEPCIONES (Excepciones Personalizadas)
# =====================================================================
class SoftwareFJException(Exception):
    """Excepción base para el sistema Software FJ."""
    pass

class ValidacionDatosError(SoftwareFJException):
    """Excepción lanzada cuando los datos de entrada no son válidos."""
    pass

class OperacionInvalidaError(SoftwareFJException):
    """Excepción lanzada al intentar una operación no permitida (ej. doble cancelación)."""
    pass

class ServicioNoDisponibleError(SoftwareFJException):
    """Excepción lanzada cuando hay problemas con el servicio solicitado."""
    pass

# =====================================================================
# 3. CLASES ABSTRACTAS (Abstracción)
# =====================================================================
class EntidadGeneral(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad
        
    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def obtener_resumen(self):
        """Método abstracto para obtener un resumen de la entidad."""
        pass


class Servicio(EntidadGeneral):
    """Clase abstracta para los servicios, hereda de EntidadGeneral."""
    def __init__(self, id_entidad, nombre, tarifa_base):
        super().__init__(id_entidad)
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.validar_parametros()

    def validar_parametros(self):
        if self.tarifa_base < 0:
            raise ValidacionDatosError(f"La tarifa base del servicio {self.nombre} no puede ser negativa.")

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0.0, impuesto=0.0):
        """
        Calcula el costo del servicio. 
        MÉTODO SOBRECARGADO (Simulado en Python usando parámetros por defecto).
        """
        pass

    @abstractmethod
    def describir_servicio(self):
        """Devuelve la descripción especializada del servicio."""
        pass


# =====================================================================
# 4. CLASES DERIVADAS Y ENCAPSULACIÓN
# =====================================================================
class Cliente(EntidadGeneral):
    """Clase Cliente con encapsulación estricta y validaciones robustas."""
    def __init__(self, id_entidad, nombre, identificacion, correo):
        super().__init__(id_entidad)
        self.__nombre = None
        self.__identificacion = None
        self.__correo = None
        
        # Uso de setters para validación automática al instanciar
        self.nombre = nombre
        self.identificacion = identificacion
        self.correo = correo

    # Encapsulación: Getters y Setters
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValidacionDatosError("El nombre del cliente no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not isinstance(valor, str) or not valor.isalnum():
            raise ValidacionDatosError("La identificación debe ser alfanumérica.")
        self.__identificacion = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, valor):
            raise ValidacionDatosError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor

    def obtener_resumen(self):
        return f"Cliente: {self.nombre} (ID: {self.identificacion}) - {self.correo}"


# --- Implementación de Polimorfismo en Servicios ---

class ReservaSala(Servicio):
    def __init__(self, id_entidad, nombre, tarifa_base, capacidad):
        self.capacidad = capacidad
        super().__init__(id_entidad, nombre, tarifa_base)

    def calcular_costo(self, duracion, descuento=0.0, impuesto=0.0):
        # La sala cobra tarifa por hora + un recargo por limpieza fijo de 20
        costo_base = (self.tarifa_base * duracion) + 20
        costo_descuento = costo_base * (1 - descuento)
        return costo_descuento * (1 + impuesto)

    def describir_servicio(self):
        return f"Sala de reuniones '{self.nombre}' con capacidad para {self.capacidad} personas."

    def obtener_resumen(self):
        return self.describir_servicio()


class AlquilerEquipo(Servicio):
    def __init__(self, id_entidad, nombre, tarifa_base, requiere_deposito):
        self.requiere_deposito = requiere_deposito
        super().__init__(id_entidad, nombre, tarifa_base)

    def calcular_costo(self, duracion, descuento=0.0, impuesto=0.0):
        # El equipo cobra tarifa por día
        costo_base = self.tarifa_base * duracion
        deposito = 50 if self.requiere_deposito else 0
        return (costo_base * (1 - descuento) * (1 + impuesto)) + deposito

    def describir_servicio(self):
        dep = "con" if self.requiere_deposito else "sin"
        return f"Alquiler de equipo: {self.nombre} ({dep} depósito requerido)."

    def obtener_resumen(self):
        return self.describir_servicio()


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_entidad, nombre, tarifa_base, nivel_experto):
        self.nivel_experto = nivel_experto
        super().__init__(id_entidad, nombre, tarifa_base)

    def calcular_costo(self, duracion, descuento=0.0, impuesto=0.0):
        # La asesoría tiene un multiplicador según el nivel del experto
        multiplicador = 1.5 if self.nivel_experto == 'Senior' else 1.0
        costo_base = self.tarifa_base * duracion * multiplicador
        return costo_base * (1 - descuento) * (1 + impuesto)

    def describir_servicio(self):
        return f"Asesoría en {self.nombre} por consultor {self.nivel_experto}."

    def obtener_resumen(self):
        return self.describir_servicio()


# =====================================================================
# 5. CLASE RESERVA Y LÓGICA DE NEGOCIO
# =====================================================================
class Reserva(EntidadGeneral):
    ESTADOS = ['Pendiente', 'Confirmada', 'Cancelada']

    def __init__(self, id_entidad, cliente, servicio, duracion):
        super().__init__(id_entidad)
        if not isinstance(cliente, Cliente):
            raise ValidacionDatosError("El cliente asignado no es válido.")
        if not isinstance(servicio, Servicio):
            raise ServicioNoDisponibleError("El servicio asignado no es válido.")
        if duracion <= 0:
            raise ValidacionDatosError("La duración debe ser mayor a cero.")
            
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = 'Pendiente'
        self.fecha_creacion = datetime.now()

    def confirmar(self):
        """Confirma la reserva utilizando try/except/else/finally."""
        try:
            if self.estado != 'Pendiente':
                raise ValueError("Solo se pueden confirmar reservas pendientes.")
            # Simulamos el proceso de confirmación
            self.estado = 'Confirmada'
        except ValueError as e:
            # Encadenamiento de excepciones (Exception Chaining)
            raise OperacionInvalidaError("Error en la validación de estado.") from e
        else:
            logging.info(f"Reserva {self.id_entidad} confirmada exitosamente.")
            print(f"-> [Éxito] Reserva {self.id_entidad} confirmada.")
        finally:
            logging.info(f"Intento de confirmación finalizado para reserva {self.id_entidad}.")

    def cancelar(self):
        if self.estado == 'Cancelada':
            raise OperacionInvalidaError("La reserva ya se encuentra cancelada.")
        self.estado = 'Cancelada'
        logging.info(f"Reserva {self.id_entidad} cancelada.")

    def procesar_pago(self, descuento=0.0, impuesto=0.0):
        # Uso de polimorfismo y métodos sobrecargados (argumentos opcionales)
        costo = self.servicio.calcular_costo(self.duracion, descuento, impuesto)
        return costo

    def obtener_resumen(self):
        return f"Reserva {self.id_entidad} | {self.cliente.nombre} | {self.servicio.nombre} | Estado: {self.estado}"


# =====================================================================
# 6. SIMULACIÓN DE 10 OPERACIONES (Gestión mediante Listas)
# =====================================================================
def ejecutar_simulacion():
    print("=== INICIANDO SIMULACIÓN SISTEMA SOFTWARE FJ ===\n")
    clientes = []
    servicios = []
    reservas = []

    # Operación 1: Creación de Cliente Válido
    try:
        print("Op 1: Registrando cliente válido...")
        cliente1 = Cliente(1, "Ana Gómez", "CC123456", "ana@empresa.com")
        clientes.append(cliente1)
        logging.info(f"Cliente registrado: {cliente1.obtener_resumen()}")
        print("-> [Éxito] Cliente creado.")
    except Exception as e:
        print(f"-> [Error]: {e}")

    # Operación 2: Creación de Cliente Inválido (Correo incorrecto)
    try:
        print("\nOp 2: Registrando cliente con correo inválido...")
        cliente2 = Cliente(2, "Luis Pérez", "CC789", "correo-invalido")
        clientes.append(cliente2)
    except ValidacionDatosError as e:
        logging.error(f"Fallo al registrar cliente: {e}")
        print(f"-> [Excepción Capturada]: {e}")

    # Operación 3: Creación de Servicio Válido (Sala)
    try:
        print("\nOp 3: Creando servicio ReservaSala...")
        sala = ReservaSala(101, "Sala Auditorio", tarifa_base=50, capacidad=100)
        servicios.append(sala)
        logging.info("Servicio Sala creado.")
        print("-> [Éxito] Servicio de sala creado.")
    except Exception as e:
        print(f"-> [Error]: {e}")

    # Operación 4: Creación de Servicio Inválido (Tarifa negativa)
    try:
        print("\nOp 4: Creando servicio con tarifa negativa...")
        equipo_error = AlquilerEquipo(102, "Proyector", tarifa_base=-10, requiere_deposito=True)
    except ValidacionDatosError as e:
        logging.error(f"Fallo al crear servicio: {e}")
        print(f"-> [Excepción Capturada]: {e}")

    # Operación 5: Creación de Servicio Válido (Asesoría)
    try:
        print("\nOp 5: Creando servicio Asesoría Especializada...")
        asesoria = AsesoriaEspecializada(103, "Optimización de BD", tarifa_base=100, nivel_experto="Senior")
        servicios.append(asesoria)
        print("-> [Éxito] Asesoría creada.")
    except Exception as e:
        print(f"-> [Error]: {e}")

    # Operación 6: Creación de Reserva Exitosa
    try:
        print("\nOp 6: Creando una reserva válida...")
        reserva1 = Reserva(1001, clientes[0], servicios[0], duracion=4) # 4 horas
        reservas.append(reserva1)
        logging.info(f"Reserva creada: {reserva1.obtener_resumen()}")
        print(f"-> [Éxito] {reserva1.obtener_resumen()}")
    except Exception as e:
        print(f"-> [Error]: {e}")

    # Operación 7: Confirmación de Reserva (Uso de try/except/else/finally)
    print("\nOp 7: Confirmando la reserva anterior...")
    reservas[0].confirmar()

    # Operación 8: Creación de Reserva Fallida (Datos incompletos/nulos)
    try:
        print("\nOp 8: Creando reserva sin cliente...")
        reserva2 = Reserva(1002, None, servicios[1], duracion=2)
    except ValidacionDatosError as e:
        logging.error(f"Intento de reserva inválida: {e}")
        print(f"-> [Excepción Capturada]: {e}")

    # Operación 9: Error encadenado y estado inválido (Doble confirmación)
    try:
        print("\nOp 9: Intentando confirmar una reserva que ya está confirmada...")
        reservas[0].confirmar()
    except OperacionInvalidaError as e:
        logging.error(f"Error de operación: {e.__cause__} -> {e}")
        print(f"-> [Excepción Capturada por Encadenamiento]: {e} (Causa original: {e.__cause__})")

    # Operación 10: Polimorfismo y Sobrecarga simulada de métodos (Cálculos de costo)
    try:
        print("\nOp 10: Calculando costos con métodos sobrecargados (Polimorfismo)...")
        # Costo normal
        costo_normal = reservas[0].procesar_pago()
        # Costo con descuento e impuesto (Simulación de sobrecarga)
        costo_descuento = reservas[0].procesar_pago(descuento=0.10, impuesto=0.19)
        
        print(f"-> Costo base (4 horas): ${costo_normal:.2f}")
        print(f"-> Costo con 10% desc. y 19% IVA: ${costo_descuento:.2f}")
        logging.info("Cálculos de costo ejecutados exitosamente mediante polimorfismo.")
    except Exception as e:
         print(f"-> [Error en el cálculo]: {e}")

    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revisa el archivo 'registro_eventos.log' para ver la trazabilidad de excepciones.")

if __name__ == "__main__":
    ejecutar_simulacion()