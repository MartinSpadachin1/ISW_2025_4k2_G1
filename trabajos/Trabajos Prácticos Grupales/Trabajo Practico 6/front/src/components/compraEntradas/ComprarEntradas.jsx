// CompraEntradas.jsx
import React, { useState } from "react";
import Animalito from '../../assets/colibri.jpg'; 
import ModalComprarEntradas from "./modalComprarEntradas";
export default function CompraEntradas() {
  const [fecha, setFecha] = useState("");
  const [cantidad, setCantidad] = useState("");
  const [metodoPago, setMetodoPago] = useState("");
  const [cardIzquierda, setCardIzquierda] = useState(false);
  const [mostrarModal, setMostrarModal] = useState(false);

  const fechaActual = new Date().toISOString().split("T")[0];

  const handleConfirmar = () => {
    if (!fecha || !cantidad || !metodoPago) {
      alert("Por favor completá todos los campos antes de confirmar.");
      return;
    }
    setCardIzquierda(true);
  };

  const handleCancelar = () => {
    setFecha("");
    setCantidad("");
    setMetodoPago("");
    setCardIzquierda(false);
    setMostrarModal(false);
  };

  const handleConfigurar = () => {
    if (!cantidad) {
      alert("Debés ingresar una cantidad antes de configurar.");
      return;
    }
    setCardIzquierda(true);
    setMostrarModal(true);
  };
  const cerrarModal = () => {
    setMostrarModal(false);
    setCardIzquierda(false);
  };

  return (
    <div
      className="w-100 d-flex align-items-center justify-content-center p-3 p-md-4"
      style={{
        minHeight: '100vh',
        paddingTop: '80px',    // compensa navbar
        paddingBottom: '80px', // compensa footer
        boxSizing: 'border-box',
      }}
    >
      <div className="row w-100 g-0" style={{ maxWidth: '1200px' }}>
        {/* Imagen del animalito: solo en desktop */}
        <div className="col-12 col-md-4 d-none d-md-flex">
          <img
            src={Animalito}
            alt="Animal del parque"
            className="w-100 h-100"
            style={{
              objectFit: 'cover',
              maxHeight: '80vh',
              borderRadius: '12px 0 0 12px',
            }}
          />
        </div>

        {/* Formulario de compra */}
        <div className="col-12 col-md-8 d-flex">
          <div
            className="card shadow w-100 border-0 rounded-3"
            style={{
              backgroundColor: 'white',
              marginLeft: cardIzquierda ? '5vw' : '0',
              transition: 'margin-left 0.5s ease',
            }}
          >
            <div className="card-body p-4 p-md-5 d-flex flex-column">
              <h3 className="card-title text-center mb-4">Comprar Entradas</h3>

              {/* Fecha */}
              <div className="mb-3">
                <label className="form-label">Fecha</label>
                <input
                  type="date"
                  className="form-control"
                  min={fechaActual}
                  value={fecha}
                  onChange={(e) => setFecha(e.target.value)}
                />
              </div>

              {/* Cantidad + Configurar */}
              <div className="d-flex align-items-end justify-content-between mb-3">
                <div style={{ flex: 1 }}>
                  <label className="form-label mb-1">Cantidad de entradas</label>
                  <input
                    type="number"
                    className="form-control"
                    min="1"
                    max="10"
                    value={cantidad}
                    onChange={(e) => {
                      const val = Number(e.target.value);
                      if (val >= 1 && val <= 10) setCantidad(val);
                      else if (e.target.value === "") setCantidad("");
                    }}
                  />
                </div>
                <button
                  className="btn btn-outline-success ms-3"
                  style={{ height: "fit-content", marginBottom: "0.25rem" }}
                  onClick={handleConfigurar}
                >
                  Configurar
                </button>
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
                    value="Efectivo"
                    checked={metodoPago === "Efectivo"}
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
                    value="Tarjeta"
                    checked={metodoPago === "Tarjeta"}
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
                  style={{ backgroundColor: '#3da35d', borderColor: '#3da35d' }}
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
          onClose={cerrarModal}
        />
      )}
    </div>
  );
}