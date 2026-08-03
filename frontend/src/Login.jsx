import { useState } from 'react'
import { login } from './api'

function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()          // stop the browser from reloading the page
    setError('')
    try {
      await login(username, password)
      onLogin()                 // tell the parent (App) we're now logged in
    } catch (err) {
      setError(err.message)     // show "Incorrect username or password"
    }
  }

  return (
    <div>
      <h1>POS-Lite — Login</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Log in</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}

export default Login