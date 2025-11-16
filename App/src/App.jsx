import FlightsGlobe from "./FlightsGlobe.jsx";
import TextAnimation from "./TextAnimation.jsx";
import BloboLogo from "./assets/blobo.png";


export default function App() {
  return (
      <div>

          <div style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              marginTop: "20px",
              marginBottom: "20px",
              position: "relative"
          }}>
              {/* Blobo text centered */}
              <TextAnimation/>

              {/* Logo positioned 300px to the left of Blobo */}
              <img
                  src={BloboLogo}
                  alt="Logo"
                  style={{
                      height: "400px",
                      width: "400px",
                      position: "absolute",
                      right: `calc(50% + 500px)` // 50% of screen + half the spacing
                  }}
              />
              <img
                  src={BloboLogo}
                  alt="Logo"
                  style={{
                      height: "400px",
                      width: "400px",
                      position: "absolute",
                      right: `calc(50% - 900px)` // 50% of screen + half the spacing
                  }}
              />
          </div>


          <div
              style={{
                  transform: "scale(4)",
                  transformOrigin: "top center",
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
                  style={{
                      padding: "1rem 1.8rem",
                      borderRadius: "14px",
                      border: "none",
                      width: "380px",       // ⬅️ bigger width
                      height: "60px",       // ⬅️ taller input
                      fontSize: "1rem",     // ⬅️ bigger text
                      textAlign: "left",    // ⬅️ feels more like a chatbox
                      background: "rgba(255,255,255,0.18)",
                      backdropFilter: "blur(12px)",
                      color: "white"
                  }}
              />


              <input
                  type="date"
                  style={{padding: "0.8rem", borderRadius: "8px", border: "none"}}
              />
              <input
                  type="date"
                  style={{padding: "0.8rem", borderRadius: "8px", border: "none"}}
              />
              <input
                  type="number"
                  placeholder="Max price ($)"
                  style={{padding: "0.8rem", borderRadius: "8px", border: "none", width: "120px"}}
              />

              <button
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


          {/* Globe */}
          <div style={{aspectRatio: "1/1", marginTop: "400px", marginLeft: "280px"}}>
              <FlightsGlobe/>
          </div>

      </div>
  );
}