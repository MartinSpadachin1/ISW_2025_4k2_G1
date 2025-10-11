const BASE_URL = 'http://127.0.0.1:8000';

function handleResponse(res) {
  if (!res.ok) return res.json().then(err => { throw err; });
  // algunos endpoints podrían devolver json vacío
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) return res.json();
  return res.text();
}

function authHeaders() {
  const token = localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(email, password) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
}

export async function register(email, password) {
  const res = await fetch(`${BASE_URL}/user/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password}),
  });
  return handleResponse(res);
}

export async function obtenerEdades() {
  const res = await fetch(`${BASE_URL}/monto/edades/`, {
    method: 'GET',
    headers: { ...authHeaders() },
  });
  return handleResponse(res);
}

export async function montoTotal(visitantes) {
  const res = await fetch(`${BASE_URL}/monto/monto_total/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ visitantes }),
  });
  return handleResponse(res);
}

export async function montoUnico(edad, tipo_entrada) {
  const res = await fetch(`${BASE_URL}/monto/monto_unico`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ edad, tipo_entrada }),
  });
  return handleResponse(res);
}

export async function validarCompra(payload) {
  const res = await fetch(`${BASE_URL}/compra/validar_compra`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

// helper local
export function saveToken(token) { if (token) localStorage.setItem('access_token', token); }
export function clearToken() { localStorage.removeItem('access_token'); }

export default { login, register, obtenerEdades, montoTotal, montoUnico, validarCompra, saveToken, clearToken };
