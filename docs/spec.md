# CalendarAI Consolidated Specification

## Overview
CalendarAI is a Django-based calendar, task, habit, and scheduling platform with an AI "secretary" backed by the OpenAI API. The system supports granular activity tracking, per-user categories, two-way Google Calendar sync with a dedicated calendar, and a multi-agent architecture for scheduling, memory, and task management.

## Goals
- Support close (full activity) or loose (productive-only) scheduling modes per user.
- Track events, tasks, habits, and assignments with category templates.
- Learn user preferences and memories from history and chat.
- Allow auto-scheduling with user-configurable behavior.
- Sync to Google Calendar bidirectionally using a dedicated app calendar.

## Onboarding Flow
1. **Scheduling Style**: Close vs loose scheduling.
2. **Activity Tracking**: Opt-in for full activity tracking (default OFF).
3. **Auto-Schedule Mode**: Off / Suggest / Auto.
4. **Category Menu**: AI suggests categories, user can add/edit/remove.
5. **Google Calendar Connect**: OAuth + two-way sync to a dedicated app calendar.

## Core Data Model
### User Profile
- Scheduling mode (close/loose)
- Activity tracking opt-in
- Auto-schedule mode (off/suggest/auto)
- Confirmation delay seconds (default 60)
- Google sync delay seconds (default 60)
- Preference confidence threshold (default 0.75)
- Inferred profile data (roles, hobbies, preferences)

### Categories
- Per-user categories
- Auto-created from recurring patterns
- Parent/child categories for grouping

### Events
- Instances with start/end, location, duration
- Linked to category templates
- `protected` flag for user-created/edited items
- Source (manual/AI/Google)
- Pending confirmation window for calendar edits

### Tasks and Habits
- Tasks can have subtasks, vague windows, priority, and duration estimates
- Habits support daily/weekly cadence

### Preferences & Memory
- Preferences are stored per-user and per-category
- Memories capture inferred user facts and routines
- Confidence scoring and status (suggested/confirmed/rejected)

### External Calendars
- Google sync state: calendar ID, sync token, last sync time

## Scheduling Rules
### Auto-Schedule Modes
- **Off**: No AI scheduling
- **Suggest**: AI suggests slots; user approves
- **Auto**: AI schedules and waits for confirmation

### Protected Events
- User-created or user-edited events are protected
- AI cannot move protected events without user approval

### Website Edits
- Event changes are marked pending
- Confirm button or auto-confirm after `confirm_delay_seconds`
- Timer resets on subsequent edits

### Google Calendar Edits
- Apply changes immediately based on most recent edit timestamp
- After external edits, reschedule AI-suggested items if conflicts arise
- Delay window is `google_sync_delay_seconds`

## Preferences, Memory, and Learning
### Confidence-based Approval
- Only require approval if confidence < threshold
- Weekly digest for reviewing low-confidence preferences/memories

### Preference Sources
- Calendar history patterns (time, location, duration)
- Chat inputs (explicit preferences)
- Behavior feedback (accepted, moved, rejected suggestions)

### Memory Management
- Users can list, edit, and delete memories/preferences
- Secretary can answer questions about stored preferences

## AI Architecture
Split into specialized agents with shared memory:
- **General Agent**: conversation routing
- **Scheduler Agent**: slotting, conflicts, constraints
- **Task Agent**: task breakdown and subtasks
- **Memory Agent**: preference inference and memory updates

## Google Calendar Sync
- Create and use a dedicated "CalendarAI" calendar
- Two-way sync
- Conflict resolution: newest change wins immediately

## OpenAI API Usage
- Category suggestion generation
- Task breakdown and decomposition
- Schedule proposals
- Preference and memory inference
