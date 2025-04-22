import { useEffect, useState } from "react";
import { fetchEngagementSummary, UserSummary } from "./api/summary";
import UserAnswers from "./components/UserAnswers";

function App() {
  const [summary, setSummary] = useState<UserSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [filtered, setFiltered] = useState<UserSummary[]>([]);

  useEffect(() => {
    fetchEngagementSummary()
      .then((data) => {
        setSummary(data);
        setFiltered(data); // show all by default
      })
      .finally(() => setLoading(false));
  }, []);

  if (selectedUser) {
    return <UserAnswers email={selectedUser} onBack={() => setSelectedUser(null)} />;
  }

  return (
    <main className="p-6 max-w-6xl mx-auto font-sans">
      <h1 className="text-3xl font-bold mb-6">Pulseboard Admin Dashboard</h1>

      <div className="mb-4">
        <label className="mr-2 font-medium">Filter:</label>
        <select
          className="border px-2 py-1 rounded"
          onChange={(e) => {
            const value = e.target.value;
            if (value === "all") setFiltered(summary);
            else if (value === "no-checkin") {
              setFiltered(summary.filter((u) => !u.checked_in_today));
            }
          }}
        >
          <option value="all">All Users</option>
          <option value="no-checkin">Only No Check-In Today</option>
        </select>
      </div>

      {loading ? (
        <p className="text-gray-600">Loading...</p>
      ) : (
        <table className="w-full border mt-4">
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
              <tr key={user.user} className="hover:bg-gray-50">
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
  );
}

export default App;