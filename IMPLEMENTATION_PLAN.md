# Implementation Plan — New Features for FCAJ Translation Validator

> **How to use this file:** Each checkbox `[ ]` becomes `[x]` once the task is implemented and verified. Copilot will update this file after each successful step.

---

## Architecture Reference (read this first)

```
Admin uploads Excel/CSV
  → UploadFile.py → SQS
  → ExtractContent.py → scrapes AWS blog + Google Doc → S3 (original/ + translated/)
  → MergeAndChunk.py → splits into ~1500-char chunks → S3 (processing/)
  → Step Functions Map: AttachPrompt.py × N chunks (Bedrock Nova Pro + Pinecone RAG) → JSON errors
  → DeduplicateErrors.py → merges + deduplicates
  → SaveErrors.py → DynamoDB (PK=ART#{id}, SK=ERR#{uuid} per error + SK=METADATA)
  → Frontend reads via: GetArticles.py, GetErrors.py, GetMarkDownFromS3.py
```

**DynamoDB schema:**

- `PK=ART#{id}`, `SK=METADATA` → ErrorCount, Status, LastUpdated, RecordType
- `PK=ART#{id}`, `SK=ERR#{uuid}` → ErrorType, Severity, OriginalText, CurrentTranslation, SuggestedFix, Explanation, CreatedAt

**S3 bucket:** `store-aws-blogs-and-translated-version`

- `original/{article_id}.md`, `translated/{article_id}.md`, `processing/{id}/chunk_N.json`

---

## Phase 0 — Article Titles in Dashboard (prerequisite)

### Backend

- [x] **0.1** `lambda/SaveErrors.py` — Add `Title` field to the METADATA item's UpdateExpression (read title from first chunk or S3 original file metadata header)
- [x] **0.2** `lambda/GetArticles.py` — Update Scan to also read `SK=METADATA` items; extract `Title` and `Status` fields; add them to the response per article

### Frontend

- [x] **0.3** `src/types/translation.ts` — Add `title?: string` and `status?: string` to the `Article` interface
- [x] **0.4** `src/views/DashboardPage.vue` — Display `post.title` (fallback to `post.article_id`) in the post card header; show a status badge

### Verify

- [x] **0.5** Dashboard shows article titles instead of raw IDs
- [x] **0.6** Status badge appears on each card (default: "Ready")

---

## Phase 1 — Dashboard Search + Filter Bar

### Frontend

- [x] **1.1** `src/stores/dashboardStore.ts` — Add `searchQuery` ref, `filterSeverity` ref, and `filteredPosts` computed
- [x] **1.2** `src/views/DashboardPage.vue` — Add filter bar UI (text input for search, dropdown for severity filter)
- [x] **1.3** `src/views/DashboardPage.vue` — Loop over `filteredPosts` instead of `posts`
- [x] **1.4** `src/views/DashboardPage.vue` — Add empty-state message when no results match

### Verify

- [x] **1.5** Typing in search box filters articles by title or article_id
- [x] **1.6** Selecting a severity filter shows only articles with that severity > 0

---

## Phase 2A — Review Status Workflow

### Backend

- [x] **2A.1** Create `lambda/UpdateArticleStatus.py` — `PATCH /articles/{article_id}/status`, validates `new_status` is one of `['Ready', 'In Review', 'Approved', 'Published']`, updates DynamoDB METADATA item, requires Cognito JWT
- [x] **2A.2** Wire up API Gateway route `PATCH /articles/{article_id}/status` → Lambda + Cognito authorizer

### Frontend

- [x] **2A.3** `src/stores/translationStore.ts` — Add `updateArticleStatus(articleId, newStatus)` function with auth token
- [x] **2A.4** `src/views/DashboardPage.vue` — Add status dropdown on each post card; on change call `updateArticleStatus`
- [x] **2A.5** `src/views/PostDetailPage.vue` — Show current status in hero card; add "Mark as Approved" button
- [x] **2A.6** `src/stores/dashboardStore.ts` — Add `filterStatus` ref and integrate into `filteredPosts` computed
- [x] **2A.7** `src/views/DashboardPage.vue` — Add status dropdown to filter bar

### Verify

- [x] **2A.8** Changing status in Dashboard persists after page refresh
- [x] **2A.9** Status filter in filter bar works correctly
- [x] **2A.10** "Mark as Approved" button on PostDetailPage updates status

---

## Phase 2B — Save Review Progress

### Backend

- [x] **2B.1** Create `lambda/SaveReviewProgress.py` — `POST /review-progress`, receives `{ article_id, accepted_error_ids, reviewed_by }`, updates METADATA item with `AcceptedErrorIds` list, requires Cognito JWT
- [x] **2B.2** Wire up API Gateway route `POST /review-progress` → Lambda + Cognito authorizer
- [x] **2B.3** `lambda/GetErrors.py` — Also query the METADATA item (SK=METADATA) and include `AcceptedErrorIds` in the response

### Frontend

- [x] **2B.4** `src/stores/translationStore.ts` — Add `saveReviewProgress(articleId, acceptedErrorIds, email)` function
- [x] **2B.5** `src/stores/translationStore.ts` — Update `fetchErrors()` return type to include `accepted_error_ids` from METADATA
- [x] **2B.6** `src/views/PostDetailPage.vue` — Add "Save Progress" button in bulk-actions
- [x] **2B.7** `src/views/PostDetailPage.vue` — On mount, after fetching errors, pre-populate `acceptedErrorIndices` from saved `AcceptedErrorIds`

### Verify

- [x] **2B.8** Accept some fixes → click Save Progress → refresh page → fixes are still ticked
- [x] **2B.9** Save Progress button shows loading state and success feedback

---

## Phase 3 — Export Corrected Markdown

### Frontend (no new Lambda needed)

- [x] **3.1** `src/views/PostDetailPage.vue` — Add `handleExportMarkdown()` function: iterate accepted errors, replace `translated` with `suggestion` in translatedMarkdown, create Blob, trigger download as `{article_id}-corrected.md`
- [x] **3.2** `src/views/PostDetailPage.vue` — Add "Export Corrected .md" button in bulk-actions

### Verify

- [x] **3.3** Clicking export downloads a `.md` file
- [x] **3.4** Exported file contains the corrected text (accepted suggestions applied)
- [x] **3.5** Unaccepted errors remain unchanged in the exported file

---

## Phase 4A — Reviewer Notes

### Backend

- [x] **4A.1** Create `lambda/SaveReviewNote.py` — `POST /articles/{article_id}/notes`, receives `{ note_text }`, writes `PK=ART#{id}`, `SK=NOTE#{timestamp_ms}` with `NoteText`, `WrittenBy` (from JWT), `CreatedAt`; requires Cognito JWT
- [x] **4A.2** Create `lambda/GetReviewNotes.py` — `GET /articles/{article_id}/notes`, queries `SK begins_with NOTE#`, returns sorted list; requires Cognito JWT
- [x] **4A.3** Wire up API Gateway routes for both Lambdas + Cognito authorizer

### Frontend

- [x] **4A.4** `src/stores/translationStore.ts` — Add `saveNote(articleId, noteText)` and `fetchNotes(articleId)` functions
- [x] **4A.5** `src/views/PostDetailPage.vue` — Add Notes section below workspace card: scrollable note list + textarea + "Add Note" button
- [x] **4A.6** `src/views/PostDetailPage.vue` — Load notes on mount via `fetchNotes`; push new note into local array on submit

### Verify

- [x] **4A.7** Adding a note persists after page refresh
- [x] **4A.8** Notes show author email and timestamp
- [x] **4A.9** Notes appear in chronological order

---

## Files Reference

### Existing files to modify

| File                             | Phases        |
| -------------------------------- | ------------- |
| `lambda/GetArticles.py`          | 0             |
| `lambda/SaveErrors.py`           | 0             |
| `lambda/GetErrors.py`            | 2B            |
| `src/types/translation.ts`       | 0             |
| `src/stores/translationStore.ts` | 2A, 2B, 4A    |
| `src/stores/dashboardStore.ts`   | 1, 2A         |
| `src/views/DashboardPage.vue`    | 0, 1, 2A      |
| `src/views/PostDetailPage.vue`   | 2A, 2B, 3, 4A |

### New files to create

| File                            | Phase |
| ------------------------------- | ----- |
| `lambda/UpdateArticleStatus.py` | 2A    |
| `lambda/SaveReviewProgress.py`  | 2B    |
| `lambda/SaveReviewNote.py`      | 4A    |
| `lambda/GetReviewNotes.py`      | 4A    |

---

## Build Order

```
Phase 0  →  Phase 1  →  Phase 2A + 2B (parallel)  →  Phase 3  →  Phase 4A
```

Phase 0 is the foundation (titles + status in DB). Phase 1 only needs frontend. Phases 2A and 2B are independent of each other. Phase 3 needs 2B (save progress). Phase 4A is standalone but benefits from auth patterns established in 2A/2B.
