import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

function PlayerHistoryChart({ player }) {
  const [data, setData] = useState([]);
  const [avg, setAvg] = useState(0);

  useEffect(() => {
    if (!player?.id) return;

    const fetchHistory = async () => {
      try {
        const res = await axios.get(`/api/players/${player.id}/history`, {
          params: { limit: 10 },
        });
        const history = res.data.history || [];
        setData(
          history.map((h) => ({
            date: h.game_date,
            points: h.points,
          })),
        );
        if (history.length > 0) {
          const sum = history.reduce((acc, h) => acc + h.points, 0);
          setAvg(sum / history.length);
        } else {
          setAvg(0);
        }
      } catch {
        setData([]);
        setAvg(0);
      }
    };

    fetchHistory();
  }, [player?.id]);

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <h2 className="mb-3 text-sm font-semibold text-slate-300">
        Son Maç Performansı
      </h2>
      {data.length === 0 ? (
        <p className="text-xs text-slate-400">
          Henüz veri bulunamadı. Önce backend veritabanını doldurman gerekiyor.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={data}>
            <XAxis dataKey="date" tick={{ fontSize: 10 }} />
            <YAxis tick={{ fontSize: 10 }} />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="points"
              stroke="#22c55e"
              strokeWidth={2}
              dot={{ r: 3 }}
            />
            <ReferenceLine
              y={avg}
              stroke="#38bdf8"
              strokeDasharray="4 4"
              label={{
                value: `Ortalama (${avg.toFixed(1)})`,
                position: "insideTopRight",
                fontSize: 10,
              }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default PlayerHistoryChart;

