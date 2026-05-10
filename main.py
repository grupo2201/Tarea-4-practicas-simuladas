import tkinter as tk
from tkinter import ttk, messagebox

from models import (
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva
)
from excepciones import ReservaError
from utils.logger import log_error, log_info

class AppReservaFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Sistema de Reservas")
        self.root.geometry("800x800")

        # Memoria temporal
        self.clientes = []
        self.servicios = []
        self.reservas = []

        self.crear_widgets()

    def crear_widgets(self):
        # --- SECCIÓN CLIENTE ---
        frame_cliente = ttk.LabelFrame(self.root, text="Gestión de Clientes")
        frame_cliente.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_cliente, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(frame_cliente)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_cliente, text="Identificación:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_cliente)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_cliente, text="Registrar Cliente", command=self.registrar_cliente).grid(row=2, column=0, columnspan=2, pady=5)

        # --- SECCIÓN SERVICIO ---
        frame_servicio = ttk.LabelFrame(self.root, text="Gestión de Servicios")
        frame_servicio.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_servicio, text="Tipo:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_tipo_serv = ttk.Combobox(frame_servicio, values=["Reserva Sala", "Alquiler Equipo", "Asesoría"], state="readonly")
        self.combo_tipo_serv.current(0)
        self.combo_tipo_serv.grid(row=0, column=1, padx=5, pady=5)
        self.combo_tipo_serv.bind("<<ComboboxSelected>>", self.actualizar_campos_servicio)

        ttk.Label(frame_servicio, text="ID / Código:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_id_serv = ttk.Entry(frame_servicio)
        self.entry_id_serv.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_servicio, text="Nombre:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_nom_serv = ttk.Entry(frame_servicio)
        self.entry_nom_serv.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_servicio, text="Costo Base ($):").grid(row=3, column=0, padx=5, pady=5)
        self.entry_costo_serv = ttk.Entry(frame_servicio)
        self.entry_costo_serv.grid(row=3, column=1, padx=5, pady=5)

        # Campos dinámicos
        self.lbl_attr1 = ttk.Label(frame_servicio, text="Capacidad:")
        self.lbl_attr1.grid(row=4, column=0, padx=5, pady=5)
        self.entry_attr1 = ttk.Entry(frame_servicio)
        self.entry_attr1.grid(row=4, column=1, padx=5, pady=5)

        self.lbl_attr2 = ttk.Label(frame_servicio, text="Ubicación:")
        self.lbl_attr2.grid(row=5, column=0, padx=5, pady=5)
        self.entry_attr2 = ttk.Entry(frame_servicio)
        self.entry_attr2.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(frame_servicio, text="Crear Servicio", command=self.registrar_servicio).grid(row=6, column=0, columnspan=2, pady=5)

        # --- SECCIÓN RESERVA ---
        frame_reserva = ttk.LabelFrame(self.root, text="Generar Reserva")
        frame_reserva.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_reserva, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_clientes = ttk.Combobox(frame_reserva, state="readonly", width=40)
        self.combo_clientes.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_reserva, text="Servicio:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_servicios_res = ttk.Combobox(frame_reserva, state="readonly", width=40)
        self.combo_servicios_res.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_reserva, text="Duración/Cant:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_duracion = ttk.Entry(frame_reserva)
        self.entry_duracion.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_reserva, text="Procesar Reserva", command=self.crear_reserva).grid(row=3, column=0, columnspan=2, pady=5)

        # --- BOTÓN DE SIMULACIÓN ---
        frame_acciones = ttk.Frame(self.root)
        frame_acciones.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_acciones, text="Simular 10 Operaciones", command=self.simular_operaciones).pack(side="left", padx=5)

        # --- ÁREA DE LOGS ---
        frame_log = ttk.LabelFrame(self.root, text="Registro de Eventos (Logs)")
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_logs = tk.Text(frame_log, height=15)
        self.txt_logs.pack(fill="both", expand=True, padx=5, pady=5)

    def log_gui(self, mensaje, nivel="INFO"):
        if nivel == "INFO":
            log_info(mensaje)
        else:
            log_error(mensaje)
        self.txt_logs.insert(tk.END, f"[{nivel}] {mensaje}\n")
        self.txt_logs.see(tk.END)

    def actualizar_campos_servicio(self, event=None):
        tipo = self.combo_tipo_serv.get()
        self.entry_attr1.delete(0, tk.END)
        self.entry_attr2.delete(0, tk.END)
        if tipo == "Reserva Sala":
            self.lbl_attr1.config(text="Capacidad:")
            self.lbl_attr2.config(text="Ubicación:")
        elif tipo == "Alquiler Equipo":
            self.lbl_attr1.config(text="Tipo de Equipo:")
            self.lbl_attr2.config(text="Estado (ej. Disponible):")
        elif tipo == "Asesoría":
            self.lbl_attr1.config(text="Especialidad:")
            self.lbl_attr2.config(text="Consultor:")

    def actualizar_comboboxes(self):
        lista_clientes = [f"{c.identificacion} - {c.nombre}" for c in self.clientes]
        self.combo_clientes["values"] = lista_clientes
        if lista_clientes and self.combo_clientes.current() == -1:
            self.combo_clientes.current(0)
            
        lista_servicios = [f"{s._id_entidad} - {s._nombre_servicio}" for s in self.servicios]
        self.combo_servicios_res["values"] = lista_servicios
        if lista_servicios and self.combo_servicios_res.current() == -1:
            self.combo_servicios_res.current(0)

    def registrar_cliente(self):
        nombre = self.entry_nombre.get()
        identificacion = self.entry_id.get()
        try:
            cliente = Cliente(nombre, identificacion)
            self.clientes.append(cliente)
            self.actualizar_comboboxes()
            self.log_gui(f"Cliente registrado: {cliente.obtener_detalles()}")
            messagebox.showinfo("Éxito", "Cliente registrado exitosamente")
        except ReservaError as e:
            self.log_gui(f"Error de validación: {e}", "ERROR")
            messagebox.showwarning("Error", str(e))
        except Exception as e:
            self.log_gui(f"Error: {e}", "ERROR")
        finally:
            self.entry_nombre.delete(0, tk.END)
            self.entry_id.delete(0, tk.END)

    def registrar_servicio(self):
        tipo = self.combo_tipo_serv.get()
        id_serv = self.entry_id_serv.get()
        nombre = self.entry_nom_serv.get()
        
        try:
            costo_str = self.entry_costo_serv.get()
            if not costo_str:
                raise ValueError("Costo base es obligatorio.")
            costo = float(costo_str)
            val1 = self.entry_attr1.get()
            val2 = self.entry_attr2.get()

            if not id_serv or not nombre:
                raise ValueError("ID y Nombre son obligatorios")

            if tipo == "Reserva Sala":
                if not val1.isdigit():
                    raise ValueError("Capacidad debe ser un número entero.")
                capacidad = int(val1)
                servicio = ReservaSala(id_serv, nombre, costo, 1, capacidad, val2)
            elif tipo == "Alquiler Equipo":
                servicio = AlquilerEquipo(id_serv, nombre, costo, 1, val1, val2)
            elif tipo == "Asesoría":
                servicio = AsesoriaEspecializada(id_serv, nombre, costo, 1, val1, val2)

            self.servicios.append(servicio)
            self.actualizar_comboboxes()
            self.log_gui(f"Servicio registrado: {servicio.obtener_detalles()}")
            messagebox.showinfo("Éxito", "Servicio registrado exitosamente")
            
            self.entry_id_serv.delete(0, tk.END)
            self.entry_nom_serv.delete(0, tk.END)
            self.entry_costo_serv.delete(0, tk.END)
            self.entry_attr1.delete(0, tk.END)
            self.entry_attr2.delete(0, tk.END)

        except ValueError as e:
            self.log_gui(f"Datos inválidos al crear servicio: {e}", "ERROR")
            messagebox.showwarning("Error", "Datos numéricos o valores inválidos.")
        except ReservaError as e:
            self.log_gui(f"Error de negocio: {e}", "ERROR")
            messagebox.showwarning("Error", str(e))
        except Exception as e:
            self.log_gui(f"Error: {e}", "ERROR")

    def crear_reserva(self):
        idx_cli = self.combo_clientes.current()
        idx_serv = self.combo_servicios_res.current()
        duracion_str = self.entry_duracion.get()

        if idx_cli == -1 or idx_serv == -1:
            messagebox.showerror("Error", "Debe seleccionar un cliente y un servicio válidos.")
            return

        cliente = self.clientes[idx_cli]
        servicio = self.servicios[idx_serv]

        try:
            duracion = int(duracion_str) if duracion_str else 0
            id_reserva = f"R{len(self.reservas) + 1}"
            
            reserva = Reserva(id_reserva, cliente, servicio, duracion)
            reserva.procesar_reserva()
            
            self.reservas.append(reserva)
            
            if isinstance(servicio, ReservaSala):
                parametros = {"horas": duracion}
            elif isinstance(servicio, AlquilerEquipo):
                parametros = {"dias": duracion}
            else:
                parametros = {"horas": duracion, "nivel": "normal"}

            costo = servicio.calcular_costo(parametros)
            self.log_gui(f"Reserva creada: {reserva.obtener_detalles()} | Costo Calculado: ${costo}")
            messagebox.showinfo("Éxito", f"Reserva completada.\nCosto total: ${costo}")

        except ValueError:
            self.log_gui("La duración debe ser un número entero.", "ERROR")
            messagebox.showwarning("Error", "Duración inválida.")
        except ReservaError as e:
            self.log_gui(str(e), "ERROR")
            messagebox.showwarning("Fallo en Reserva", str(e))
        except Exception as e:
            self.log_gui(f"Error crítico al crear reserva: {e}", "ERROR")

    def simular_operaciones(self):
        self.txt_logs.delete(1.0, tk.END)
        self.log_gui("--- INICIANDO SIMULACIÓN DE 10 OPERACIONES ---")
        
        try:
            # 1. Cliente válido
            c1 = Cliente("Juan Perez", "1010")
            self.clientes.append(c1)
            self.log_gui("Op 1: Cliente Juan Perez creado (Éxito)")
            
            # 2. Cliente inválido
            try:
                c2 = Cliente("A", "2020")
            except Exception as e:
                self.log_gui(f"Op 2: Error esperado al crear cliente: {e}", "ERROR")

            # 3. Crear Servicios Válidos y Reserva
            s1 = ReservaSala("S_SIM_1", "Sala Norte", 50, 1, 10, "Piso 2")
            self.servicios.append(s1)
            r1 = Reserva("R_SIM_1", c1, s1, 2)
            r1.procesar_reserva()
            costo = s1.calcular_costo({"horas": 2})
            self.log_gui(f"Op 3: Reserva Sala procesada (Éxito). Costo: ${costo}")

            # 4. Reserva Equipo
            s2 = AlquilerEquipo("E_SIM_1", "Laptop", 30, 1, "Portátil", "Disponible")
            self.servicios.append(s2)
            r2 = Reserva("R_SIM_2", c1, s2, 3)
            r2.procesar_reserva()
            self.log_gui("Op 4: Reserva Equipo procesada (Éxito)")

            # 5. Reserva Asesoría
            s3 = AsesoriaEspecializada("A_SIM_1", "Consultoría", 100, 1, "IA", "Carlos")
            self.servicios.append(s3)
            r3 = Reserva("R_SIM_3", c1, s3, 2)
            r3.procesar_reserva()
            self.log_gui("Op 5: Reserva Asesoría procesada (Éxito)")

            # 6. Reserva fallida: Cliente nulo
            try:
                r4 = Reserva("R_SIM_4", None, s1, 2)
                r4.procesar_reserva()
            except Exception as e:
                self.log_gui(f"Op 6: Error esperado, Reserva sin cliente falló: {e}", "ERROR")

            # 7. Cancelar reserva
            r1.cancelar_reserva()
            self.log_gui("Op 7: Reserva R1 cancelada (Éxito)")

            # 8. Cancelar reserva ya cancelada
            try:
                r1.cancelar_reserva()
            except Exception as e:
                self.log_gui(f"Op 8: Error esperado al cancelar de nuevo: {e}", "ERROR")

            # 9. Crear Sala con capacidad 0
            try:
                s4 = ReservaSala("S_SIM_ERR", "Sala Sur", 50, 1, 0, "Piso 1")
            except Exception as e:
                self.log_gui(f"Op 9: Error esperado al crear sala sin capacidad: {e}", "ERROR")

            # 10. Alquilar equipo no disponible
            try:
                s5 = AlquilerEquipo("E_SIM_ERR", "Microfono", 10, 1, "Audio", "Dañado")
                s5.calcular_costo({"dias": 1})
            except Exception as e:
                self.log_gui(f"Op 10: Error esperado al usar equipo no disponible: {e}", "ERROR")

        except Exception as e:
            self.log_gui(f"Error inesperado en simulación: {e}", "ERROR")
            
        self.actualizar_comboboxes()
        self.log_gui("--- FIN DE SIMULACIÓN ---")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppReservaFJ(root)
    root.mainloop()