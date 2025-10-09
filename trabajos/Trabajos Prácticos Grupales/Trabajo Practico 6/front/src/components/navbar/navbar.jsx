import React from "react";
import logo from "../../assets/dale.png"; // ajustá la ruta según la ubicación real del archivo

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg fixed-top" style={{backgroundColor:"#C6E5B1"}}>
      <div className="container-fluid justify-content-center">
        <a className="navbar-brand mx-auto" href="#">
          <img
            src={logo}
            alt="Logo"
            style={{
              height: "8vh", // usa unidades relativas
              objectFit: "contain"
            }}
          />
        </a>
      </div>
    </nav>
  );
};

export default Navbar;
