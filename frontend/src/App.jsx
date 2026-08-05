import { useState, useEffect } from 'react'
import Login from './Login'
import NewSale from './NewSale'
import AdminPanel from './AdminPanel'
import { apiFetch, getToken, clearToken } from './api'
import ProductManager from './ProductManager'

function App() {
  const [loggedIn, setLoggedIn] = useState(Boolean(getToken()))
  const [user, setUser] = useState(null)

  useEffect(() => {
    if (loggedIn) apiFetch('/auth/me').then(setUser).catch(() => setUser(null))
    else setUser(null)
  }, [loggedIn])

  if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />

  return (
    <div className="app">
      <header className="app-header">
        <img className="logo" src="/logo.png" alt="" onError={(e) => (e.currentTarget.style.display = 'none')} />
        <h1>POS-Lite</h1>
        <span className="spacer" />
        {user && <span className="who">{user.username}{user.is_admin ? ' · admin' : ''}</span>}
        <button className="btn" onClick={() => { clearToken(); setLoggedIn(false) }}>Log out</button>
      </header>

      <NewSale />
      {user?.is_admin && <ProductManager />}
      {user?.is_admin && <AdminPanel />}
    </div>
  )
}

export default App