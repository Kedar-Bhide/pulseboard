import { useEffect, useState } from "react";
import { fetchUserAnswers, UserAnswer } from "../api/user";

export default function UserAnswers({ email, onBack }: { email: string; onBack: () => void }) {
  const [answers, setAnswers] = useState<UserAnswer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserAnswers(email).then(setAnswers).finally(() => setLoading(false));
  }, [email]);

  return (
    <div style={{ padding: "1rem" }}>
      <button onClick={onBack}>⬅️ Back</button>
      <h2>Check-ins for {email}</h2>
      {loading ? <p>Loading...</p> : (
        <ul>
          {answers.map(ans => (
            <li key={ans.id} style={{ marginBottom: "1rem" }}>
              <b>{new Date(ans.timestamp).toLocaleString()}</b><br />
              <i>Q: {ans.question}</i><br />
              <p>A: {ans.answer}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}