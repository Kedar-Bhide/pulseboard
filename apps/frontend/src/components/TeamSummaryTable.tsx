import React from 'react';
import { Sparklines, SparklinesBars } from "react-sparklines";
import { UserSummary } from '../types/index';

interface TeamSummaryTableProps {
  data: UserSummary[];
  loading: boolean;
  onUserSelect: (email: string) => void;
  sortField: string;
  sortDirection: "asc" | "desc";
  onSort: (field: string) => void;
}

const TeamSummaryTable: React.FC<TeamSummaryTableProps> = ({
  data,
  loading,
  onUserSelect,
  sortField,
  sortDirection,
  onSort,
}) => {
  const sortData = (data: UserSummary[]) => {
    return [...data].sort((a, b) => {
      const valA = a[sortField as keyof UserSummary];
      const valB = b[sortField as keyof UserSummary];
  
      if (typeof valA === "number" && typeof valB === "number") {
        return sortDirection === "asc" ? valA - valB : valB - valA;
      }
  
      return sortDirection === "asc"
        ? String(valA).localeCompare(String(valB))
        : String(valB).localeCompare(String(valA));
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg shadow">
      <table className="w-full border-collapse bg-white">
        <thead className="bg-gray-50">
          <tr>
            <th 
              className="p-4 text-left text-sm font-semibold text-gray-600 cursor-pointer hover:bg-gray-100"
              onClick={() => onSort("user")}
            >
              User {sortField === "user" && (sortDirection === "asc" ? "↑" : "↓")}
            </th>
            <th 
              className="p-4 text-center text-sm font-semibold text-gray-600 cursor-pointer hover:bg-gray-100"
              onClick={() => onSort("total_checkins")}
            >
              Total {sortField === "total_checkins" && (sortDirection === "asc" ? "↑" : "↓")}
            </th>
            <th 
              className="p-4 text-center text-sm font-semibold text-gray-600 cursor-pointer hover:bg-gray-100"
              onClick={() => onSort("last_checkin")}
            >
              Last {sortField === "last_checkin" && (sortDirection === "asc" ? "↑" : "↓")}
            </th>
            <th 
              className="p-4 text-center text-sm font-semibold text-gray-600 cursor-pointer hover:bg-gray-100"
              onClick={() => onSort("current_streak")}
            >
              Streak {sortField === "current_streak" && (sortDirection === "asc" ? "↑" : "↓")}
            </th>
            <th 
              className="p-4 text-center text-sm font-semibold text-gray-600 cursor-pointer hover:bg-gray-100"
              onClick={() => onSort("checked_in_today")}
            >
              Today {sortField === "checked_in_today" && (sortDirection === "asc" ? "↑" : "↓")}
            </th>
            <th className="p-4 text-center text-sm font-semibold text-gray-600">Trend</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {sortData(data).map((user) => (
            <tr key={user.user} className="hover:bg-gray-50 transition-colors">
              <td className="p-4">
                <button
                  onClick={() => onUserSelect(user.user)}
                  className="text-blue-600 hover:text-blue-800 hover:underline font-medium"
                >
                  {user.user}
                </button>
              </td>
              <td className="p-4 text-center">{user.total_checkins}</td>
              <td className="p-4 text-center">{user.last_checkin || "—"}</td>
              <td className="p-4 text-center">
                {user.current_streak > 5 ? (
                  <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">
                    🔥 {user.current_streak} days
                  </span>
                ) : user.current_streak > 0 ? (
                  <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-xs font-medium">
                    {user.current_streak} days
                  </span>
                ) : (
                  <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-xs font-medium">
                    0
                  </span>
                )}
              </td>
              <td className="p-4 text-center">
                {user.checked_in_today ? (
                  <span className="text-green-600">✅</span>
                ) : (
                  <span className="text-red-600">❌</span>
                )}
              </td>
              <td className="p-4 text-center">
                <div className="h-6 w-20 mx-auto">
                  <Sparklines 
                    data={user.activity || [0, 0, 0, 0, 0, 0, 0]} 
                    limit={7} 
                    width={60} 
                    height={20} 
                    margin={2}
                  >
                    <SparklinesBars style={{ fill: "#4299e1" }} />
                  </Sparklines>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TeamSummaryTable; 