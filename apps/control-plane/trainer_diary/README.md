# Trainer Diary Writer - Feature Documentation

## Overview
The Trainer Diary Writer is the second tool in the TrainAI Suite, designed to automate teaching session documentation through speech-to-text transcription and AI-powered summarization.

## Features

### 1. Session Recording
- Record teaching session details (date, duration, course, students)
- Capture delivery mode (face-to-face, online, blended, workplace)
- Manual note-taking interface
- Track learning outcomes and assessment activities

### 2. Speech-to-Text Transcription
- Upload audio recordings (MP3, WAV, M4A formats)
- Automatic transcription using speech-to-text engines
- Support for multiple transcription engines:
  - OpenAI Whisper (default)
  - Google Speech-to-Text
  - Azure Speech Service
  - AWS Transcribe
- Confidence scoring for transcription quality
- Speaker diarization support

### 3. AI-Powered Summarization
- Automatic session summarization using LLMs
- Extract key topics covered
- Generate follow-up action items
- Identify learning outcomes addressed
- Multiple summary styles (brief, detailed, evidence-focused)
- Integration with transcript and manual notes

### 4. Daily Evidence Creation
- Aggregate daily teaching activities
- Calculate total sessions, hours, and students
- Generate daily highlights and achievements
- Track courses taught
- Compliance-ready evidence documentation

### 5. Evidence Document Generation
- Multiple document types:
  - Session Plans
  - Attendance Records
  - Teaching Evidence
  - Assessment Records
  - Student Feedback Summaries
  - Compliance Reports
  - Professional Reflections
- Export formats: Markdown, HTML, PDF, Word
- Automatic compliance tagging

## Technical Implementation

### Backend (Django)

#### Models (5 models)
1. **DiaryEntry**: Main diary records with session details, transcripts, and AI summaries
2. **AudioRecording**: Audio file management with transcription results
3. **DailySummary**: Aggregated daily teaching statistics
4. **EvidenceDocument**: Generated evidence documents for compliance
5. **TranscriptionJob**: Queue management for speech-to-text processing

#### API Endpoints
- `POST /api/trainer-diary/diary-entries/` - Create diary entry
- `POST /api/trainer-diary/diary-entries/upload-audio/` - Upload audio file
- `POST /api/trainer-diary/diary-entries/transcribe-audio/` - Start transcription
- `POST /api/trainer-diary/diary-entries/generate-summary/` - Generate AI summary
- `POST /api/trainer-diary/diary-entries/create-daily-summary/` - Create daily summary
- `POST /api/trainer-diary/diary-entries/generate-evidence/` - Generate evidence document
- `GET /api/trainer-diary/diary-entries/dashboard/` - Dashboard statistics
- `POST /api/trainer-diary/diary-entries/export-evidence/` - Export evidence

#### Database Migrations
- Applied successfully: `trainer_diary.0001_initial`
- 5 models created with indexes and relationships

### Frontend (Next.js)

#### Page Structure
- **Location**: `/apps/web-portal/src/app/dashboard/[tenantSlug]/trainer-diary/page.tsx`
- **Size**: 1,050+ lines of TypeScript/React
- **Technology**: Plain HTML with Tailwind CSS (no shadcn UI)

#### Tabs (6 tabs)
1. **Record Session**: Form to log teaching session details
2. **Upload Audio**: Audio file upload with drag-drop interface
3. **Sessions**: List of all diary entries with summaries
4. **Transcripts**: View audio transcriptions and processing status
5. **Daily Summaries**: Aggregated daily teaching statistics
6. **Evidence**: Generated evidence documents

#### Dashboard Integration
- Card added to TrainAI Suite section
- Teal/cyan gradient styling matching suite theme
- Badge: "🎤 Speech-to-Text + AI"
- Route: `/dashboard/[tenantSlug]/trainer-diary`

## Data Flow

### Audio to Summary Flow
1. Trainer records teaching session (manual entry)
2. Uploads audio recording of session
3. System queues transcription job
4. Speech-to-text engine processes audio
5. Transcript stored with confidence score
6. LLM generates summary from transcript + manual notes
7. Key topics and action items extracted
8. Evidence documents generated on demand

### Daily Summary Flow
1. Trainer completes multiple sessions in a day
2. System aggregates all completed entries for the date
3. Calculates statistics (sessions, hours, students, courses)
4. Generates daily highlights and achievements
5. Creates compliance-ready daily evidence

## Compliance & Evidence

### RTO Standards Support
- Maintains detailed teaching records
- Tracks learning outcomes addressed
- Documents assessment activities
- Records student engagement metrics
- Generates audit-ready evidence

### Evidence Types
- Teaching Evidence: Session details with AI summaries
- Session Plans: Structured lesson documentation
- Professional Reflections: Trainer insights and improvements
- Attendance Records: Student participation tracking
- Compliance Reports: Standards alignment verification

## AI Integration

### Speech-to-Text
- Primary: OpenAI Whisper API
- Fallback: Google, Azure, AWS engines
- Language support: English (extensible)
- Accuracy tracking via confidence scores

### Summarization
- Primary: GPT-4 (configurable)
- Input: Transcript + manual notes + metadata
- Output: 
  - Session summary (paragraph)
  - Key topics (list)
  - Follow-up actions (list)
  - Learning outcomes addressed
- Token usage tracking

## Status Tracking

### Entry Statuses
- **draft**: Initial creation, no processing
- **transcribing**: Audio being transcribed
- **summarizing**: AI generating summary
- **complete**: Fully processed with summary
- **archived**: Historical records

### Recording Statuses
- **uploaded**: File received, not processed
- **queued**: Waiting for transcription
- **processing**: Transcription in progress
- **completed**: Transcription finished
- **failed**: Processing error

## Dashboard Statistics
- Total diary entries
- Entries this week/month
- Total teaching hours
- Total students taught
- Audio recordings count
- Pending transcriptions
- Daily summaries count
- Evidence documents count

## Visual Design
- Color scheme: Teal/cyan gradient (matching TrainAI Suite)
- Icons: Emoji-based (🎤 📝 💬 📅 📋)
- Layout: Responsive grid with cards
- Status badges: Color-coded by state
- Progress indicators: For currency tracking

## Next Steps (Future Enhancements)
1. Real-time transcription during live sessions
2. Multi-speaker identification in recordings
3. Integration with calendar for automatic session scheduling
4. Bulk export of evidence portfolios
5. Email notifications for completed transcriptions
6. Video recording support
7. Integration with learning management systems
8. Automatic tagging based on content analysis

## File Locations

### Backend
- Models: `/apps/control-plane/trainer_diary/models.py`
- Views: `/apps/control-plane/trainer_diary/views.py`
- Serializers: `/apps/control-plane/trainer_diary/serializers.py`
- URLs: `/apps/control-plane/trainer_diary/urls.py`
- Admin: `/apps/control-plane/trainer_diary/admin.py`
- Tests: `/apps/control-plane/trainer_diary/tests.py`
- Migrations: `/apps/control-plane/trainer_diary/migrations/0001_initial.py`

### Frontend
- Main Page: `/apps/web-portal/src/app/dashboard/[tenantSlug]/trainer-diary/page.tsx`
- Dashboard Card: `/apps/web-portal/src/app/dashboard/[tenantSlug]/page.tsx` (lines 498-512)

### Configuration
- Settings: `/apps/control-plane/control_plane/settings.py` (trainer_diary added to INSTALLED_APPS)
- URLs: `/apps/control-plane/control_plane/urls.py` (trainer_diary routes registered)

## API Examples

### Create Diary Entry
```bash
POST /api/trainer-diary/diary-entries/
{
  "tenant": "demo-rto",
  "trainer_id": "trainer-001",
  "trainer_name": "John Smith",
  "session_date": "2024-01-15",
  "course_name": "Certificate IV in Training and Assessment",
  "course_code": "TAE40116",
  "student_count": 15,
  "session_duration_minutes": 180,
  "delivery_mode": "face_to_face",
  "manual_notes": "Session covered design principles..."
}
```

### Upload Audio
```bash
POST /api/trainer-diary/diary-entries/upload-audio/
FormData: {
  "diary_entry_id": 123,
  "audio_file": <file>,
  "recording_filename": "session_2024_01_15.mp3",
  "language": "en"
}
```

### Generate Summary
```bash
POST /api/trainer-diary/diary-entries/generate-summary/
{
  "diary_entry_id": 123,
  "include_transcript": true,
  "include_manual_notes": true,
  "summary_style": "detailed"
}
```

## Testing
- Unit tests: `/apps/control-plane/trainer_diary/tests.py`
- Test coverage:
  - Model creation and validation
  - Auto-generated unique identifiers
  - Relationships between models
  - Unique constraints on daily summaries

## Deployment Status
✅ Backend: Complete and migrated
✅ Frontend: Complete with no errors
✅ Database: Tables created successfully
✅ Dashboard: Card added to TrainAI Suite
✅ Visual Design: Matches TrainAI Suite theme
✅ API Endpoints: All routes registered
✅ Admin Interface: Full CRUD support

---

**TrainAI Suite Progress:**
- Tool 1: PD Tracker ✅ Complete
- Tool 2: Trainer Diary Writer ✅ Complete
- Tool 3: TBD
- Tool 4: TBD
