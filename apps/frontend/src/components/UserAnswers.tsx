import { useEffect, useState } from "react";
import { fetchUserAnswers, UserAnswer, fetchUserWeeklySummary, WeeklySummary } from "../api/user";

export default function UserAnswers({ email, onBack }: { email: string; onBack: () => void }) {
  const [answers, setAnswers] = useState<UserAnswer[]>([]);
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchUserAnswers(email),
      fetchUserWeeklySummary(email),
    ])
      .then(([ans, summaryData]) => {
        setAnswers(ans);
        setSummary(summaryData.summary);
      })
      .finally(() => setLoading(false));
  }, [email]);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <button onClick={onBack} className="text-blue-600 hover:underline mb-4">⬅️ Back</button>
      <h2 className="text-2xl font-bold mb-4">Check-ins for {email}</h2>

      {loading ? (
        <p className="text-gray-600">Loading...</p>
      ) : (
        <>
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded shadow">
            <h3 className="font-semibold mb-2">🧠 Weekly Summary</h3>
            <p className="text-gray-800 whitespace-pre-line">{summary}</p>
          </div>

          {summary && (
            <div className="mb-6 flex justify-end">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(`Weekly Summary for ${email}:\n\n${summary}`);
                  alert("Summary copied to clipboard!");
                }}
                className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
              >
                📋 Copy Summary
              </button>
            </div>
          )}

          <ul className="space-y-4">
            {answers.map(ans => (
              <li key={ans.id} className="p-4 border border-gray-300 rounded shadow-sm hover:shadow-md transition-shadow">
                <p className="text-sm text-gray-500">{new Date(ans.timestamp).toLocaleString()}</p>
                <p className="text-gray-700 italic">Q: {ans.question}</p>
                <p className="text-gray-900 mt-2">A: {ans.answer}</p>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}