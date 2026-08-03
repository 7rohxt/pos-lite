import { useState, useEffect } from 'react'
import { apiFetch } from './api'

function NewSale() {
  const [products, setProducts] = useState([])
  const [qty, setQty] = useState({})          // { productId: quantity }
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function loadProducts() {
    apiFetch('/products').then(setProducts).catch((e) => setError(e.message))
  }
  useEffect(loadProducts, [])

  function setQuantity(id, value) {
    setQty({ ...qty, [id]: Number(value) })
  }

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
      setQty({})            // clear the inputs
      loadProducts()        // refresh stock
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div>
      <h2>New Sale</h2>
      {products.map((p) => (
        <div key={p.id}>
          {p.name} — ${p.price} ({p.stock} in stock){' '}
          <input
            type="number"
            min="0"
            value={qty[p.id] || ''}
            onChange={(e) => setQuantity(p.id, e.target.value)}
            style={{ width: 60 }}
          />
        </div>
      ))}
      <button onClick={submitSale}>Complete sale</button>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}

export default NewSale