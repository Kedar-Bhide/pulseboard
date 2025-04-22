export interface UserAnswer {
  id: number;
  answer: string;
  timestamp: string;
  question: string;
}

export async function fetchUserAnswers(userEmail: string): Promise<UserAnswer[]> {
  const res = await fetch(`http://localhost:8000/api/v1/admin/user-answers?email=${userEmail}`);
  if (!res.ok) throw new Error("Failed to fetch user answers");
  return res.json();
}

export interface WeeklySummary {
  summary: string;
}

export async function fetchUserWeeklySummary(userEmail: string): Promise<WeeklySummary> {
  const res = await fetch(`http://localhost:8000/api/v1/admin/weekly-summary?email=${userEmail}`);
  if (!res.ok) throw new Error("Failed to fetch summary");
  return res.json();
}