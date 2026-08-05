import { useState, useEffect } from 'react'
import { apiFetch } from './api'

function NewSale() {
  const [products, setProducts] = useState([])
  const [qty, setQty] = useState({})
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function loadProducts() {
    apiFetch('/products').then(setProducts).catch((e) => setError(e.message))
  }
  useEffect(loadProducts, [])

  function setQuantity(id, value) { setQty({ ...qty, [id]: Number(value) }) }

  async function submitSale() {
    setMessage(''); setError('')
    const items = Object.entries(qty)
      .filter(([, q]) => q > 0)
      .map(([product_id, quantity]) => ({ product_id: Number(product_id), quantity }))
    if (items.length === 0) { setError('Add at least one item.'); return }
    try {
      const sale = await apiFetch('/sales', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items }),
      })
      setMessage(`Sale #${sale.id} complete — total $${sale.total}`)
      setQty({})
      loadProducts()
    } catch (e) { setError(e.message) }
  }

  return (
    <div className="card">
      <h2>New Sale</h2>
      <div className="product-grid">
        {products.map((p) => (
          <div className="product-card" key={p.id}>
            <div className="product-img">
              <img
                src={`/products/${p.id}.png`}
                alt={p.name}
                onError={(e) => (e.currentTarget.style.display = 'none')}
              />
            </div>
            <div className="product-info">
              <div className="product-name">{p.name}</div>
              <div className="product-meta">${p.price} · {p.stock} left</div>
              <input
                className="field qty"
                type="number"
                min="0"
                placeholder="0"
                value={qty[p.id] || ''}
                onChange={(e) => setQuantity(p.id, e.target.value)}
              />
            </div>
          </div>
        ))}
      </div>
      <button className="btn btn-primary" onClick={submitSale} style={{ marginTop: 16 }}>
        Complete sale
      </button>
      {message && <p className="msg-ok">{message}</p>}
      {error && <p className="msg-error">{error}</p>}
    </div>
  )
}

export default NewSale