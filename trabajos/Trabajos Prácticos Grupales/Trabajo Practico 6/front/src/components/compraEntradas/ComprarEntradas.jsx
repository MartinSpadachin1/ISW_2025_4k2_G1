// CompraEntradas.jsx
import React, { useState, useContext } from "react";
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import Animalito from "../../assets/colibri.jpg";
import ModalComprarEntradas from "./modalComprarEntradas";
import ModalPago from "./ModalPago";
import ModalConfirmacion from "./ModalConfirmacion";
import api from "../../services/api";
import { AuthContext } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useToast } from '../common/ToastContext';
export default function CompraEntradas() {
  // ahora manejamos fecha como objeto Date o null
  const [fecha, setFecha] = useState(null);
  const [cantidad, setCantidad] = useState("");
  const [metodoPago, setMetodoPago] = useState("");
  const [mostrarModal, setMostrarModal] = useState(false);
  const [entradasCargadas, setEntradasCargadas] = useState([]);
  const [showConfirmacion, setShowConfirmacion] = useState(false);
  const [confirmacionData, setConfirmacionData] = useState({ idReserva: null, entradas: [], fecha: null });

  const fechaActual = new Date();

  // Hooks que deben definirse antes de los handlers que los usan
  const auth = useContext(AuthContext);
  const navigate = useNavigate();
  const toast = useToast();

  const handleEntradasChange = (nuevasEntradas) => {
    setEntradasCargadas(nuevasEntradas);
  };

  const handleConfirmar = () => {
    if (!fecha || !cantidad || !metodoPago) {
      toast.show("Por favor completá todos los campos antes de confirmar.");
      return;
    }
    // Si no está autenticado, mostrar modal de invitación a loguearse
    if (!auth || !auth.token) {
      setShowAuthModal(true);
      return;
    }
    // Abrir el modal de configuración para completar edades/tipos
    setMostrarModal(true);
  };

  const handleCancelar = () => {
    setFecha("");
    setCantidad("");
    setMetodoPago("");
    setMostrarModal(false);
  };

  const cerrarModal = (datos) => {
    setMostrarModal(false);
    if (datos) {
      // datos puede venir como { entradas, id_compra }
      if (datos.entradas) setEntradasCargadas(datos.entradas);
      console.log("Entradas cargadas:", datos.entradas || datos);
      
      // Si vino id_compra y el método de pago actual es tarjeta, calculamos monto y abrimos ModalPago
      if (datos.id_compra && metodoPago === 'tarjeta') {
        setIdReservaPago(datos.id_compra);
        const entradasRecibidas = datos.entradas || [];
        const total = entradasRecibidas.reduce((acc, e) => acc + (Number(e.precio) || 0), 0);
        setMontoPago(total);
        setShowModalPago(true);
      }
      // Si el método es efectivo, mostramos toast de éxito
      if (datos.id_compra && metodoPago === 'efectivo') {
        // abrir modal de confirmación en lugar de toast
  const entradasRecibidas = datos.entradas || [];
        const total = entradasRecibidas.reduce((acc, e) => acc + (Number(e.precio) || 0), 0);
        setConfirmacionData({ idReserva: datos.id_compra, entradas: datos.entradas || [], fecha, monto: total, metodoPago: metodoPago });
        setShowConfirmacion(true);
        // limpiar formulario
        setFecha(null);
        setCantidad('');
        setMetodoPago('');
        setEntradasCargadas([]);
      }
    }
  };

  // estado para modal de pago
  const [showModalPago, setShowModalPago] = useState(false);
  const [idReservaPago, setIdReservaPago] = useState(null);
  const [montoPago, setMontoPago] = useState(null);

  const handlePagoClose = (result) => {
    setShowModalPago(false);
    if (result && result.success) {
      // Mostrar modal de confirmación en lugar de toast
  setConfirmacionData({ idReserva: idReservaPago, entradas: entradasCargadas, fecha, monto: montoPago, metodoPago: 'tarjeta' });
      setShowConfirmacion(true);
      // limpiar formulario
      setFecha(null);
      setCantidad('');
      setMetodoPago('');
      setEntradasCargadas([]);
      setIdReservaPago(null);
    }
  };

  // estado para modal de autenticación
  const [showAuthModal, setShowAuthModal] = useState(false);

  return (
    <div
      className="w-100 d-flex align-items-center justify-content-center p-3 p-md-4"
      style={{
        minHeight: "100vh",
        paddingTop: "80px", // compensa navbar
        paddingBottom: "80px", // compensa footer
        boxSizing: "border-box",
      }}
    >
      <div className="row w-100 g-0" style={{ maxWidth: "1200px" }}>
        {/* Imagen del animalito: solo en desktop */}
        <div className="col-12 col-md-4 d-none d-md-flex">
          <img
            src={Animalito}
            alt="Animal del parque"
            className="w-100 h-100"
            style={{
              objectFit: "cover",
              maxHeight: "80vh",
              borderRadius: "12px 0 0 12px",
            }}
          />
        </div>

        {/* Formulario de compra */}
        <div className="col-12 col-md-8 d-flex">
          <div
            className="card shadow w-100 border-0 rounded-3"
            style={{ backgroundColor: "white" }}
          >
            <div className="card-body p-4 p-md-5 d-flex flex-column">
              <h3 className="card-title text-center mb-4">Comprar Entradas</h3>

              {/* Fecha */}
              <div className="mb-3">
                <label className="form-label">Fecha</label>
                <div className="d-flex align-items-center gap-2">
                  <div style={{ position: 'relative', minWidth: 220 }}>
                    <DatePicker
                      selected={fecha}
                      onChange={(date) => setFecha(date)}
                      minDate={fechaActual}
                      dateFormat="dd/MM/yyyy"
                      placeholderText="Elegí la fecha de tu visita"
                      className="form-control"
                      aria-label="Seleccionar fecha de visita"
                    />
                  </div>

                  {/* Aclaración: no abre los lunes ni en Navidad (25/12) y Año Nuevo (01/01) */}
                  <div className="form-text text-muted mt-1">Aclaración: el parque <strong>no abre</strong> los días <strong>lunes</strong> ni los <strong>días festivos (25/12 y 01/01)</strong>. Por favor tenlo en cuenta al elegir la fecha.</div>
                </div>
                
              </div>

              {/* Cantidad */}
              <div className="mb-3">
                <label className="form-label mb-1">Cantidad de entradas</label>
                <input
                  type="number"
                  className="form-control"
                  min="1"
                  max="10"
                  value={cantidad}
                  onChange={(e) => {
                    const val = Number(e.target.value);
                    if (val >= 1 && val <= 10 && Number.isInteger(val)) setCantidad(val);
                    else if (e.target.value === "") setCantidad("");
                  }}
                />
                <small className="text-muted">Máx. 10 entradas por compra.</small>
              </div>

              {/* Método de pago */}
              <div className="mb-3">
                <label className="form-label d-block">Método de pago:</label>
                <div className="form-check form-check-inline">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="metodoPago"
                    id="efectivo"
                    value="efectivo"
                    checked={metodoPago === "efectivo"}
                    onChange={(e) => setMetodoPago(e.target.value)}
                  />
                  <label className="form-check-label" htmlFor="efectivo">
                    Efectivo
                  </label>
                </div>
                <div className="form-check form-check-inline">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="metodoPago"
                    id="tarjeta"
                    value="tarjeta"
                    checked={metodoPago === "tarjeta"}
                    onChange={(e) => setMetodoPago(e.target.value)}
                  />
                  <label className="form-check-label" htmlFor="tarjeta">
                    Tarjeta
                  </label>
                </div>
              </div>

              {/* Botones */}
              <div className="d-flex justify-content-between mt-auto pt-2">
                <button className="btn btn-secondary" onClick={handleCancelar}>
                  Cancelar
                </button>
                <button
                  className="btn btn-success"
                  style={{ backgroundColor: "#3da35d", borderColor: "#3da35d" }}
                  onClick={handleConfirmar}
                >
                  Confirmar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      {mostrarModal && (
        <ModalComprarEntradas
          cantidad={cantidad}
          fecha={fecha}
          metodoPago={metodoPago}
          onClose={cerrarModal}
          entradasIniciales={entradasCargadas} // le pasamos los datos previos
          onChange={handleEntradasChange} // callback para cada cambio
        />
      )}
      {showModalPago && idReservaPago && (
        <ModalPago idReserva={idReservaPago} monto={montoPago} onClose={handlePagoClose} />
      )}
      {showAuthModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-md">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Necesitás una cuenta</h5>
                <button type="button" className="btn-close" onClick={() => setShowAuthModal(false)}></button>
              </div>
              <div className="modal-body">
                <p>Para confirmar una reserva necesitás iniciar sesión o registrarte. Podés hacerlo ahora y continuar con la compra.</p>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAuthModal(false)}>Cancelar</button>
                <button type="button" className="btn btn-outline-success" onClick={() => { setShowAuthModal(false); navigate('/registrarse'); }}>Registrarse</button>
                <button type="button" className="btn btn-success" onClick={() => { setShowAuthModal(false); navigate('/iniciar-sesion'); }}>Iniciar sesión</button>
              </div>
            </div>
          </div>
        </div>
      )}
      {showConfirmacion && (
        <ModalConfirmacion idReserva={confirmacionData.idReserva} entradas={confirmacionData.entradas} fecha={confirmacionData.fecha} monto={confirmacionData.monto} metodoPago={confirmacionData.metodoPago} onClose={() => setShowConfirmacion(false)} />
      )}
    </div>
  );
}
