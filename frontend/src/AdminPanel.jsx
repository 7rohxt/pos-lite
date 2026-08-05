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

  return (
    <div className="card">
      <h2>Admin</h2>
      {error && <p className="msg-error">{error}</p>}

      {report && (
        <div className="stat-row">
          <div className="stat"><div className="num">{report.sales_count}</div><div className="label">Sales today</div></div>
          <div className="stat"><div className="num">${report.total_revenue}</div><div className="label">Revenue today</div></div>
          <div className="stat"><div className="num">{lowStock.length}</div><div className="label">Low-stock items</div></div>
        </div>
      )}

      <h3 style={{ marginTop: 20 }}>Low stock (≤ 5)</h3>
      {lowStock.length === 0 ? <p className="muted">None.</p> : (
        <ul className="plain-list">{lowStock.map((p) => <li key={p.id}>{p.name} — {p.stock} left</li>)}</ul>
      )}

      <h3 style={{ marginTop: 20 }}>All sales</h3>
      {sales.length === 0 ? <p className="muted">No sales yet.</p> : (
        <ul className="plain-list">
          {sales.map((s) => <li key={s.id}>Sale #{s.id} — ${s.total} — cashier {s.cashier_id} — {s.items.length} item(s)</li>)}
        </ul>
      )}
    </div>
  )
}

export default AdminPanel