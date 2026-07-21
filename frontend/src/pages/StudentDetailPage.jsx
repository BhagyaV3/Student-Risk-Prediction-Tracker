import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import api from '../api/client'

const RISK_CLASS = { low: 'badge-low', medium: 'badge-medium', high: 'badge-high' }

export default function StudentDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [student, setStudent] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api.get(`/students/${id}`),
      api.get(`/students/${id}/metrics/latest`).catch(() => ({ data: null })),
      api.get(`/students/${id}/predictions/latest`).catch(() => ({ data: null })),
    ])
      .then(([studentRes, metricsRes, predRes]) => {
        setStudent(studentRes.data)
        setMetrics(metricsRes.data)
        setPrediction(predRes.data)
      })
      .catch(() => setError('Failed to load student data.'))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="loading">Loading…</div>
  if (error)   return <div className="alert alert-error">{error}</div>
  if (!student) return null

  return (
    <div>
      <div className="page-header">
        <div>
          <Link to="/students" className="back-link">← All Students</Link>
          <h1>{student.first_name} {student.last_name}</h1>
        </div>
        <button className="btn btn-secondary" onClick={() => navigate(`/students/${id}/edit`)}>
          Edit
        </button>
      </div>

      <div className="detail-grid">
        {/* ── Student info ───────────────────────────── */}
        <div className="card">
          <h2>Student Info</h2>
          <dl className="detail-list">
            <dt>Email</dt>
            <dd>{student.email}</dd>
            <dt>Enrolled</dt>
            <dd>{new Date(student.enrollment_date).toLocaleDateString()}</dd>
            <dt>Added</dt>
            <dd>{new Date(student.created_at).toLocaleDateString()}</dd>
          </dl>
        </div>

        {/* ── Risk prediction ────────────────────────── */}
        <div className="card">
          <h2>Risk Prediction</h2>
          {prediction ? (
            <>
              <div className="prediction-summary">
                <span className={`badge ${RISK_CLASS[prediction.risk_level]}`}>
                  {prediction.risk_level.toUpperCase()} RISK
                </span>
                <div className="risk-score-bar">
                  <div
                    className="risk-score-fill"
                    style={{ width: `${prediction.risk_score * 100}%` }}
                  />
                </div>
                <span className="text-muted" style={{ fontSize: '0.83rem' }}>
                  Score: {(prediction.risk_score * 100).toFixed(1)}%
                  &nbsp;·&nbsp;
                  Confidence: {(prediction.confidence * 100).toFixed(1)}%
                </span>
              </div>

              <h3>Contributing Factors</h3>
              <table className="table table-compact">
                <tbody>
                  {Object.entries(prediction.feature_importance)
                    .sort(([, a], [, b]) => b - a)
                    .map(([feature, value]) => (
                      <tr key={feature}>
                        <td style={{ textTransform: 'capitalize' }}>
                          {feature.replace(/_/g, ' ')}
                        </td>
                        <td style={{ color: 'var(--text-muted)', textAlign: 'right' }}>
                          {(value * 100).toFixed(1)}%
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </>
          ) : (
            <div className="empty-state">
              No prediction yet.
            </div>
          )}
        </div>

        {/* ── Latest metrics ─────────────────────────── */}
        <div className="card">
          <h2>Latest Metrics</h2>
          {metrics ? (
            <dl className="detail-list">
              <dt>Attendance</dt>
              <dd>{metrics.attendance_percentage}%</dd>
              <dt>GPA</dt>
              <dd>{metrics.gpa}</dd>
              <dt>Assignments</dt>
              <dd>{metrics.assignment_completion_percentage}%</dd>
              <dt>Test Score Avg</dt>
              <dd>{metrics.test_score_average}</dd>
              <dt>Behavior Score</dt>
              <dd>{metrics.behavior_score}</dd>
              <dt>Recorded</dt>
              <dd>{new Date(metrics.recorded_date).toLocaleDateString()}</dd>
            </dl>
          ) : (
            <div className="empty-state">No metrics recorded yet.</div>
          )}
        </div>
      </div>
    </div>
  )
}
