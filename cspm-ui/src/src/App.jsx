import { useState } from 'react'
import activity from '/activity.svg'
import moreDown from '/moreDown.svg'
import moreUp from '/moreUp.svg'
import refresh from '/refresh.svg'

export { activity, moreDown, moreUp, refresh }
import './App.css'

const DEFAULT_URI =
  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Cube_3d_in_sharp_solid_style.svg/1024px-Cube_3d_in_sharp_solid_style.svg.png'

const OPTIONS = [
  { value: 'all', name: 'All Risk' },
  { value: 'low-risk', name: 'Low Risk' },
  { value: 'high-risk', name: 'High Risk' },
]

function App() {
  const [count, setCount] = useState(0)
  const [scannedAssets, setScannedAssets] = useState(0)
  const [lowRiskAssets, setLowRiskAssets] = useState(0)
  const [highRiskAssets, setHighRiskAssets] = useState(0)
  const [resources, setResources] = useState([])
  const fetchAnalysis = () => {}

  const onSubmit = () => {
    document.getElementsByClassName['dialog'][0].close()
  }

  return (
    <>
      <div className="top-panel">
        <button onClick={fetchAnalysis}>
          <img src={refresh} />
        </button>
        <button onClick={document.getElementsByClassName['dialog'][0].showModal()}>
          Enter AWS Credential
        </button>
        <dialog className="dialog">
          <p>AWS Access Key</p>
          <input placeholder="Value" />
          <p>AWS Secret Access Key</p>
          <input placeholder="Value" />
          <p>Message [Optional]</p>
          <button onClick={document.getElementsByClassName['dialog'][0].close}>Close</button>
          <button onClick={onSubmit}>Sumbit</button>
        </dialog>
      </div>
      <h1>{lowRiskAssets / (scannedAssets || 1) > 0.5 ? 'Low Risk 🟢' : 'High Risk 🔴'}</h1>
      <div className="cards">
        <div className="card-1">
          <button onClick={() => setCount((count) => count + 1)}>count is {count}</button>
          <p>Scanned Assets</p>
          <p>
            {{ scannedAssets }} <img src={{ activity }} />
          </p>
        </div>
        <div className="card-2">
          <p>Low Risk Assets</p>
          <p>
            {{ lowRiskAssets }} <img src={{ activity }} />
          </p>
        </div>
        <div className="card-3">
          <p>High Risk Assets</p>
          <p>
            {{ highRiskAssets }} <img src={{ activity }} />
          </p>
        </div>
      </div>
      <p className="resources">
        Resources
        <select>
          {{
            ...OPTIONS.map((elem, id) => (
              <option id={id} value={elem.value}>
                {elem.name}
              </option>
            )),
          }}
        </select>
      </p>
      <table>
        <tc>
          <td>Resource</td>
          <td>Type</td>
          <td>Status</td>
          <td>Risk</td>
        </tc>
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
    </>
  )
}

export default App
