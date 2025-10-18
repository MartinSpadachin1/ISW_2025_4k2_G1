import React, { useState } from 'react';
import api from '../../services/api';
import { useToast } from '../common/ToastContext';

function formatCard(value = '') {
  const v = value.replace(/\D/g, '').slice(0, 16);
  return v.replace(/(.{4})/g, '$1 ').trim();
}

function unformatCard(value = '') {
  return value.replace(/\D/g, '').slice(0, 16);
}

export default function ModalPago({ idReserva, monto = null, onClose }) {
  const [numero, setNumero] = useState('');
  const [cvv, setCvv] = useState('');
  const [vencimiento, setVencimiento] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const toast = useToast();

  const tarjetasPrueba = [
    { label: 'Visa test', numero: '4111 1111 1111 1111', cvv: '123', venc: '2030-12-31' },
    { label: 'Master test', numero: '5555 5555 5555 4444', cvv: '321', venc: '2028-06-30' },
  ];

  const handlePagar = async () => {
    setError(null);
    if (!numero || !cvv || !vencimiento) {
      setError('Completá todos los campos de la tarjeta');
      return;
    }
    try {
      setLoading(true);
      // Enviar el número sin espacios
      const payload = {
        id_reserva: idReserva,
        numero_tarjeta: numero.replace(/\s+/g, ''),
        cvv,
        fecha_expiracion: vencimiento,
      };
  const res = await api.procesarPago(payload);
  toast.show(res?.message || 'Pago simulado con éxito');
  onClose && onClose({ success: true, reserva_id: idReserva });
    } catch (err) {
      setError(err.detail || err.message || 'Error procesando el pago');
    } finally {
      setLoading(false);
    }
  };

  function detectBrand(cardNumber) {
    const n = cardNumber.replace(/\D/g, '');
    if (n.startsWith('4')) return 'VISA';
    if (n.startsWith('5')) return 'MASTERCARD';
    if (n.startsWith('37') || n.startsWith('34')) return 'AMEX';
    return null;
  }

  function formatCurrency(val) {
    if (val == null) return '';
    return Number(val).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
  }

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-md">
        <div className="modal-content" style={{ overflow: 'hidden' }}>
          <div style={{ background: '#009ee3', padding: '12px 16px', color: 'white' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <strong>Pasarela de pago (Mercado Pago)</strong>
              <small style={{ opacity: 0.9 }}>{idReserva ? `Reserva #${idReserva}` : ''}</small>
            </div>
          </div>
          <div className="modal-body">
            {error && <div className="alert alert-danger">{error}</div>}

            <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start', flexWrap: 'wrap' }}>
              <div style={{ flex: '1 1 260px' }}>
                <div style={{ background: '#f6fbff', border: '1px solid #e6f2fb', padding: '12px', borderRadius: 8, marginBottom: 12 }}>
                  <div style={{ fontSize: 12, color: '#666' }}>Monto a pagar</div>
                  <div style={{ fontSize: 20, fontWeight: 700, marginTop: 6 }}>{formatCurrency(monto)}</div>
                </div>

                <label className="form-label">Tarjetas de prueba</label>
                <div className="d-flex gap-2 mb-3">
                  {tarjetasPrueba.map((t, i) => (
                    <button key={i} type="button" className="btn btn-outline-primary btn-sm" onClick={() => { setNumero(t.numero); setCvv(t.cvv); setVencimiento(t.venc); setError(null); }}>
                      {t.label}
                    </button>
                  ))}
                </div>

                <div style={{ position: 'relative' }}>
                  <label className="form-label">Número de tarjeta</label>
                  <input
                    className="form-control"
                    value={formatCard(numero)}
                    onChange={e => setNumero(unformatCard(e.target.value))}
                    placeholder="1234 5678 1234 5678"
                    inputMode="numeric"
                  />
                  <div style={{ position: 'absolute', right: 12, top: 34, fontSize: 12, color: '#666' }}>{detectBrand(numero) || ''}</div>
                </div>
              </div>

              <div style={{ width: 220 }}>
                <label className="form-label">CVV</label>
                <input className="form-control mb-2" value={cvv} onChange={e => setCvv(e.target.value.replace(/\D/g, ''))} placeholder="123" inputMode="numeric" />
                <label className="form-label">Vencimiento</label>
                <input className="form-control" value={vencimiento} onChange={e => setVencimiento(e.target.value)} placeholder="YYYY-MM-DD" />
              </div>
            </div>
          </div>
          <div className="modal-footer d-flex flex-column align-items-stretch gap-2">
            <div style={{ fontSize: 12, color: '#666' }}>Tus datos estarán seguros</div>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
              <button className="btn btn-outline-secondary" onClick={() => onClose && onClose()}>Cancelar</button>
              <button className="btn btn-primary" style={{ background: '#00a0df', borderColor: '#00a0df' }} onClick={handlePagar} disabled={loading}>{loading ? 'Procesando...' : `Pagar ${formatCurrency(monto)}`}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

