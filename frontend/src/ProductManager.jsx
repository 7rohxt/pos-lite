import { useState, useEffect } from 'react'
import { apiFetch } from './api'

function ProductManager() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({ name: '', price: '', stock: '' })
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  function load() {
    apiFetch('/products').then(setProducts).catch((e) => setError(e.message))
  }
  useEffect(load, [])

  function setField(k, v) { setForm({ ...form, [k]: v }) }

  async function addProduct(e) {
    e.preventDefault()
    setError(''); setMessage('')
    try {
      await apiFetch('/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: form.name,
          price: Number(form.price),
          stock: Number(form.stock),
        }),
      })
      setMessage(`Added ${form.name}`)
      setForm({ name: '', price: '', stock: '' })
      load()
    } catch (e) { setError(e.message) }
  }

  async function remove(id) {
    setError(''); setMessage('')
    try {
      await apiFetch(`/products/${id}`, { method: 'DELETE' })
      load()
    } catch (e) { setError(e.message) }   // shows the 409 "in past sale(s)" message
  }

  return (
    <div className="card">
      <h2>Manage Products</h2>
      <form onSubmit={addProduct} className="product-form">
        <input className="field" placeholder="Name" value={form.name}
               onChange={(e) => setField('name', e.target.value)} />
        <input className="field" type="number" step="0.01" placeholder="Price" value={form.price}
               onChange={(e) => setField('price', e.target.value)} />
        <input className="field" type="number" placeholder="Stock" value={form.stock}
               onChange={(e) => setField('stock', e.target.value)} />
        <button className="btn btn-primary" type="submit">Add</button>
      </form>
      {message && <p className="msg-ok">{message}</p>}
      {error && <p className="msg-error">{error}</p>}

      <ul className="plain-list">
        {products.map((p) => (
          <li key={p.id} className="manage-row">
            <span>{p.name} — ${p.price} · {p.stock} in stock</span>
            <button className="btn" onClick={() => remove(p.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ProductManager