import { useEffect, useState } from "react";
import { fetchEngagementSummary, fetchTeamSummaries, fetchBatchActivity } from "./api/summary";
import UserAnswers from "./components/UserAnswers";
import Layout from "./components/Layout";
import TeamSummaryTable from "./components/TeamSummaryTable";
import { UserSummary } from "./types";

function App() {
  const [summary, setSummary] = useState<UserSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [filtered, setFiltered] = useState<UserSummary[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [sortField, setSortField] = useState<string>("user");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");

  useEffect(() => {
    fetchEngagementSummary()
      .then(async (data) => {
        const batchActivity = await fetchBatchActivity();
        const updatedData = data.map(user => ({
          ...user,
          activity: batchActivity[user.user] || [0, 0, 0, 0, 0, 0, 0],
        }));
        setSummary(updatedData);
        setFiltered(updatedData);
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

  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  if (selectedUser) {
    return <UserAnswers email={selectedUser} onBack={() => setSelectedUser(null)} />;
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">Team Check-In Summary</h2>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  const query = e.target.value.toLowerCase();
                  setSearchQuery(query);
                  if (!query) {
                    setFiltered(summary);
                  } else {
                    setFiltered(summary.filter((u) => u.user.toLowerCase().includes(query)));
                  }
                }}
                placeholder="Search by email..."
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <svg
                className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <select
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              onChange={(e) => handleFilterChange(e.target.value)}
            >
              <option value="all">All Users</option>
              <option value="no-checkin">No Check-In Today</option>
            </select>
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
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              <span>Download Summary</span>
            </button>
          </div>
        </div>

        <TeamSummaryTable
          data={filtered}
          loading={loading}
          onUserSelect={setSelectedUser}
          sortField={sortField}
          sortDirection={sortDirection}
          onSort={handleSort}
        />
      </div>
    </Layout>
  );
}

export default App;