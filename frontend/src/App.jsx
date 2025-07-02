import { useState } from 'react'
import './App.css'

function App() {
    const [zipcode, setZipcode] = useState('')
    const [permit, setPermit] = useState(null)
    const [error, setError] = useState(null)
    const [showAll, setShowAll] = useState(false)

    const handleInputChange = (e) => {
        const value = e.target.value;
        setZipcode(value);
        if (value.trim() === "") {
            setPermit(null);
            setShowAll(false);
        }
    }

    const handleSearch = async () => {
        setError('');
        setShowAll(false);

        if (!/^\d{5}$/.test(zipcode)) {
            setPermit(null)
            setError("Please enter a valid 5-digit zipcode");
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:5000/permits/${zipcode}/all`)
            const data = await response.json()
            setPermit(data)
        } catch (error) {
            console.error("Fetch error:", error);
            setError("Something went wrong. Please try again.");
        }
    }

    return (
        <>
            <div className='container'>
                <h1>Start Your Permit Search</h1>
                <p>
                    Permilytic helps you look up building permit information by ZIP code.
                    Enter a 5-digit ZIP code below and click "Submit" to see permits, fees, and timelines.
                </p>
                <p>
                    Example: Try entering <code><strong>98101</strong></code>.
                </p>

                <div className='form-row'>
                    <input value={zipcode} onChange={handleInputChange} />
                    <button onClick={handleSearch}>Submit</button>
                </div>

                {error && <p style={{ color: 'red' }}>{error}</p>}

                {permit && permit.length > 0 && (
                    <div>
                        <h2>Permit Details</h2>
                        {permit.slice(0, showAll ? permit.length : 1).map((p, index) => (
                            <div key={index} style={{ marginBottom: "1rem" }}>
                                <p><strong>Type:</strong> {p.type}</p>
                                <p><strong>Fee:</strong> {p.fee}</p>
                                <p><strong>Permit Type:</strong> {p.permit_type}</p>
                                <p><strong>Processing Time:</strong> {p.processing_time}</p>
                                <p><strong>Required:</strong> {p.required ? "Yes" : "No"}</p>
                            </div>
                        ))}

                        {permit.length > 3 && !showAll && (
                            <button onClick={() => setShowAll(true)}>Show all permits</button>
                        )}
                        {showAll && (
                            <button onClick={() => setShowAll(false)}>Show less</button>
                        )}
                    </div>
                )}
            </div>
        </>
    )
}

export default App

