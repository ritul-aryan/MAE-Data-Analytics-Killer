import { useState } from 'react'
import axios from 'axios'
import PlotlyModule from 'react-plotly.js'

// 🔥 THE FIX: Safely unwrap the Plotly module so Vite and React don't fight
const Plot = (PlotlyModule as any).default || PlotlyModule

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [intent, setIntent] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file || !intent) {
      setError('Please provide both a CSV file and an intent.')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('intent', intent)

    try {
      // This checks if there is a live URL provided by Vercel; if not, it falls back to your local computer
      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(`${apiUrl}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || err.message || 'An error occurred.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
      <h1>🧠 Data Analytics Killer</h1>
      <p>Upload a messy CSV and tell the AI what you want to see.</p>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem', padding: '1.5rem', border: '1px solid #ccc', borderRadius: '8px' }}>
        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '0.5rem' }}>1. Upload Dataset (CSV)</label>
          <input type="file" accept=".csv" onChange={handleFileChange} />
        </div>

        <div>
          <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '0.5rem' }}>2. What is your intent?</label>
          <textarea
            rows={3}
            placeholder="e.g., Clean this data, drop invalid amounts, and show me a bar chart of sales by customer."
            value={intent}
            onChange={(e) => setIntent(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{ padding: '0.75rem', fontSize: '1rem', backgroundColor: loading ? '#ccc' : '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: loading ? 'not-allowed' : 'pointer' }}
        >
          {loading ? 'AI Agents are analyzing...' : 'Analyze Data'}
        </button>
      </form>

      {error && (
        <div style={{ color: 'red', padding: '1rem', border: '1px solid red', borderRadius: '4px', marginBottom: '1rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && result.status === 'success' && (
        <div style={{ borderTop: '2px solid #eee', paddingTop: '2rem' }}>
          <h2>📊 Analytical Summary</h2>
          <p style={{ lineHeight: '1.6', fontSize: '1.1rem', backgroundColor: '#f9f9f9', padding: '1rem', borderRadius: '4px' }}>
            {result.analytical_summary}
          </p>

          <h2 style={{ marginTop: '2rem' }}>📈 Visualization</h2>
          {result.plotly_config && result.plotly_config.data ? (
            <div style={{ width: '100%', overflowX: 'auto' }}>
              <Plot
                data={result.plotly_config.data}
                layout={{ ...result.plotly_config.layout, autosize: true }}
                useResizeHandler={true}
                style={{ width: '100%', height: '500px' }}
              />
            </div>
          ) : (
            <p style={{ color: 'orange' }}>The AI did not generate a valid chart for this query.</p>
          )}
        </div>
      )}
    </div>
  )
}

export default App