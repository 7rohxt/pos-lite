import { useState, useEffect } from 'react'
import { apiFetch } from './api'

function ProductList() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch('/products')
      .then((data) => setProducts(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])   // [] = run once, when the component first mounts

  if (loading) return <p>Loading products…</p>
  if (error) return <p style={{ color: 'red' }}>{error}</p>

  return (
    <div>
      <h2>Products</h2>
      {products.length === 0 ? (
        <p>No products yet.</p>
      ) : (
        <ul>
          {products.map((p) => (
            <li key={p.id}>
              {p.name} — ${p.price} ({p.stock} in stock)
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default ProductList