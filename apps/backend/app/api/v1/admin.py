from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.security import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.answer import Answer

router = APIRouter()

@router.get("/engagement-summary")
def get_engagement_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """
    Get engagement summary for all users
    """
    # Check if user is admin
    if current_user.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = db.query(User).all()
    today = datetime.utcnow().date()
    
    summary = []
    for user in users:
        # Get last check-in
        last_checkin = None
        if user.last_checkin:
            last_checkin = user.last_checkin.isoformat()
        
        # Check if user checked in today
        checked_in_today = False
        if user.last_checkin:
            checked_in_today = user.last_checkin.date() == today
        
        summary.append({
            "user": user.email,
            "slack_id": user.slack_id,
            "total_checkins": user.total_checkins,
            "last_checkin": last_checkin,
            "current_streak": user.current_streak,
            "checked_in_today": checked_in_today
        })
    
    return summary

@router.get("/team-summaries")
def get_team_summaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, str]:
    """
    Get team summaries
    """
    # Check if user is admin
    if current_user.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = db.query(User).all()
    today = datetime.utcnow().date()
    
    summary_lines = []
    summary_lines.append("PulseBoard Team Summary")
    summary_lines.append("=" * 50)
    summary_lines.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    summary_lines.append("")
    
    for user in users:
        checked_in_today = "✓" if (user.last_checkin and user.last_checkin.date() == today) else "✗"
        summary_lines.append(f"{user.full_name} ({user.email}) - Today: {checked_in_today}")
        summary_lines.append(f"  Total Check-ins: {user.total_checkins}")
        summary_lines.append(f"  Current Streak: {user.current_streak}")
        if user.last_checkin:
            summary_lines.append(f"  Last Check-in: {user.last_checkin.strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append("")
    
    full_summary = "\n".join(summary_lines)
    return {"full_summary": full_summary}

@router.get("/batch-activity")
def get_batch_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, List[int]]:
    """
    Get batch activity for all users (last 7 days)
    """
    # Check if user is admin
    if current_user.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = db.query(User).all()
    today = datetime.utcnow().date()
    
    activity_data = {}
    for user in users:
        # Generate mock activity data for last 7 days
        # In a real implementation, this would query actual answer data
        activity = []
        for i in range(7):
            check_date = today - timedelta(days=6-i)
            # Mock: user has activity if they have a last_checkin on that date
            has_activity = 1 if (user.last_checkin and user.last_checkin.date() == check_date) else 0
            activity.append(has_activity)
        
        activity_data[user.email] = activity
    
    return {"activity": activity_data} 