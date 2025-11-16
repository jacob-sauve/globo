import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import FlightsGlobe from "./FlightsGlobe.jsx"

function App() {
  const [count, setCount] = useState(0)
return (
    <div className="w-full h-screen flex flex-col bg-gray-900 text-white">
      {/* Top Bar */}
      <div className="w-full flex items-center px-6 py-4 bg-black/40 backdrop-blur-md shadow-md z-10">
        <img src="/logo.png" alt="Logo" className="h-10 w-10 mr-3" />
        <h1 className="text-3xl font-bold tracking-wide">GLOBO</h1>
      </div>

      {/* Search Bar */}
      <div className="w-full flex justify-center mt-4 z-10">
        <div className="flex gap-3 bg-black/30 backdrop-blur-md p-4 rounded-2xl shadow-lg">
          <input
            type="text"
            placeholder="From (airport/city)"
            className="px-4 py-2 rounded-xl bg-gray-800 text-white outline-none"
          />
          <input
            type="date"
            className="px-4 py-2 rounded-xl bg-gray-800 text-white outline-none"
          />
          <button className="px-6 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 transition font-semibold">
            Search
          </button>
        </div>
      </div>

      <div className="flex-1">
        <FlightsGlobe />
      </div>
    </div>
  );
}

export default App
