import React, { useState } from "react";

function TeamSelector({ onTeamSelect }) {
  const [teamId, setTeamId] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!teamId) return;
    onTeamSelect({ id: Number(teamId) });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-wrap items-end gap-3 rounded-lg border border-slate-800 bg-slate-900/60 p-4"
    >
      <div className="flex flex-col">
        <label htmlFor="teamId" className="text-xs font-medium text-slate-400">
          Takım ID
        </label>
        <input
          id="teamId"
          type="number"
          value={teamId}
          onChange={(e) => setTeamId(e.target.value)}
          className="mt-1 rounded-md border border-slate-700 bg-slate-950 px-3 py-1.5 text-sm text-slate-50 outline-none focus:border-emerald-400"
          placeholder="Örn: 1"
        />
      </div>
      <button
        type="submit"
        className="rounded-md bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400"
      >
        Risk Haritası Göster
      </button>
    </form>
  );
}

export default TeamSelector;

