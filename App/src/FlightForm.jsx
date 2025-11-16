import { useState } from "react";

export default function FlightForm() {
  const [prompt, setPrompt] = useState("");
  const [airport, setAirport] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  const handleSearch = () => {
    // Collect filled entries only
    const filledEntries = {};
    if (prompt) filledEntries.prompt = prompt;
    if (airport) filledEntries.airport = airport;
    if (startDate) filledEntries.startDate = startDate;
    if (endDate) filledEntries.endDate = endDate;
    if (maxPrice) filledEntries.maxPrice = maxPrice;

    console.log("Filled entries:", filledEntries);

    // Example: send to Python backend
    // fetch("http://localhost:8000/search", {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(filledEntries),
    // });
  };

  return (
    <div
      style={{
        transform: "scale(4)",
        transformOrigin: "top center",
        marginLeft: "200px",
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: "1rem",
        width: "100%",
        padding: "2rem",
        backgroundColor: "rgba(0,0,0,0.3)",
        borderRadius: "16px",
        backdropFilter: "blur(10px)",
      }}
    >
      <input
        type="text"
        placeholder="Take me somewhere I can dream..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        style={{
          padding: "1rem 1.8rem",
          borderRadius: "14px",
          border: "none",
          width: "380px",
          height: "60px",
          fontSize: "1rem",
          textAlign: "left",
          background: "rgba(255,255,255,0.18)",
          backdropFilter: "blur(12px)",
          color: "white",
        }}
      />
      <input
        type="number"
        placeholder="Airport Code"
        value={airport}
        onChange={(e) => setAirport(e.target.value)}
        style={{ padding: "0.8rem", borderRadius: "8px", border: "none", width: "120px" }}
      />
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
        style={{ padding: "0.8rem", borderRadius: "8px", border: "none" }}
      />
      <input
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
        style={{ padding: "0.8rem", borderRadius: "8px", border: "none" }}
      />
      <input
        type="number"
        placeholder="Max price ($)"
        value={maxPrice}
        onChange={(e) => setMaxPrice(e.target.value)}
        style={{ padding: "0.8rem", borderRadius: "8px", border: "none", width: "120px" }}
      />

      <button
        onClick={handleSearch}
        style={{
          padding: "0.8rem 1.5rem",
          borderRadius: "8px",
          backgroundColor: "#1a73e8",
          color: "white",
          border: "none",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Search
      </button>
    </div>
  );
}
