import React, { useEffect, useState } from "react";
import api from '../../services/api';

export default function ModalComprarEntradas({ cantidad, fecha, metodoPago, onClose }) {
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
        console.error('No se pudieron obtener edades desde el backend, usando valores por defecto', err);
        // fallback a valores hardcodeados
        const PRECIO_VIP = 10000;
        const PRECIO_GENERAL = 6000;
        setPrecios({
          bebes: { rango: { desde: 0, hasta: 3 }, vip: 0, general: 0 },
          niños: { rango: { desde: 4, hasta: 15 }, vip: PRECIO_VIP * 0.5, general: PRECIO_GENERAL * 0.5 },
          adultos: { rango: { desde: 16, hasta: 65 }, vip: PRECIO_VIP, general: PRECIO_GENERAL },
          adulto_mayor: { rango: { desde: 66, hasta: 120 }, vip: PRECIO_VIP * 0.5, general: PRECIO_GENERAL * 0.5 },
        });
      }
    };

    init();

    const filasIniciales = Array.from({ length: cantidad }, () => ({ edad: "", tipo: "", precio: 0 }));
    setEntradas(filasIniciales);
  }, [cantidad]);

  const calcularPrecioLocal = (edad, tipo) => {
    if (!precios || !edad || !tipo) return 0;
    edad = Number(edad);
    const { bebes, niños, adultos, adulto_mayor } = precios;
    if (edad >= bebes.rango.desde && edad <= bebes.rango.hasta) return bebes[tipo] || 0;
    if (edad >= niños.rango.desde && edad <= niños.rango.hasta) return niños[tipo] || 0;
    if (edad >= adultos.rango.desde && edad <= adultos.rango.hasta) return adultos[tipo] || 0;
    if (edad >= adulto_mayor.rango.desde && edad <= adulto_mayor.rango.hasta) return adulto_mayor[tipo] || 0;
    return 0;
  };

  const handleChange = (index, field, value) => {
    const nuevasEntradas = [...entradas];
    if (field === "edad" && value < 0) return;
    nuevasEntradas[index][field] = value;
    // recalcular precio localmente
    const edad = nuevasEntradas[index].edad;
    const tipo = nuevasEntradas[index].tipo;
    nuevasEntradas[index].precio = calcularPrecioLocal(edad, tipo);
    setEntradas(nuevasEntradas);
  };

  if (!mostrar) return null;

  const calcularMontoTotalBackend = async () => {
    setError(null);
    setLoading(true);
    try {
      const visitantes = entradas.map(e => ({ edad: Number(e.edad), tipo_entrada: (e.tipo === 'vip' ? 'vip' : 'general') }));
      const res = await api.montoTotal(visitantes);
      setLoading(false);
      return res;
    } catch (err) {
      setLoading(false);
      setError(err.detail || err.message || 'Error calculando monto total');
      throw err;
    }
  };

  const handleConfirmar = async () => {
    setError(null);
    // validaciones simples
    for (let i = 0; i < entradas.length; i++) {
      if (!entradas[i].edad || !entradas[i].tipo) { setError('Completá todas las edades y tipos'); return; }
    }

    try {
      const visitantes = entradas.map(e => ({ edad: Number(e.edad), tipo_entrada: (e.tipo === 'vip' ? 'vip' : 'general') }));
      const payload = { token: localStorage.getItem('access_token') || null, fecha: fecha || null, visitantes, forma_pago: metodoPago || null };
      setLoading(true);
      // solicitar validación al backend
      const resVal = await api.validarCompra(payload);
      setLoading(false);
      // mostrar resultado y cerrar
      alert(resVal?.message || 'Compra validada correctamente');
      setMostrar(false);
      onClose && onClose();
    } catch (err) {
      setLoading(false);
      setError(err.detail || err.message || 'Error validando compra');
    }
  };

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: "rgba(0,0,0,0.5)", transition: "all 0.3s ease" }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Configurar Entradas</h5>
            <button type="button" className="btn-close" onClick={() => { setMostrar(false); onClose && onClose(); }}></button>
          </div>

          <div className="modal-body">
            {precios ? (
              <>
                {error && <div className="alert alert-danger">{error}</div>}
                <table className="table table-bordered text-center align-middle">
                  <thead className="table-light">
                    <tr><th>Edad</th><th>Tipo de Entrada</th><th>Precio</th></tr>
                  </thead>
                  <tbody>
                    {entradas.map((entrada, i) => (
                      <tr key={i}>
                        <td style={{ width: "30%" }}>
                          <input type="number" className="form-control text-center" min="0" value={entrada.edad} onChange={(e) => handleChange(i, 'edad', e.target.value)} />
                        </td>
                        <td style={{ width: "40%" }}>
                          <div className="d-flex justify-content-center gap-3">
                            <div className="form-check">
                              <input className="form-check-input" type="radio" name={`tipo${i}`} id={`vip${i}`} value="vip" checked={entrada.tipo === 'vip'} onChange={(e) => handleChange(i, 'tipo', e.target.value)} />
                              <label className="form-check-label" htmlFor={`vip${i}`}>VIP</label>
                            </div>
                            <div className="form-check">
                              <input className="form-check-input" type="radio" name={`tipo${i}`} id={`general${i}`} value="general" checked={entrada.tipo === 'general'} onChange={(e) => handleChange(i, 'tipo', e.target.value)} />
                              <label className="form-check-label" htmlFor={`general${i}`}>General</label>
                            </div>
                          </div>
                        </td>
                        <td style={{ width: "30%" }}>${(entrada.precio || 0).toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <div className="d-flex justify-content-end gap-2">
                  <button className="btn btn-outline-secondary" onClick={async () => {
                    try {
                      const res = await calcularMontoTotalBackend();
                      alert('Monto total: ' + (res.total || JSON.stringify(res)));
                    } catch (err) { /* error ya seteado */ }
                  }}>Calcular monto (backend)</button>
                </div>
              </>
            ) : (
              <p>Cargando precios...</p>
            )}
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={() => { setMostrar(false); onClose && onClose(); }}>Cerrar</button>
            <button type="button" className="btn btn-success" onClick={handleConfirmar} disabled={loading}>{loading ? 'Procesando...' : 'Confirmar'}</button>
          </div>
        </div>
      </div>
    </div>
  );
}
