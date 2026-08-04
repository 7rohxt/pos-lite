import { useState, useEffect } from 'react'
import Login from './Login'
import NewSale from './NewSale'
import AdminPanel from './AdminPanel'
import { apiFetch, getToken, clearToken } from './api'

function App() {
  const [loggedIn, setLoggedIn] = useState(Boolean(getToken()))
  const [user, setUser] = useState(null)

  useEffect(() => {
    if (loggedIn) apiFetch('/auth/me').then(setUser).catch(() => setUser(null))
    else setUser(null)
  }, [loggedIn])

  if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />

  return (
    <div>
      <h1>POS-Lite</h1>
      {user && <p>Logged in as {user.username}{user.is_admin ? ' (admin)' : ''}</p>}
      <button onClick={() => { clearToken(); setLoggedIn(false) }}>Log out</button>
      <NewSale />
      {user?.is_admin && <AdminPanel />}
    </div>
  )
}

export default App