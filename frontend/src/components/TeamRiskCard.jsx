import React, { useEffect, useState } from "react";
import axios from "axios";

function TeamRiskCard({ team }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!team?.id) return;

    const fetchRisk = async () => {
      try {
        setError("");
        const res = await axios.get(`/api/teams/${team.id}/risk`);
        setData(res.data);
      } catch {
        setError("Takım riski alınırken hata oluştu.");
      }
    };

    fetchRisk();
  }, [team?.id]);

  const badgeColor =
    data?.risk_level === "high"
      ? "bg-red-500 text-red-50"
      : data?.risk_level === "medium"
        ? "bg-amber-500 text-amber-50"
        : "bg-emerald-500 text-emerald-950";

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <h2 className="mb-3 text-sm font-semibold text-slate-300">
        Takım Risk Özeti
      </h2>
      {error && <p className="text-xs text-red-400">{error}</p>}

      {data && (
        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2">
            <span className="text-base font-semibold">
              {data.team_name} (ID: {data.team_id})
            </span>
            <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${badgeColor}`}>
              {data.risk_level?.toUpperCase()}
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Oyuncu sayısı: {data.player_count}
          </p>
          <p className="text-xs text-slate-400">
            Yorgunluk skoru: {data.fatigue_score}
          </p>
        </div>
      )}
    </div>
  );
}

export default TeamRiskCard;

