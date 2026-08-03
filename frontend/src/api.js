const BASE_URL = "http://127.0.0.1:8000/api"

// --- token storage (in the browser's localStorage, survives refresh) ---
export function getToken() {
  return localStorage.getItem("token")
}
export function setToken(token) {
  localStorage.setItem("token", token)
}
export function clearToken() {
  localStorage.removeItem("token")
}

// --- log in: OAuth2 password flow expects FORM data, not JSON ---
export async function login(username, password) {
  const body = new URLSearchParams()
  body.append("username", username)
  body.append("password", password)

  const res = await fetch(`${BASE_URL}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || "Login failed")
  }

  const data = await res.json()
  setToken(data.access_token)   // save the JWT
  return data
}

// --- authenticated request helper: auto-attaches the Bearer token ---
export async function apiFetch(path, options = {}) {
  const token = getToken()
  const headers = { ...(options.headers || {}) }
  if (token) headers["Authorization"] = `Bearer ${token}`

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Request failed (${res.status})`)
  }
  if (res.status === 204) return null   // DELETE returns no body
  return res.json()
}