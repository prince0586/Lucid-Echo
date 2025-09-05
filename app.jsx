import React from 'react'
import { createRoot } from 'https://unpkg.com/react-dom@18/esm/react-dom.production.min.js'

function App() {
  const [dream, setDream] = React.useState('')
  const [result, setResult] = React.useState(null)
  const [loading, setLoading] = React.useState(false)
  const [history, setHistory] = React.useState(null)
  const [password, setPassword] = React.useState('')

  async function submitDream() {
    setLoading(true)
    setResult(null)
    try {
      const res = await fetch('/interpret', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Memory-Password': password },
        body: JSON.stringify({ text: dream })
      })
      const data = await res.json()
      setResult(data)
      setDream('')
      loadHistory(password)
    } catch (e) {
      setResult({ error: e.message })
    } finally {
      setLoading(false)
    }
  }

  async function loadHistory(pw = password) {
    try {
      const res = await fetch('/history', { headers: { 'X-Memory-Password': pw } })
      const data = await res.json()
      setHistory(data)
    } catch (e) {
      setHistory({ error: e.message })
    }
  }

  React.useEffect(() => {
    // no-op
  }, [])

  return (
    React.createElement('div', { className: 'bg-white rounded-xl shadow p-6' },
      React.createElement('h1', { className: 'text-2xl font-bold mb-4' }, 'Lucid Echo — Dream Interpreter'),

      React.createElement('label', { className: 'block text-sm text-gray-600 mb-1' }, 'Memory Password (required)'),
      React.createElement('input', {
        className: 'w-full border rounded p-2 mb-3',
        type: 'password',
        value: password,
        onChange: e => setPassword(e.target.value),
        placeholder: 'Enter a local password to encrypt your dream memory'
      }),

      React.createElement('textarea', {
        className: 'w-full border rounded p-3 mb-3 h-40 focus:outline-none focus:ring',
        placeholder: 'Write your dream here...',
        value: dream,
        onChange: e => setDream(e.target.value)
      }),
      React.createElement('div', { className: 'flex gap-3 mb-4' },
        React.createElement('button', {
          className: 'px-4 py-2 bg-indigo-600 text-white rounded disabled:opacity-50',
          onClick: submitDream,
          disabled: loading || dream.trim() === '' || password.trim() === ''
        }, loading ? 'Interpreting…' : 'Interpret Dream'),
        React.createElement('button', {
          className: 'px-4 py-2 border rounded',
          onClick: () => loadHistory(password)
        }, 'Load History')
      ),
      result && React.createElement('div', { className: 'mt-4 p-4 bg-gray-50 rounded' },
        React.createElement('h2', { className: 'font-semibold mb-2' }, 'Result'),
        React.createElement('pre', { className: 'whitespace-pre-wrap' }, JSON.stringify(result, null, 2))
      ),
      history && React.createElement('div', { className: 'mt-6' },
        React.createElement('h2', { className: 'font-semibold mb-2' }, 'History Preview'),
        React.createElement('pre', { className: 'whitespace-pre-wrap max-h-64 overflow-auto bg-gray-100 p-3 rounded' }, JSON.stringify(history, null, 2))
      )
    )
  )
}

const container = document.getElementById('root')
createRoot(container).render(React.createElement(App))
