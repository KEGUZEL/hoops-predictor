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
        <div className="space-y-3 text-sm">
          {/* Tahmin Kısmı */}
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-emerald-400">
              {(data.prob_above_avg * 100).toFixed(1)}%
            </span>
            <span className="text-xs uppercase tracking-wide text-slate-400">
              {data.prediction_label}
            </span>
          </div>
          <p className="text-xs text-slate-500">
            Tarih: {data.game_date}
          </p>

          <hr className="border-slate-800" />

          {/* İstatistikler */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-slate-400">Sezon Ortalaması</p>
              <p className="text-lg font-semibold text-white">
                {data.season_avg_pts.toFixed(1)}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-400">Son 5 Maç (Ort)</p>
              <p className="text-lg font-semibold text-emerald-300">
                {data.rolling_pts_5.toFixed(1)}
              </p>
            </div>
          </div>

          <div className="mt-2 space-y-1 text-xs text-slate-400">
            <p>Dinlenme günü: <span className="text-slate-200">{data.rest_days}</span></p>
            <p>Zorluk skoru: <span className="text-slate-200">{data.matchup_difficulty_score.toFixed(2)}</span></p>
          </div>
        </div>
      )}
    </div>
  );
}

export default PlayerPredictionCard;