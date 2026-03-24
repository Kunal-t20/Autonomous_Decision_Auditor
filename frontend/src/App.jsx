import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import './App.css'

const envApiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const API_BASE = envApiUrl.replace(/\/+$/, '')

function parseLines(text) {
  return text
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean)
}

function apiErrorMessage(data, fallback) {
  const d = data?.detail
  if (Array.isArray(d)) {
    return d.map((x) => x.msg || JSON.stringify(x)).join('; ') || fallback
  }
  if (typeof d === 'string') return d
  return fallback
}

async function postAudit(body) {
  const res = await fetch(`${API_BASE}/audit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(apiErrorMessage(data, res.statusText || 'Audit failed'))
  }
  return data
}

async function postResolve(auditId, body) {
  const res = await fetch(`${API_BASE}/audit/${auditId}/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(apiErrorMessage(data, res.statusText || 'Resolve failed'))
  }
  return data
}

function VerdictBadge({ verdict }) {
  const map = {
    ACCEPT: 'verdict verdict--accept',
    REJECT: 'verdict verdict--reject',
    ESCALATE: 'verdict verdict--escalate',
  }
  return <span className={map[verdict] || 'verdict'}>{verdict}</span>
}

export default function App() {
  const [reasoning, setReasoning] = useState('')
  const [evidenceText, setEvidenceText] = useState('')
  const [policiesText, setPoliciesText] = useState('')
  const [finalVerdict, setFinalVerdict] = useState('ACCEPT')
  const [reviewerNotes, setReviewerNotes] = useState('')

  const auditMutation = useMutation({
    mutationFn: (variables) => postAudit(variables),
  })

  const resolveMutation = useMutation({
    mutationFn: (variables) => postResolve(variables.auditId, variables.payload),
  })

  const handleClear = () => {
    setReasoning('')
    setEvidenceText('')
    setPoliciesText('')
    setFinalVerdict('ACCEPT')
    setReviewerNotes('')
    auditMutation.reset()
    resolveMutation.reset()
  }

  const result = auditMutation.data
  const err = auditMutation.error || resolveMutation.error

  return (
    <div className="app">
      <header className="header">
        <div className="header__brand">
          <span className="header__logo" aria-hidden="true" />
          <div>
            <h1 className="header__title">Decision Auditor</h1>
            <p className="header__subtitle">
              Multi-agent reasoning review · AI-assisted verdicts
            </p>
          </div>
        </div>
      </header>

      <main className="main">
        <section className="card card--form">
          <h2 className="card__heading">New audit</h2>
          <p className="card__hint">
            Describe the reasoning to evaluate. Add evidence and policies as
            separate lines (optional).
          </p>

          <label className="field">
            <span className="field__label">Reasoning</span>
            <textarea
              className="field__input field__input--area"
              rows={5}
              placeholder="Paste or type the decision reasoning paragraph…"
              value={reasoning}
              onChange={(e) => setReasoning(e.target.value)}
            />
          </label>

          <label className="field">
            <span className="field__label">Evidence (one item per line)</span>
            <textarea
              className="field__input field__input--area"
              rows={3}
              placeholder="Report A&#10;Study B"
              value={evidenceText}
              onChange={(e) => setEvidenceText(e.target.value)}
            />
          </label>

          <label className="field">
            <span className="field__label">Policies (one per line)</span>
            <textarea
              className="field__input field__input--area"
              rows={2}
              placeholder="Internal policy notes…"
              value={policiesText}
              onChange={(e) => setPoliciesText(e.target.value)}
            />
          </label>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              type="button"
              className="btn btn--primary"
              disabled={!reasoning.trim() || auditMutation.isPending}
              onClick={() =>
                auditMutation.mutate({
                  reasoning,
                  evidence: parseLines(evidenceText),
                  policies: parseLines(policiesText),
                })
              }
            >
              {auditMutation.isPending ? 'Running pipeline…' : 'Run audit'}
            </button>
            <button
              type="button"
              className="btn btn--secondary"
              disabled={auditMutation.isPending}
              onClick={handleClear}
            >
              Clear Form
            </button>
          </div>
        </section>

        {(result || err || auditMutation.isPending) && (
          <section className="card card--result">
            <h2 className="card__heading">Result</h2>

            {auditMutation.isPending && (
              <div className="banner banner--ok" role="status">
                Running pipeline...
              </div>
            )}

            {!auditMutation.isPending && err && (
              <div className="banner banner--error" role="alert">
                {String(err.message)}
              </div>
            )}

            {!auditMutation.isPending && result && (
              <>
                <div className="result-row">
                  <span className="result-label">Verdict</span>
                  <VerdictBadge verdict={result.verdict} />
                </div>

                <div className="result-row">
                  <span className="result-label">Confidence</span>
                  <div className="confidence">
                    <div
                      className="confidence__bar"
                      style={{
                        width: `${Math.round((result.confidence || 0) * 100)}%`,
                      }}
                    />
                    <span className="confidence__value">
                      {(result.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>

                {result.audit_id != null && (
                  <p className="meta">
                    Audit ID: <code>{result.audit_id}</code>
                  </p>
                )}

                <div className="explanation">
                  <span className="result-label">Explanation</span>
                  <p>{result.explanation}</p>
                </div>

                <details className="breakdown">
                  <summary>Breakdown (JSON)</summary>
                  <pre className="breakdown__pre">
                    {JSON.stringify(result.breakdown || {}, null, 2)}
                  </pre>
                </details>

                {result.verdict === 'ESCALATE' && result.audit_id != null && (
                  <div className="hitl">
                    <h3 className="hitl__title">Human review</h3>
                    <p className="card__hint">
                      This audit is escalated. Submit a final decision for audit{' '}
                      <code>{result.audit_id}</code>.
                    </p>

                    <label className="field">
                      <span className="field__label">Final verdict</span>
                      <select
                        className="field__input"
                        value={finalVerdict}
                        onChange={(e) => setFinalVerdict(e.target.value)}
                      >
                        <option value="ACCEPT">ACCEPT</option>
                        <option value="REJECT">REJECT</option>
                      </select>
                    </label>

                    <label className="field">
                      <span className="field__label">Reviewer notes</span>
                      <textarea
                        className="field__input field__input--area"
                        rows={3}
                        value={reviewerNotes}
                        onChange={(e) => setReviewerNotes(e.target.value)}
                      />
                    </label>

                    <button
                      type="button"
                      className="btn btn--secondary"
                      disabled={
                        resolveMutation.isPending || !reviewerNotes.trim()
                      }
                      onClick={() =>
                        resolveMutation.mutate({
                          auditId: result.audit_id,
                          payload: {
                            final_verdict: finalVerdict,
                            reviewer_notes: reviewerNotes,
                          },
                        })
                      }
                    >
                      {resolveMutation.isPending
                        ? 'Submitting…'
                        : 'Submit resolution'}
                    </button>

                    {resolveMutation.isSuccess && (
                      <div className="banner banner--ok" role="status">
                        Resolution saved.
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </section>
        )}
      </main>

      <footer className="footer">
        API: <code>{API_BASE}</code> · configure{' '}
        <code>VITE_API_URL</code> in <code>.env</code>
      </footer>
    </div>
  )
}
