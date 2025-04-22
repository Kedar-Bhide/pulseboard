export interface UserSummary {
    user: string;
    slack_id: string | null;
    total_checkins: number;
    last_checkin: string | null;
    current_streak: number;
    checked_in_today: boolean;
  }
  
  export async function fetchEngagementSummary(): Promise<UserSummary[]> {
    const res = await fetch("http://localhost:8000/api/v1/admin/engagement-summary");
    if (!res.ok) throw new Error("Failed to fetch engagement summary");
    return res.json();
  }