import React, { useState } from "react";

export default function CompraEntradas() {
  const [fecha, setFecha] = useState("");
  const [cantidad, setCantidad] = useState("");
  const [metodoPago, setMetodoPago] = useState("");
  const [cardIzquierda, setCardIzquierda] = useState(false); // controla el desplazamiento

  const fechaActual = new Date().toISOString().split("T")[0];

  // === Confirmar ===
  const handleConfirmar = () => {
    if (!fecha || !cantidad || !metodoPago) {
      alert("Por favor completá todos los campos antes de confirmar.");
      return;
    }
    setCardIzquierda(true);
  };

  // === Cancelar ===
  const handleCancelar = () => {
    setFecha("");
    setCantidad("");
    setMetodoPago("");
    setCardIzquierda(false);
  };

  // === Configurar ===
  const handleConfigurar = () => {
    if (!cantidad) {
      alert("Debés ingresar una cantidad antes de configurar.");
      return;
    }
    setCardIzquierda(true);
  };

  return (
    <div
      className={`d-flex vh-100 ${
        cardIzquierda ? "justify-content-start" : "justify-content-center"
      } align-items-center `}
      style={{ transition: "all 0.5s ease" }}
    >
      <div
        className="card shadow p-4"
        style={{
          width: "30vw",
          minWidth: "22rem",
          borderRadius: "1rem",
          marginLeft: cardIzquierda ? "5vw" : "0",
          transition: "all 0.5s ease",
        }}
      >
        <h3 className="card-title text-center mb-4">Comprar Entradas</h3>

        {/* === Fecha === */}
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

        {/* === Cantidad + Configurar === */}
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
            className="btn btn-warning ms-3"
            style={{ height: "fit-content", marginBottom: "0.25rem" }}
            onClick={handleConfigurar}
          >
            Configurar
          </button>
        </div>

        {/* === Método de pago === */}
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

        {/* === Botones === */}
        <div className="d-flex justify-content-between mt-4">
          <button className="btn btn-secondary" onClick={handleCancelar}>
            Cancelar
          </button>
          <button className="btn btn-primary" onClick={handleConfirmar}>
            Confirmar
          </button>
        </div>
      </div>
    </div>
  );
}
