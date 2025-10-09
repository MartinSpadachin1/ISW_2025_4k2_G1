import './App.css';
import Navbar from './components/navbar/navbar';
import Login from './components/login/login';
import Registrar from './components/Registrar/Registrar';
import CompraEntradas from './components/compraEntradas/ComprarEntradas'; 
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './components/landingPage/landingPage';
import Footer from './components/Footer/Footer';
import QuienesSomos from './components/QuienesSomos/QuienesSomos';

function App() {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          {/* Ruta del Landing Page */}
          <Route path='/' element={<LandingPage />} />

          {/* Ruta para saber quiénes somos nosotros (los integrantes del Grupo 1 - Comisión 4k2) */}
          <Route path='/quienes-somos' element={<QuienesSomos/>}/>

          {/* Ruta para registrarse */}
          <Route path='/registrarse' element={<Registrar/>}></Route>

          {/* Ruta para hacer el Login */}
          <Route path="/iniciar-sesion" element={<Login />} />

          {/* Ruta para comprar entradas */}
          <Route path="/comprar-entradas" element={<CompraEntradas />} />


        </Routes>
        <Footer />
      </BrowserRouter>

    </>
  );
}

export default App;
