const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface UserSummary {
  user: string;
  slack_id: string | null;
  total_checkins: number;
  last_checkin: string | null;
  current_streak: number;
  checked_in_today: boolean;
  activity?: number[];
}
  
export async function fetchEngagementSummary(): Promise<UserSummary[]> {
  const res = await fetch(`${API_URL}/admin/engagement-summary`);
  if (!res.ok) throw new Error("Failed to fetch engagement summary");
  return res.json();
}

export async function fetchTeamSummaries(): Promise<string> {
  const res = await fetch(`${API_URL}/admin/team-summaries`);
  if (!res.ok) throw new Error("Failed to fetch team summaries");
  const data = await res.json();
  return data.full_summary;
}

export async function fetchBatchActivity(): Promise<{ [email: string]: number[] }> {
  const res = await fetch(`${API_URL}/admin/batch-activity`);
  if (!res.ok) throw new Error("Failed to fetch batch activity");
  const data = await res.json();
  return data.activity;
}