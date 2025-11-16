import FlightsGlobe from "./FlightsGlobe.jsx";
import TextAnimation from "./TextAnimation.jsx";
import BloboLogo from "./assets/blobo.png";
import FlightForm from "./FlightForm.jsx";


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


          <FlightForm />


          {/* Globe */}
          <div style={{aspectRatio: "1/1", marginTop: "400px", marginLeft: "280px"}}>
              <FlightsGlobe/>
          </div>

      </div>
  );
}