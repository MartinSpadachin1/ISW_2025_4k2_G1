// Login.jsx
import React, { useState } from "react";
import Claudia from '../../assets/claudia.png';
import { Link, useNavigate } from 'react-router-dom';
import api, { saveToken } from '../../services/api';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  return (
    <div
      className="w-100 d-flex align-items-center justify-content-center p-3 p-md-4"
      style={{
        minHeight: '100vh',
        paddingTop: '80px',    // ≈ altura del navbar
        paddingBottom: '80px', // ≈ altura del footer
        boxSizing: 'border-box',
      }}
    >
      {/* Contenedor principal: 1/3 imagen + 2/3 formulario en desktop */}
      <div className="row w-100 g-0" style={{ maxWidth: '1200px' }}>
        {/* Imagen: solo en desktop */}
        <div className="col-12 col-md-4 d-none d-md-flex">
          <img
            src={Claudia}
            alt="Claudia la leona en el parque"
            className="w-100 h-100"
            style={{
              objectFit: 'cover',
              maxHeight: '80vh',
              borderRadius: '12px 0 0 12px',
            }}
          />
        </div>

        {/* Formulario */}
        <div className="col-12 col-md-8 d-flex">
          <div
            className="card shadow w-100 border-0 rounded-3"
            style={{ backgroundColor: 'white' }}
          >
            <div className="card-body p-4 p-md-5 d-flex flex-column">
              <h3 className="card-title text-center mb-4">Iniciar Sesión</h3>

              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  id="email"
                  className="form-control"
                  placeholder="Ingresá tu email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div className="mb-3">
                <label htmlFor="password" className="form-label">Contraseña</label>
                <div style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                    id="password"
                    className="form-control"
                    placeholder="Ingresá tu contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ paddingRight: '70px' }}
                  />
                  <span
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '15px',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      fontSize: '0.9rem',
                      color: '#3da35d',
                      fontWeight: 600,
                      cursor: 'pointer',
                      userSelect: 'none',
                      background: 'white',
                      paddingLeft: '4px',
                    }}
                  >
                    {showPassword ? 'Ocultar' : 'Mostrar'}
                  </span>
                </div>
              </div>

              {error && <div className="alert alert-danger">{error}</div>}

              {/* Nuevo texto + enlace */}
              <div className="text-center mb-3 mt-auto">
                <p className="mb-1" style={{ fontSize: '0.95rem', color: '#555' }}>
                  ¿Todavía no tenés una cuenta?
                </p>
                <small>
                  <Link to="/registrarse" className="text-decoration-none fw-semibold" style={{ color: '#3da35d' }}>
                    Registrarse
                  </Link>
                </small>
              </div>

              <div className="d-flex justify-content-between">
                <button className="btn btn-secondary" onClick={() => { setEmail(''); setPassword(''); setError(null); }}>Cancelar</button>
                <button className="btn btn-success" onClick={async () => {
                  setError(null);
                  setLoading(true);
                  try {
                    const res = await api.login(email, password);
                    if (res && res.access_token) {
                      saveToken(res.access_token);
                      navigate('/');
                    } else {
                      setError('Respuesta inválida del servidor');
                    }
                  } catch (err) {
                    setError(err.detail || err.message || 'Error en login');
                  } finally { setLoading(false); }
                }} disabled={loading}>{loading ? 'Ingresando...' : 'Ingresar'}</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}