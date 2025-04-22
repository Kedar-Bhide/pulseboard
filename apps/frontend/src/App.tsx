import { useEffect, useState } from "react";
import { fetchEngagementSummary, UserSummary } from "./api/summary";

function App() {
  const [summary, setSummary] = useState<UserSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEngagementSummary()
      .then(setSummary)
      .finally(() => setLoading(false));
  }, []);

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Pulseboard Admin Dashboard</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table border={1} cellPadding={8} style={{ marginTop: "1rem" }}>
          <thead>
            <tr>
              <th>User</th>
              <th>Total Check-Ins</th>
              <th>Last Check-In</th>
              <th>Streak</th>
              <th>Checked In Today?</th>
            </tr>
          </thead>
          <tbody>
            {summary.map((user) => (
              <tr key={user.user}>
                <td>{user.user}</td>
                <td>{user.total_checkins}</td>
                <td>{user.last_checkin || "—"}</td>
                <td>{user.current_streak}</td>
                <td>{user.checked_in_today ? "✅" : "❌"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}

export default App;