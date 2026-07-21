import { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api/client'

const PAGE_SIZE = 10

export default function StudentsPage() {
  const [students, setStudents] = useState([])
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(0)
  const [hasMore, setHasMore] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const fetchStudents = useCallback(async (pageIndex) => {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/students', {
        params: { skip: pageIndex * PAGE_SIZE, limit: PAGE_SIZE },
      })
      setStudents(res.data)
      setHasMore(res.data.length === PAGE_SIZE)
    } catch {
      setError('Failed to load students.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchStudents(page)
  }, [page, fetchStudents])

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Delete ${name}? This cannot be undone.`)) return
    try {
      await api.delete(`/students/${id}`)
      setStudents((prev) => prev.filter((s) => s.id !== id))
    } catch {
      alert('Failed to delete student. Please try again.')
    }
  }

  const filtered = students.filter((s) =>
    `${s.first_name} ${s.last_name}`.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div>
      <div className="page-header">
        <h1>Students</h1>
        <button className="btn btn-primary" onClick={() => navigate('/students/new')}>
          + Add Student
        </button>
      </div>

      <div className="card">
        <div className="card-toolbar">
          <input
            type="search"
            className="form-control search-input"
            placeholder="Search by name…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="loading">Loading students…</div>
        ) : error ? (
          <div className="alert alert-error">{error}</div>
        ) : filtered.length === 0 ? (
          <div className="empty-state">
            {search
              ? 'No students match your search.'
              : 'No students yet. Click "+ Add Student" to get started.'}
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Enrolled</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((student) => (
                <tr key={student.id}>
                  <td>
                    <Link to={`/students/${student.id}`}>
                      {student.first_name} {student.last_name}
                    </Link>
                  </td>
                  <td>{student.email}</td>
                  <td>
                    {new Date(student.enrollment_date).toLocaleDateString()}
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button
                        className="btn btn-sm btn-secondary"
                        onClick={() => navigate(`/students/${student.id}`)}
                      >
                        View
                      </button>
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() =>
                          handleDelete(
                            student.id,
                            `${student.first_name} ${student.last_name}`
                          )
                        }
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {!loading && !error && (
          <div className="pagination">
            <button
              className="btn btn-sm btn-secondary"
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={page === 0}
            >
              ← Prev
            </button>
            <span>Page {page + 1}</span>
            <button
              className="btn btn-sm btn-secondary"
              onClick={() => setPage((p) => p + 1)}
              disabled={!hasMore}
            >
              Next →
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
