import React, { useState, useEffect } from "react";
import axios from "axios";

function PlayerSearchPanel({ onPlayerSelect }) {
  const [players, setPlayers] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [loading, setLoading] = useState(true);

  // Sayfa açılınca oyuncu listesini çek
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const res = await axios.get("/api/players/");
        // İsim sırasına göre alfabetik sıralayalım
        const sorted = res.data.sort((a, b) => a.name.localeCompare(b.name));
        setPlayers(sorted);
        setLoading(false);
      } catch (err) {
        console.error("Oyuncu listesi yüklenemedi", err);
        setLoading(false);
      }
    };
    fetchPlayers();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedId) return;
    onPlayerSelect({ id: Number(selectedId) });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-wrap items-end gap-3 rounded-lg border border-slate-800 bg-slate-900/60 p-4"
    >
      <div className="flex flex-col w-full sm:w-64">
        <label htmlFor="playerId" className="text-xs font-medium text-slate-400 mb-1">
          Oyuncu Seçiniz
        </label>
        
        <select
          id="playerId"
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value)}
          className="rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-50 outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
        >
          <option value="">-- Bir Oyuncu Seçin --</option>
          {loading ? (
            <option disabled>Yükleniyor...</option>
          ) : (
            players.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.position})
              </option>
            ))
          )}
        </select>
      </div>
      
      <button
        type="submit"
        disabled={!selectedId}
        className="rounded-md bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Tahmin Göster
      </button>
    </form>
  );
}

export default PlayerSearchPanel;