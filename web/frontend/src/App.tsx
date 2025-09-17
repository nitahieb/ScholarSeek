import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import NotFound from './pages/NotFound'
import ProtectedRoute from './components/ProtectedRoute'


function Logout(): React.JSX.Element {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  return <Navigate to="/login" />;
}

function RegisterAndLogout(): React.JSX.Element {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  return <Register />;
}


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/" element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        } />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>

  )
}

export default App
