import { useState } from 'react'
import Login from './Login'
import { getToken, clearToken } from './api'

function App() {
  const [loggedIn, setLoggedIn] = useState(Boolean(getToken()))

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />
  }

  return (
    <div>
      <h1>POS-Lite</h1>
      <p>You're logged in. 🎉</p>
      <button onClick={() => { clearToken(); setLoggedIn(false) }}>
        Log out
      </button>
    </div>
  )
}

export default App