export interface UserSummary {
  user: string;
  slack_id: string | null;
  total_checkins: number;
  last_checkin: string | null;
  current_streak: number;
  checked_in_today: boolean;
  activity?: number[];
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  team_id?: number;
  role: string;
  timezone: string;
  last_checkin?: string;
  current_streak: number;
  total_checkins: number;
}

export interface Answer {
  date: string;
  answers: {
    question: string;
    answer: string;
  }[];
} 