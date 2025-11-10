# Engagement Heatmap Test Data Summary

## Overview
Successfully implemented comprehensive test data for the Engagement Heatmap module, which tracks student engagement through attendance, LMS activity, and sentiment analysis to identify at-risk students.

## Implementation Date
November 10, 2025

## Data Created

### Total Records: 733
- **Engagement Heatmaps**: 60 (weekly tracking for 5 students per tenant over 4 weeks)
- **Attendance Records**: 300 (5 days per week for each heatmap)
- **LMS Activities**: 239 (varying by student engagement level)
- **Discussion Sentiments**: 98 (forum posts/replies with sentiment analysis)
- **Engagement Alerts**: 36 (automated alerts for at-risk students)

## Risk Level Distribution

### Engagement Heatmaps by Risk Level:
- **High Risk**: 3 students
- **Medium Risk**: 9 students
- **Low Risk**: 24 students
- **Fully Engaged**: 24 students

### Attendance Status Distribution:
- **Present**: 186 (62%)
- **Late**: 56 (19%)
- **Absent**: 48 (16%)
- **Excused**: 10 (3%)

### LMS Activity Types:
- Quiz Attempts: 44
- Video Watch: 38
- Content View: 36
- Forum Posts: 35
- Assignment Submissions: 31
- Resource Downloads: 30
- Logins: 25

### Discussion Sentiment Analysis:
- Very Positive: 31 (32%)
- Positive: 37 (38%)
- Neutral: 28 (28%)
- Negative: 2 (2%)

### Engagement Alerts by Severity:
- **Critical**: 4
- **High**: 19
- **Medium**: 13

## Key Features Demonstrated

### 1. Composite Engagement Scoring
- **Attendance Score** (40% weight): Based on presence, lateness, and participation
- **LMS Activity Score** (35% weight): Login frequency, content interaction, assignment completion
- **Sentiment Score** (25% weight): Discussion participation and emotional indicators
- **Overall Engagement Score**: Automatically calculated composite score

### 2. Risk Detection
Risk flags automatically triggered for:
- Low attendance (<70%)
- Inactive LMS usage (<60%)
- Negative sentiment (<50%)
- Disengaged students (multiple risk factors)

### 3. Trend Analysis
- **Improving**: Student engagement increasing week-over-week
- **Stable**: Consistent engagement levels
- **Declining**: Gradual decrease in engagement
- **Critical Decline**: Rapid decrease requiring immediate intervention

### 4. Automated Alerts
Alert types generated based on risk factors:
- **Attendance Alerts**: Missing multiple sessions
- **LMS Inactivity**: No login for extended period
- **Negative Sentiment**: Concerning keywords in discussions
- **Overall Engagement**: Multiple metrics below threshold

### 5. Intervention Tracking
- Alert acknowledgement workflow
- Resolution tracking with notes
- Intervention effectiveness monitoring
- Recommended actions for trainers

## Example Student Profile

**Student**: Michael Brown (STU6584)
**Tenant**: Melbourne Training
**Period**: 2025-11-02 to 2025-11-08 (weekly)

### Scores:
- Attendance: 52.5%
- LMS Activity: 53.6%
- Sentiment: 48.9%
- **Overall Engagement: 52.0% (MEDIUM RISK)**

### Risk Indicators:
- **Trend**: Critical decline (-14.5%)
- **Risk Flags**: low_attendance, inactive_lms, negative_sentiment
- **Alerts Triggered**: 3
- **Interventions Applied**: 2

### Active Alerts:
1. [MEDIUM] Negative Sentiment Detected - Recent forum posts show concerning keywords
2. [HIGH] LMS Inactivity Detected - No login for 2+ days
3. [HIGH] Low Attendance Warning - Missed 5 days in the last week

## Heatmap Data Structure

Each engagement heatmap includes a JSON `heatmap_data` field with daily metrics:
```json
{
  "2025-11-02": {
    "attendance": true,
    "lms_minutes": 45,
    "sentiment": 0.6
  },
  "2025-11-03": {
    "attendance": false,
    "lms_minutes": 0,
    "sentiment": -0.3
  }
}
```

## Integration Points

### Attendance Tracking
- Session-level tracking with scheduled vs actual times
- Minutes late and minutes attended
- Participation levels (high/medium/low/none)

### LMS Activity Monitoring
- 9 activity types tracked
- Duration and completion status
- Quality scores for submissions
- Course and module attribution

### Sentiment Analysis
- Sentiment scores (-1 to +1)
- 7 emotion types detected (joy, interest, confusion, frustration, anxiety, anger, sadness)
- Negative keyword detection
- Help-seeking keyword identification
- Word count and question/exclamation tracking

### Alert Management
- 4 severity levels (critical/high/medium/low)
- 4 status types (active/acknowledged/resolved/dismissed)
- Trigger metrics stored as JSON
- Recommended actions array
- Acknowledgement and resolution workflow

## Use Cases

1. **Early Intervention**: Identify at-risk students before they fail
2. **Resource Allocation**: Prioritize trainer support based on severity
3. **Trend Monitoring**: Track engagement changes over time
4. **Compliance**: Document intervention attempts for audit purposes
5. **Data-Driven Decisions**: Use engagement data to improve course design
6. **Student Support**: Proactive outreach to struggling students

## Technical Implementation

### Seed Command Usage
```bash
python manage.py seed_test_data --clear
```

### Models Created
1. `EngagementHeatmap` - Master engagement tracking model
2. `AttendanceRecord` - Daily attendance with session details
3. `LMSActivity` - Learning management system interactions
4. `DiscussionSentiment` - Sentiment analysis of student communications
5. `EngagementAlert` - Automated risk alerts with recommended actions

### Data Generation Approach
- **Realistic distribution**: Mix of high, medium, and low engagement students
- **Varied attendance patterns**: Present, absent, late, excused statuses
- **Activity diversity**: Multiple LMS interaction types
- **Sentiment variety**: Range from very positive to negative
- **Alert correlation**: Alerts match risk levels and flags

## Grand Total Across All Modules

**974 total test records** across 9 major modules:
- Core System: 24
- Authentication & Authorization: 0 (tables not yet migrated)
- Authenticity Check: 25
- Continuous Improvement: 39
- Email Assistant: 69
- **Engagement Heatmap: 733** ⭐
- Assessments & Audit: 27
- Competency & Training: 37
- Adaptive Learning: 20

## Next Steps

1. Run migrations for users_userinvitation and users_emailverification tables
2. Add test data for remaining modules (evidence mapper, risk engine, study coach, etc.)
3. Create visualizations for heatmap data in admin interface
4. Add API endpoints for engagement heatmap queries
5. Implement real-time alert notifications

## Notes

- All engagement data follows realistic patterns (at-risk students show concerning trends)
- Composite scoring weights can be adjusted: attendance (40%), LMS (35%), sentiment (25%)
- Alert recommended actions provide actionable guidance for trainers
- Heatmap data JSON structure supports calendar/grid visualizations
- Sentiment analysis includes confidence scores for reliability tracking
