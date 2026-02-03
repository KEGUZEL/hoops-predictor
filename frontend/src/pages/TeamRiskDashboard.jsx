import React, { useState } from "react";
import TeamSelector from "../components/TeamSelector";
import TeamRiskCard from "../components/TeamRiskCard";

function TeamRiskDashboard() {
  const [selectedTeam, setSelectedTeam] = useState(null);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">
        Takım Yorgunluk & Sakatlık Riski
      </h1>

      <TeamSelector onTeamSelect={setSelectedTeam} />

      {selectedTeam && <TeamRiskCard team={selectedTeam} />}
    </div>
  );
}

export default TeamRiskDashboard;

