export interface UserSummary {
  user: string;
  total_checkins: number;
  last_checkin: string | null;
  current_streak: number;
  checked_in_today: boolean;
  activity: number[];
} 