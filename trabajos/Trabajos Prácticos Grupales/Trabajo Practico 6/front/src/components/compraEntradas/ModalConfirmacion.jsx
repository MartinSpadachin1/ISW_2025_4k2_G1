import React from 'react';

export default function ModalConfirmacion({ idReserva = null, entradas = [], fecha = null, monto = null, metodoPago = null, onClose }) {
  const formattedDate = fecha ? (typeof fecha === 'string' ? fecha : new Date(fecha).toLocaleDateString()) : null;
  const formattedMonto = monto != null ? Number(monto).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' }) : null;
  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-md">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Compra confirmada</h5>
            <button type="button" className="btn-close" onClick={() => onClose && onClose()}></button>
          </div>
          <div className="modal-body">
            <p>La compra se procesó correctamente.</p>
            {idReserva && <p><strong>Reserva #</strong>{idReserva}</p>}
            {formattedDate && <p><strong>Fecha:</strong> {formattedDate}</p>}
            {entradas && entradas.length > 0 && (
              <div>
                <p><strong>Entradas:</strong></p>
                <ul>
                  {entradas.map((e, i) => (
                    <li key={i}>{e.tipo_entrada || e.tipo || 'Entrada'} - {e.edad ? `Edad: ${e.edad}` : ''} {e.precio ? ` - $${e.precio}` : ''}</li>
                  ))}
                </ul>
              </div>
            )}
            {metodoPago && <p><strong>Método de pago:</strong> {metodoPago}</p>}
            {formattedMonto && <p><strong>Total:</strong> {formattedMonto}</p>}
            <p>Se envió un correo con los detalles de la reserva.</p>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={() => onClose && onClose()}>Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  );
}
