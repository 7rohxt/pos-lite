import { useState } from 'react'
import { login } from './api'

function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      await login(username, password)
      onLogin()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="login-wrap">
      <div className="login-card">
        <h1>POS-Lite</h1>
        <form onSubmit={handleSubmit}>
          <input className="field" type="text" placeholder="Username"
                 value={username} onChange={(e) => setUsername(e.target.value)} />
          <input className="field" type="password" placeholder="Password"
                 value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="btn btn-primary" type="submit" style={{ width: '100%' }}>Log in</button>
        </form>
        {error && <p className="msg-error">{error}</p>}
      </div>
    </div>
  )
}

export default Login