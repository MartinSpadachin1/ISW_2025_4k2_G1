import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './components/navbar/navbar'
import Login from './components/login/login'
import CompraEntradas from './components/compraEntradas/compraEntradas'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <Navbar/>
    { //<Login/>}
}
    <CompraEntradas/>
    </>
  )
}

export default App
