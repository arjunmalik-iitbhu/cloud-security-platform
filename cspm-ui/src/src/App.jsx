import { useState, useRef, useEffect } from 'react'
import activity from '/activity.svg'
import moreDown from '/moreDown.svg'
import moreUp from '/moreUp.svg'
import refresh from '/refresh.svg'

export { activity, moreDown, moreUp, refresh }
import './App.css'

const config = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
}

const RISK_LOW = 'low'
const RISK_HIGH = 'high'

const OPTIONS = [
  { value: 'all', name: 'All Risk' },
  { value: RISK_LOW, name: 'Low Risk' },
  { value: RISK_HIGH, name: 'High Risk' },
]

function App() {
  const dialogElementRef = useRef(null)
  const accessKeyInputRef = useRef(null)
  const secretAccessKeyInputRef = useRef(null)
  const regionInputRef = useRef(null)

  const credentialRef = useRef('')
  const accessKeyRef = useRef('')
  const secretAccessKeyRef = useRef('')

  const [scannedAssets, setScannedAssets] = useState(0)
  const [lowRiskAssets, setLowRiskAssets] = useState(0)
  const [highRiskAssets, setHighRiskAssets] = useState(0)
  const [resources, setResources] = useState([])
  const riskFilterRef = useRef(OPTIONS[0].value)
  const fetchAnalysis = async () => {
    if (!credentialRef.current) throw new Error('Empty credential id')
    const resp = await fetch(`${config.API_BASE_URL}/version/v1/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        credentialId: credentialRef.current,
        resourceRisk: riskFilterRef.current,
      }),
    })
    const { resources = [] } = (await resp.json()) || {}
    setScannedAssets(resources.length)
    setLowRiskAssets(resources.filter((elem) => elem.currentResourceRisk === RISK_LOW).length)
    setHighRiskAssets(resources.filter((elem) => elem.currentResourceRisk === RISK_HIGH).length)
    setResources(resources)
  }
  const showSecretDialog = () => {
    dialogElementRef?.current?.showModal()
  }
  const closeSecretDialog = () => {
    dialogElementRef?.current?.close()
  }
  const onSubmit = async () => {
    const accessKey = accessKeyInputRef?.current?.value || ''
    const secretAccessKey = secretAccessKeyInputRef?.current?.value || ''
    const region = regionInputRef?.current?.value || ''
    if (!accessKey) {
      closeSecretDialog()
      alert('Empty access key. Please provide a value')
      return
    }
    if (!secretAccessKey) {
      closeSecretDialog()
      alert('Empty secret access key. Please provide a value')
      return
    }
    if (accessKeyRef.current && accessKey === accessKeyRef.current) {
      closeSecretDialog()
      alert('Access key is duplicate. Please provide different value')
      return
    }
    if (secretAccessKeyRef.current && secretAccessKey === secretAccessKeyRef.current) {
      closeSecretDialog()
      alert('Secret access key is duplicate. Please provide different value')
      return
    }
    accessKeyRef.current = accessKey
    secretAccessKeyRef.current = secretAccessKey
    const resp = await fetch(`${config.API_BASE_URL}/version/v1/credential`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cloudName: 'Amazon Web Services',
        accessKey,
        secretAccessKey,
        region,
      }),
    })
    credentialRef.current = (await resp.json())?.id || ''
    await fetchAnalysis()
    closeSecretDialog()
  }

  return (
    <div className="cspm">
      <div className="top-panel">
        <button
          className="refresh-button"
          onClick={fetchAnalysis}
          disabled={!credentialRef.current}
        >
          <img src={refresh} />
        </button>
        <dialog ref={dialogElementRef} className="secrets-dialog">
          <p>AWS Access Key</p>
          <input
            ref={accessKeyInputRef}
            className="secrets-dialog-access-key"
            placeholder="Value"
          />
          <p>AWS Secret Access Key</p>
          <input
            ref={secretAccessKeyInputRef}
            className="secrets-dialog-secret-access-key"
            placeholder="Value"
          />
          <p>Region</p>
          <input
            ref={regionInputRef}
            className="secrets-dialog-region"
            placeholder="Value"
          />
          <p>Message [Optional]</p>
          <input className="secrets-dialog-message" placeholder="Value" />
          <div className="secrets-dialog-buttons">
            <button onClick={closeSecretDialog}>Close</button>
            <button onClick={onSubmit}>Submit</button>
          </div>
        </dialog>
        <button onClick={showSecretDialog} className="secrets-button">
          Enter AWS Credential
        </button>
      </div>
      <h1 className="title">
        {lowRiskAssets / (scannedAssets || 1) > 0.5 ? 'Low Risk 🟢' : 'High Risk 🔴'}
      </h1>
      <div className="cards">
        <div className="card-1">
          <div className="card-title">Scanned Assets</div>
          <div className="card-value">
            <p>{scannedAssets}</p>
            <img src={activity} />
          </div>
        </div>
        <div className="card-2">
          <div className="card-title">Low Risk Assets</div>
          <div className="card-value">
            <p>{lowRiskAssets}</p>
            <img src={activity} />
          </div>
        </div>
        <div className="card-3">
          <div className="card-title">High Risk Assets</div>
          <div className="card-value">
            <p>{highRiskAssets}</p>
            <img src={activity} />
          </div>
        </div>
      </div>
      <div className="resources">
        <p className="resources-title">Resources</p>
        <div className="resources-filter">
          <select defaultValue={riskFilterRef.current}>
            {OPTIONS.map((elem, id) => (
              <option id={id} value={elem.value} key={id}>
                {elem.name}
              </option>
            ))}
          </select>
        </div>
        <div className="resources-table">
          <table>
            <thead>
              <tr className="resources-table-header">
                <th>Resource</th>
                <th>Type</th>
                <th>Status</th>
                <th>Risk</th>
              </tr>
            </thead>
            <tbody>
              {resources.map(({ resource, type, status, risk }, id) => (
                <tr id={id}>
                  <td>
                    {/* {getResourceIcon[type]} */}
                    {resource}
                  </td>
                  <td>{type}</td>
                  <td>{status}</td>
                  <td>{risk}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default App
