import { ReactNode } from 'react'
import './layout.css'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <header className="layout-header">
        <div className="header-content">
          <h1>מחשבון מערכת סולארית</h1>
          <p className="text-sm text-neutral-600">תכנון וחישוב חומרים לפרויקטים סולאריים</p>
        </div>
      </header>

      <main className="layout-main">
        <div className="container">
          {children}
        </div>
      </main>

      <footer className="layout-footer">
        <p className="text-sm text-neutral-600">
          מחשבון מערכת סולארית © 2024
        </p>
      </footer>
    </div>
  )
}
