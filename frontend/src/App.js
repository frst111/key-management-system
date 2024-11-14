import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [keys, setKeys] = useState([]);
    const [userType, setUserType] = useState('');
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchKeys();
    }, []);

    const fetchKeys = async () => {
        try {
            const res = await axios.get('http://127.0.0.1:8000/keys');
            setKeys(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleAssignKey = async () => {
        try {
            const res = await axios.post('http://127.0.0.1:8000/keys/assign', null, {
                params: { user_type: userType },
            });
            setMessage(`Assigned key ${res.data.key_id} to ${userType}`);
            fetchKeys();
        } catch (err) {
            console.error(err);
            setMessage('No available keys for your user type');
        }
    };

    const handleReturnKey = async (keyId) => {
        try {
            await axios.post(`http://127.0.0.1:8000/keys/return/${keyId}`);
            setMessage(`Returned key ${keyId}`);
            fetchKeys();
        } catch (err) {
            console.error(err);
        }
    };

    const handleMonthlyInspection = async () => {
        try {
            await axios.post('http://127.0.0.1:8000/keys/monthly_inspection');
            setMessage('Monthly inspection completed');
            fetchKeys();
        } catch (err) {
            console.error(err);
            setMessage('Failed to perform monthly inspection');
        }
    };

    const returnedKeys = keys.filter((key) => key.status === 'Returned');
    const inUseKeys = keys.filter((key) => key.status === 'In Use');

    return (
        <div className="container">
            <h1>Key Management Dashboard</h1>

            <div className="assign-section">
                <h2>Pick Up a Key</h2>
                <select value={userType} onChange={(e) => setUserType(e.target.value)}>
                    <option value="">Select User Type</option>
                    <option value="Guest">Guest</option>
                    <option value="Cleaners">Cleaners</option>
                    <option value="Maintenance">Maintenance</option>
                </select>
                <button onClick={handleAssignKey} disabled={!userType}>
                    Pick Up Key
                </button>
                {message && <p className="message">{message}</p>}
            </div>


            <div className="inspection-section">
                <button onClick={handleMonthlyInspection}>Monthly Inspection</button>
            </div>

            <h2>All Keys</h2>
            <table>
                <thead>
                    <tr>
                        <th>Key ID</th>
                        <th>Type</th>
                        <th>Status</th>
                        <th>Assigned To</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {keys.map((key) => (
                        <tr key={key.id}>
                            <td>{key.key_id}</td>
                            <td>{key.type}</td>
                            <td>{key.status}</td>
                            <td>{key.assigned_to}</td>
                            <td>
                                {key.status === 'In Use' && key.assigned_to === userType && (
                                    <button onClick={() => handleReturnKey(key.key_id)}>
                                        Return Key
                                    </button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div className="key-lists">
                <div>
                    <h2>Keys That Have Been Returned</h2>
                    <ul>
                        {returnedKeys.map((key) => (
                            <li key={key.id}>
                                {key.key_id} ({key.type})
                            </li>
                        ))}
                    </ul>
                </div>

                <div>
                    <h2>Keys That Are In Use</h2>
                    <ul>
                        {inUseKeys.map((key) => (
                            <li key={key.id}>
                                {key.key_id} ({key.type}) - Assigned to {key.assigned_to}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default App;
