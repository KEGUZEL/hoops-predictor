import React, { useState } from "react";
import PlayerSearchPanel from "../components/PlayerSearchPanel";
import PlayerPredictionCard from "../components/PlayerPredictionCard";
import PlayerHistoryChart from "../components/PlayerHistoryChart";

function PlayerDashboard() {
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">
        Oyuncu Performans Analizi
      </h1>

      <PlayerSearchPanel onPlayerSelect={setSelectedPlayer} />

      {selectedPlayer && (
        <div className="grid gap-6 md:grid-cols-2">
          <PlayerPredictionCard player={selectedPlayer} />
          <PlayerHistoryChart player={selectedPlayer} />
        </div>
      )}
    </div>
  );
}

export default PlayerDashboard;

