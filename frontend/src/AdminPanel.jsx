import { useState, useEffect } from 'react'
import { apiFetch } from './api'

function AdminPanel() {
  const [report, setReport] = useState(null)
  const [lowStock, setLowStock] = useState([])
  const [sales, setSales] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      apiFetch('/admin/reports/today'),
      apiFetch('/admin/reports/low-stock?threshold=5'),
      apiFetch('/admin/sales'),
    ])
      .then(([r, low, s]) => { setReport(r); setLowStock(low); setSales(s) })
      .catch((e) => setError(e.message))
  }, [])

  if (error) return <p style={{ color: 'red' }}>Admin: {error}</p>

  return (
    <div>
      <h2>Admin</h2>

      {report && <p>Today: {report.sales_count} sales, total ${report.total_revenue}</p>}

      <h3>Low stock (≤ 5)</h3>
      {lowStock.length === 0
        ? <p>None.</p>
        : <ul>{lowStock.map((p) => <li key={p.id}>{p.name} — {p.stock} left</li>)}</ul>}

      <h3>All sales</h3>
      {sales.length === 0
        ? <p>No sales yet.</p>
        : <ul>{sales.map((s) => (
            <li key={s.id}>
              Sale #{s.id} — ${s.total} — cashier {s.cashier_id} — {s.items.length} item(s)
            </li>
          ))}</ul>}
    </div>
  )
}

export default AdminPanel