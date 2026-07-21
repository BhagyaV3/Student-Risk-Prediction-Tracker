import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-wrapper">
      <header className="app-header">
        <div className="header-brand">
          <Link to="/students">📊 Student Risk Tracker</Link>
        </div>
        <nav className="header-nav">
          <Link to="/students">Students</Link>
          {user && (
            <span className="header-user">
              {user.username}
              <button className="btn btn-ghost btn-sm" onClick={handleLogout}>
                Logout
              </button>
            </span>
          )}
        </nav>
      </header>
      <main className="app-main">{children}</main>
    </div>
  )
}
