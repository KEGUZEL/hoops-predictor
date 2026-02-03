import React, { useEffect, useState } from "react";
import axios from "axios";

function PlayerPredictionCard({ player }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!player?.id) return;

    const fetchPrediction = async () => {
      try {
        setLoading(true);
        setError("");
        const res = await axios.get(`/api/players/${player.id}/prediction`);
        setData(res.data);
      } catch (err) {
        setError("Tahmin alınırken hata oluştu.");
      } finally {
        setLoading(false);
      }
    };

    fetchPrediction();
  }, [player?.id]);

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <h2 className="mb-3 text-sm font-semibold text-slate-300">
        Oyuncu Tahmini
      </h2>

      {loading && <p className="text-xs text-slate-400">Yükleniyor...</p>}
      {error && <p className="text-xs text-red-400">{error}</p>}

      {data && (
        <div className="space-y-2 text-sm">
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-emerald-400">
              {(data.prob_above_avg * 100).toFixed(1)}%
            </span>
            <span className="text-xs uppercase tracking-wide text-slate-400">
              {data.prediction_label}
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Tarih: {data.game_date}
          </p>
          <ul className="mt-2 space-y-1 text-xs text-slate-300">
            <li>Son 5 maç ortalama sayı: {data.rolling_pts_5.toFixed(1)}</li>
            <li>Dinlenme günü: {data.rest_days}</li>
            <li>
              Matchup zorluk skoru: {data.matchup_difficulty_score.toFixed(2)}
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default PlayerPredictionCard;

