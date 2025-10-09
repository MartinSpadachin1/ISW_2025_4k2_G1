import './App.css';
import Navbar from './components/navbar/navbar';
import Login from './components/login/login';
import Footer from './components/Footer/Footer';
import CompraEntradas from './components/compraEntradas/ComprarEntradas'; 
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './components/landingPage/landingPage';
import FooterBanner from './components/Footer/FooterBanner/FooterBanner';

function App() {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          {/* Ruta del Landing Page */}
          <Route path='/' element={<LandingPage />} />

          {/* Ruta para hacer el Login */}
          <Route path="/iniciar-sesion" element={<Login />} />

          {/* Ruta para comprar entradas */}
          <Route path="/comprar-entradas" element={<CompraEntradas />} />
        </Routes>
      </BrowserRouter>

      {/* <FooterBanner /> */}
      <Footer />
    </>
  );
}

export default App;
