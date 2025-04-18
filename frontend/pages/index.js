import { useState, useEffect } from "react";

export default function Home() {
  // Renamed state variable from users to salesReps
  const [salesReps, setSalesReps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  useEffect(() => {
    // Updated fetch URL to the correct backend endpoint
    fetch("http://localhost:8000/api/sales-reps")
      .then((res) => {
        if (!res.ok) { // Basic error handling for HTTP status codes
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        // Adjusted data access to get the salesReps array
        // Assuming dummyData.json is { "salesReps": [...] }
        setSalesReps(data || []); // Set state directly with the received array, or empty array if data is null/undefined
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch data:", err);
        setLoading(false);
        // You might want to display an error message to the user in the UI
      });
  }, []); // Empty dependency array means this runs once on mount

  const handleAskQuestion = async () => {
    try {
      const response = await fetch("/api/ai", { // Using relative path for AI endpoint too
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error("Error in AI request:", error);
      setAnswer("Error getting AI response."); // Display error to user
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Sales Dashboard</h1> {/* Updated title */}

      <section style={{ marginBottom: "2rem" }}>
        <h2>Sales Representative Performance</h2> {/* Updated section title */}
        {/* Updated loading message */}
        {loading ? (
          <p>Loading sales data...</p> 
          
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '2rem' }}> {/* Example Grid layout */}
            {salesReps.map((rep) => ( // Map over salesReps state
              <div key={rep.id} style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px', backgroundColor: '#f9f9f9' }}> {/* Styled container for each rep */}
                <h3>{rep.name} ({rep.role})</h3> {/* Display rep name and role */}
                {rep.deals && rep.deals.length > 0 ? ( // Check if deals exist and have items
                  <div> {/* Container for deals list */}
                    <h4>Deals:</h4>
                    <ul style={{ listStyle: 'none', padding: 0 }}> {/* Style the list */}
                      {rep.deals.map((deal) => ( // Map over nested deals
                        <li key={deal.id} style={{ marginBottom: '0.5rem', padding: '0.5rem', borderBottom: '1px dashed #eee' }}> {/* Style each deal item */}
                          Client: <strong>{deal.client}</strong><br />
                          Status: {deal.status}<br />
                          Value: ${deal.value ? deal.value.toLocaleString() : 'N/A'} {/* Format value, handle missing */}
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : (
                  /* Message if no deals */
                  <p>No deals recorded for this representative.</p> 
                )}
                {/* Add rendering for clients here if needed and structured in dummy data */}
              </div>
            ))}
          </div>
        )}
        {/* Add a message if salesReps array is empty after loading */}
        {!loading && salesReps.length === 0 && <p>No sales representatives found.</p>}
      </section>

      <section>
        <h2>Ask a Question (AI Endpoint)</h2>
        <div>
          <input
            type="text"
            placeholder="Enter your question about sales data..." /* Updated placeholder */
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            style={{ marginRight: '0.5rem', padding: '0.5rem' }} /* Basic input style */
          />
          <button onClick={handleAskQuestion} style={{ padding: '0.5rem 1rem' }}>Ask</button> {/* Basic button style */}
        </div>
        {answer && (
          <div style={{ marginTop: "1rem", padding: '1rem', border: '1px solid #eee', backgroundColor: '#fff' }}> {/* Basic AI response box style */}
            <strong>AI Response:</strong> {answer}
          </div>
        )}
      </section>
    </div>
  );
}