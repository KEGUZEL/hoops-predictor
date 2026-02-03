import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import PlayerDashboard from "./pages/PlayerDashboard";
import TeamRiskDashboard from "./pages/TeamRiskDashboard";

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      <header className="border-b border-slate-800 bg-slate-900/70 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <span className="text-lg font-semibold tracking-tight">
            HoopsPredictor
          </span>
          <nav className="flex gap-4 text-sm">
            <Link to="/" className="hover:text-emerald-300">
              Oyuncu Analiz
            </Link>
            <Link to="/teams" className="hover:text-emerald-300">
              Takım Risk Haritası
            </Link>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        <Routes>
          <Route path="/" element={<PlayerDashboard />} />
          <Route path="/teams" element={<TeamRiskDashboard />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

