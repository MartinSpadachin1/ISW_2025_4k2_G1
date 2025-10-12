import React, { createContext, useContext, useState, useCallback } from 'react';

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const show = useCallback((message, options = {}) => {
    const id = Date.now() + Math.random();
    const toast = { id, message, ...options };
    setToasts(t => [...t, toast]);
    if (!options.sticky) {
      const timeout = options.duration || 4000;
      setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), timeout);
    }
    return id;
  }, []);

  const hide = useCallback((id) => setToasts(t => t.filter(x => x.id !== id)), []);

  return (
    <ToastContext.Provider value={{ show, hide }}>
      {children}
      <div aria-live="polite" aria-atomic="true" style={{ position: 'fixed', top: 12, right: 12, zIndex: 1050 }}>
        {toasts.map(t => (
          <div key={t.id} className="toast show mb-2" role="alert" aria-live="assertive" aria-atomic="true">
            <div className="toast-body">{t.message}</div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within ToastProvider');
  return ctx;
}

export default ToastContext;
