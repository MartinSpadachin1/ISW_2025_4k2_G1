import React, { useEffect, useState } from "react";
import api from "../../services/api";

export default function ModalComprarEntradas({
  cantidad,
  fecha,
  metodoPago,
  onClose,
  entradasIniciales = [],
  onChange,
}) {
  const [precios, setPrecios] = useState(null);
  const [entradas, setEntradas] = useState([]);
  const [mostrar, setMostrar] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const init = async () => {
      try {
        const data = await api.obtenerEdades();
        setPrecios(data);
      } catch (err) {
        console.error(
          "No se pudieron obtener edades desde el backend, usando valores por defecto",
          err
        );
        // fallback a valores hardcodeados
        
      }
    };

    init();

    // Inicializamos las entradas: usamos las que vienen del padre si existen
    const filasIniciales = entradasIniciales.length
      ? entradasIniciales
      : Array.from({ length: cantidad }, () => ({
          edad: "",
          tipo: "",
          precio: 0,
        }));

    setEntradas(filasIniciales);
  }, [cantidad, entradasIniciales]);

 const handleChange = (index, field, value) => {
  const nuevasEntradas = [...entradas];
  if (field === "edad" && value < 0) return;

  nuevasEntradas[index][field] = value;
  setEntradas(nuevasEntradas);

  const edad = nuevasEntradas[index].edad;
  const tipo = nuevasEntradas[index].tipo;

  // Actualizamos al padre inmediatamente
  if (onChange) {
    onChange(nuevasEntradas);
  }

  // Solo llamamos a la API si ambos campos están completos
  if (edad && tipo) {
    api.montoUnico(Number(edad), tipo)
      .then((precio) => {
        const nuevasConPrecio = [...nuevasEntradas];
        nuevasConPrecio[index].precio = precio;
        setEntradas(nuevasConPrecio);

        // También actualizamos al padre con el precio
        if (onChange) {
          onChange(nuevasConPrecio);
        }
      })
      .catch((err) => console.error("Error obteniendo precio:", err));
  }
};


  if (!mostrar) return null;

  const calcularMontoTotalBackend = async () => {
    setError(null);
    setLoading(true);
    try {
      const visitantes = entradas.map((e) => ({
        edad: Number(e.edad),
        tipo_entrada: e.tipo === "vip" ? "vip" : "regular",
      }));
      const res = await api.montoTotal(visitantes);
      setLoading(false);
      return res;
    } catch (err) {
      setLoading(false);
      setError(err.detail || err.message || "Error calculando monto total");
      throw err;
    }
  };

  const handleConfirmar = async () => {
    setError(null);

    // validaciones simples
    for (let i = 0; i < entradas.length; i++) {
      if (!entradas[i].edad || !entradas[i].tipo) {
        setError("Completá todas las edades y tipos");
        return;
      }
    }

    try {
      const visitantes = entradas.map((e) => ({
        edad: Number(e.edad),
        tipo_entrada: e.tipo === "vip" ? "vip" : "general",
      }));

      const payload = {
        token: localStorage.getItem("access_token") || null,
        fecha: fecha || null,
        visitantes,
        forma_pago: metodoPago || null,
      };

      setLoading(true);
      const resVal = await api.validarCompra(payload);
      setLoading(false);

      alert(resVal?.message || "Compra validada correctamente");

      // ✅ devolvemos las entradas al padre
      onClose && onClose(entradas);

      setMostrar(false);
    } catch (err) {
      setLoading(false);
      setError(err.detail || err.message || "Error validando compra");
    }
  };

  return (
    <div
      className="modal show d-block"
      tabIndex="-1"
      style={{
        backgroundColor: "rgba(0,0,0,0.5)",
        transition: "all 0.3s ease",
      }}
    >
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Configurar Entradas</h5>
            <button
              type="button"
              className="btn-close"
              onClick={() => {
                setMostrar(false);
                onClose && onClose();
              }}
            ></button>
          </div>

          <div className="modal-body">
            {precios ? (
              <>
               {/* Tabla de referencia de precios por edad */}
                  <h6 className="fw-bold mb-3">Tabla de Precios por Edad</h6>
                  <table className="table table-sm table-bordered text-center align-middle mb-4">
                    <thead className="table-light">
                      <tr>
                        <th>Categoría</th>
                        <th>Rango de Edad</th>
                        <th>Precio VIP</th>
                        <th>Precio General</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(precios).map(([categoria, datos]) => (
                        <tr key={categoria}>
                          <td>{categoria.replace("_", " ")}</td>
                          <td>{datos.rango.desde} - {datos.rango.hasta}</td>
                          <td>${datos.vip.toFixed(2)}</td>
                          <td>${datos.general.toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                {error && <div className="alert alert-danger">{error}</div>}
                <table className="table table-bordered text-center align-middle">
                  <thead className="table-light">
                    <tr>
                      <th>Edad</th>
                      <th>Tipo de Entrada</th>
                      <th>Precio</th>
                    </tr>
                  </thead>
                  <tbody>
                    {entradas.map((entrada, i) => (
                      <tr key={i}>
                        <td style={{ width: "30%" }}>
                          <input
                            type="number"
                            className="form-control text-center"
                            min="0"
                            value={entrada.edad}
                            onChange={(e) =>
                              handleChange(i, "edad", e.target.value)
                            }
                          />
                        </td>
                        <td style={{ width: "40%" }}>
                          <div className="d-flex justify-content-center gap-3">
                            <div className="form-check">
                              <input
                                className="form-check-input"
                                type="radio"
                                name={`tipo${i}`}
                                id={`vip${i}`}
                                value="vip"
                                checked={entrada.tipo === "vip"}
                                onChange={(e) =>
                                  handleChange(i, "tipo", e.target.value)
                                }
                              />
                              <label
                                className="form-check-label"
                                htmlFor={`vip${i}`}
                              >
                                VIP
                              </label>
                            </div>
                            <div className="form-check">
                              <input
                                className="form-check-input"
                                type="radio"
                                name={`tipo${i}`}
                                id={`general${i}`}
                                value="general"
                                checked={entrada.tipo === "general"}
                                onChange={(e) =>
                                  handleChange(i, "tipo", e.target.value)
                                }
                              />
                              <label
                                className="form-check-label"
                                htmlFor={`general${i}`}
                              >
                                General
                              </label>
                            </div>
                          </div>
                        </td>
                        <td style={{ width: "30%" }}>
                          ${(entrada.precio || 0).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <div
                  className="d-flex justify-content-end"
                  style={{ paddingRight: "2rem" }}
                >
                  <span className="fw-bold">
                    Total: $
                    {entradas
                      .reduce((acc, e) => acc + (e.precio || 0), 0)
                      .toFixed(2)}
                  </span>
                </div>
              </>
            ) : (
              <p>Cargando precios...</p>
            )}
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                setMostrar(false);
                onClose && onClose();
              }}
            >
              Cerrar
            </button>
            <button
              type="button"
              className="btn btn-success"
              onClick={handleConfirmar}
              disabled={loading}
            >
              {loading ? "Procesando..." : "Confirmar"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
