import { useEffect, useState } from "react";
import { fetchEngagementSummary, UserSummary } from "./api/summary";
import UserAnswers from "./components/UserAnswers";

function App() {
  const [summary, setSummary] = useState<UserSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [filtered, setFiltered] = useState<UserSummary[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");

  useEffect(() => {
    fetchEngagementSummary()
      .then((data) => {
        setSummary(data);
        setFiltered(data); // show all by default
      })
      .finally(() => setLoading(false));
  }, []);

  const handleFilterChange = (value: string) => {
    if (value === "all") {
      setFiltered(summary);
    } else if (value === "no-checkin") {
      setFiltered(summary.filter((u) => !u.checked_in_today));
    }
  };

  if (selectedUser) {
    return <UserAnswers email={selectedUser} onBack={() => setSelectedUser(null)} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <header className="bg-white shadow sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">Pulseboard Admin</h1>
          <span className="text-sm text-gray-500">Built with FastAPI + GPT</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Team Check-In Summary</h2>
          <div>
            <label className="mr-2 font-medium">Filter:</label>
            <select
              className="border px-2 py-1 rounded"
              onChange={(e) => handleFilterChange(e.target.value)}
            >
              <option value="all">All Users</option>
              <option value="no-checkin">Only No Check-In Today</option>
            </select>
          </div>
        </div>

        <div className="mb-4">
          <button
            onClick={async () => {
              try {
                const summary = await fetchTeamSummaries();
                const blob = new Blob([summary], { type: "text/plain;charset=utf-8" });
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "pulseboard_team_summary.txt";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              } catch (err) {
                alert("Failed to download summaries!");
              }
            }}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
          >
            📦 Download Team Summaries
          </button>
        </div>

        <div className="mb-4">
          <label htmlFor="search" className="mr-2 font-medium">Search by Email:</label>
          <input
            id="search"
            type="text"
            value={searchQuery}
            onChange={(e) => {
              const query = e.target.value.toLowerCase();
              setSearchQuery(query);
              if (!query) {
                setFiltered(summary); // Reset if search is empty
              } else {
                setFiltered(summary.filter((u) => u.user.toLowerCase().includes(query)));
              }
            }}
            className="border px-3 py-1 rounded w-64"
            placeholder="e.g. maya@startup.com"
          />
        </div>

        {loading ? (
          <p className="text-gray-600">Loading...</p>
        ) : (
          <table className="w-full border mt-4 text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-2 text-left">User</th>
                <th className="p-2 text-center">Total</th>
                <th className="p-2 text-center">Last</th>
                <th className="p-2 text-center">Streak</th>
                <th className="p-2 text-center">Today</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((user) => (
                <tr key={user.user} className="hover:bg-gray-50 border-t">
                  <td className="p-2">
                    <button
                      onClick={() => setSelectedUser(user.user)}
                      className="text-blue-600 hover:underline"
                    >
                      {user.user}
                    </button>
                  </td>
                  <td className="p-2 text-center">{user.total_checkins}</td>
                  <td className="p-2 text-center">{user.last_checkin || "—"}</td>
                  <td className="p-2 text-center">{user.current_streak}</td>
                  <td className="p-2 text-center">{user.checked_in_today ? "✅" : "❌"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </main>
    </div>
  );
}

export default App;