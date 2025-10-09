import React, { useEffect, useState } from "react";

export default function ModalComprarEntradas({ cantidad, onClose }) {
  const [precios, setPrecios] = useState(null);
  const [entradas, setEntradas] = useState([]);
  const [mostrar, setMostrar] = useState(true);

  useEffect(() => {
    const obtenerPrecios = async () => {
      try {
        const PRECIO_VIP = 10000;
        const PRECIO_GENERAL = 6000;

        const data = {
          bebes: { rango: { desde: 0, hasta: 3 }, vip: 0, general: 0 },
          niños: {
            rango: { desde: 4, hasta: 15 },
            vip: PRECIO_VIP * 0.5,
            general: PRECIO_GENERAL * 0.5,
          },
          adultos: {
            rango: { desde: 16, hasta: 65 },
            vip: PRECIO_VIP,
            general: PRECIO_GENERAL,
          },
          adulto_mayor: {
            rango: { desde: 66, hasta: 120 },
            vip: PRECIO_VIP * 0.5,
            general: PRECIO_GENERAL * 0.5,
          },
        };

        setPrecios(data);
      } catch (err) {
        console.error("Error al obtener precios:", err);
      }
    };

    obtenerPrecios();

    const filasIniciales = Array.from({ length: cantidad }, () => ({
      edad: "",
      tipo: "",
      precio: 0,
    }));
    setEntradas(filasIniciales);
  }, [cantidad]);

  const calcularPrecio = (edad, tipo) => {
    if (!precios || !edad || !tipo) return 0;
    edad = Number(edad);

    const { bebes, niños, adultos, adulto_mayor } = precios;

    if (edad >= bebes.rango.desde && edad <= bebes.rango.hasta)
      return bebes[tipo] || 0;
    if (edad >= niños.rango.desde && edad <= niños.rango.hasta)
      return niños[tipo] || 0;
    if (edad >= adultos.rango.desde && edad <= adultos.rango.hasta)
      return adultos[tipo] || 0;
    if (edad >= adulto_mayor.rango.desde && edad <= adulto_mayor.rango.hasta)
      return adulto_mayor[tipo] || 0;

    return 0;
  };

  const handleChange = (index, field, value) => {
    const nuevasEntradas = [...entradas];
    if (field === "edad" && value < 1) return; // Evitar edades negativas o 0

    nuevasEntradas[index][field] = value;

    // Recalcular precio cada vez que cambia edad o tipo
    const edad = nuevasEntradas[index].edad;
    const tipo = nuevasEntradas[index].tipo;
    nuevasEntradas[index].precio = calcularPrecio(edad, tipo);

    setEntradas(nuevasEntradas);
  };

  if (!mostrar) return null;

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
                      {/* Edad */}
                      <td style={{ width: "30%" }}>
                        <input
                          type="number"
                          className="form-control text-center"
                          min="1"
                          value={entrada.edad}
                          onChange={(e) =>
                            handleChange(i, "edad", e.target.value)
                          }
                        />
                      </td>

                      {/* Tipo de Entrada (botones) */}
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

                      {/* Precio */}
                      <td style={{ width: "30%" }}>
                        ${entrada.precio.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
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
            <button type="button" className="btn btn-success">
              Confirmar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
