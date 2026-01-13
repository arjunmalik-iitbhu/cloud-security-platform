import { useState } from 'react'
import activity from '/activity.svg'
import moreDown from '/moreDown.svg'
import moreUp from '/moreUp.svg'
import refresh from '/refresh.svg'

export { activity, moreDown, moreUp, refresh }
import './App.css'

const OPTIONS = [
  { value: 'all', name: 'All Risk' },
  { value: 'low-risk', name: 'Low Risk' },
  { value: 'high-risk', name: 'High Risk' },
]

function App() {
  const [scannedAssets, setScannedAssets] = useState(0)
  const [lowRiskAssets, setLowRiskAssets] = useState(0)
  const [highRiskAssets, setHighRiskAssets] = useState(0)
  const [resources, setResources] = useState([])
  const fetchAnalysis = () => {}

  const showSecretDialog = () => {
    document.getElementsByClassName['secrets-dialog'][0]?.showModal()
  };
  const closeSecretDialog = () => {
    document.getElementsByClassName['secrets-dialog'][0]?.close()
  };
  const onSubmit = () => {
    closeSecretDialog()
  }

  return (
    <div className="cspm">
      <div className="top-panel">
        <button className="refresh-button">
          <img src={refresh} />
        </button>
        <dialog className="secrets-dialog">
          <p>AWS Access Key</p>
          <input placeholder="Value" />
          <p>AWS Secret Access Key</p>
          <input placeholder="Value" />
          <p>Message [Optional]</p>
          <input placeholder="Value" /> */}
          <button onClick={closeSecretDialog}>Close</button>
          <button onClick={onSubmit}>Sumbit</button>
        </dialog>
        <button onClick={showSecretDialog} className="secrets-button">
          Enter AWS Credential
        </button>
      </div>
      <h1 className="title">{lowRiskAssets / (scannedAssets || 1) > 0.5 ? 'Low Risk 🟢' : 'High Risk 🔴'}</h1>
      <div className="cards">
        <div className="card-1">
          <div className="card-title">Scanned Assets</div>
          <div className="card-value">
            <p>{ scannedAssets }</p>
            <img src={ activity } />
          </div>
        </div>
        <div className="card-2">
          <div className="card-title">Low Risk Assets</div>
          <div className="card-value">
            <p>{ lowRiskAssets }</p>
            <img src={ activity } />
          </div>
        </div>
        <div className="card-3">
          <div className="card-title">High Risk Assets</div>
          <div className="card-value">
            <p>{ highRiskAssets }</p>
            <img src={ activity } />
          </div>
        </div>
      </div>
      <div className="resources">
        <p className="resources-title">
          Resources
        </p>
        <div className="resources-filter">
          <select>
              {
                OPTIONS.map((elem, id) => (
                  <option id={id} value={elem.value}>
                    {elem.name}
                  </option>
                ))
              }
          </select>
        </div>
        <div className="resources-table">
          <table>
            <tr className="resources-table-header">
              <th>Resource</th>
              <th>Type</th>
              <th>Status</th>
              <th>Risk</th>
            </tr>
            {resources.map(({ resource, type, status, risk }, id) => (
              <tr id={id}>
                <td>
                  {getLogo[type]}
                  {resource}
                </td>
                <td>{type}</td>
                <td>{status}</td>
                <td>{risk}</td>
              </tr>
            ))}
        </table>
        </div>
      </div>
    </div>
  )
}

export default App
