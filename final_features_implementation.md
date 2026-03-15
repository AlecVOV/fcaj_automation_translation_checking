# **High-Impact Features To Add**

1. **Save Review Decisions**

- Problem solved: accepted fixes are lost on refresh.
- Add API endpoint to persist `acceptedErrorIndices` per `article_id`.
- Integrate in PostDetailPage.vue (`handleAcceptError`, `handleAcceptAll`, `handleResetAll`).

2. **Export Final Corrected Markdown**

- Problem solved: reviewers need final output quickly.
- Add “Export .md / Copy corrected text” button from `CorrectedBlogPreview`.
- Hook into `translatedMarkdown` + accepted suggestions in PostDetailPage.vue.

3. **Dashboard Search + Filters**

- Problem solved: hard to find articles when volume grows.
- Add filter by `article_id`, error count, and severity.
- Implement in DashboardPage.vue using `dashboardStore.posts`.

4. **Terminology Consistency Checker**

- Problem solved: AWS term inconsistency across articles.
- Add glossary rules (forbidden translations + preferred terms).
- Validate during upload/fetch pipeline in translationStore.ts and show warnings in `PostDetailPage`.

5. **Review Status Workflow**

- Add statuses: `new`, `in_review`, `approved`, `published`.
- Display status badges in dashboard cards.
- Helps team collaboration and tracking.

6. **Reviewer Notes + Audit Trail**

- Save who accepted what and when.
- In admin environment this is very useful for QA and rollback confidence.

**Quick Wins (1-2 days)**

1. Add `Save progress` button in `PostDetailPage`.
2. Add `Export corrected markdown` button.
3. Add dashboard filter/search bar.
4. Add “% accepted by severity” mini chart.

**Where To Extend In Current Code**

- Routing and new pages: index.ts
- Review logic and acceptance state: PostDetailPage.vue
- Aggregated listing and stats: DashboardPage.vue, dashboardStore.ts
- API integration layer: translationStore.ts
- Shared typing for new fields (`status`, `reviewed_by`, `reviewed_at`): translation.ts

# **Next Steps**

Here is the full implementation plan. I've read every Lambda and every relevant frontend file. Here's what each does, what's missing, and exactly how to build each feature:

---

## Plan: 5 New Features for AWS Translation Validator

### System Architecture (How it works today)

```
Admin uploads Excel
       ↓
UploadFile.py → SQS
       ↓
ExtractContent.py → scrapes AWS blog + Google Doc → S3 (original/ + translated/)
       ↓
MergeAndChunk.py → splits into 1500-char chunks → S3 (processing/)
       ↓
Step Functions Map (parallel)
  └─ AttachPrompt.py × each chunk → Bedrock Nova Pro + Pinecone RAG → JSON errors
       ↓
DeduplicateErrors.py → merges all chunk results
       ↓
SaveErrors.py → writes DynamoDB
  ├─ PK=ART#{id}, SK=ERR#{uuid} (one per error)
  └─ PK=ART#{id}, SK=METADATA (ErrorCount, Status='Ready', LastUpdated)
       ↓
Frontend reads via:
  GetArticles.py → Dashboard list
  GetErrors.py → PostDetailPage error cards
  GetMarkDownFromS3.py → original + translated text panels
```

---

## Feature 1: Article Titles in Dashboard _(prerequisite for Feature 4)_

**Problem:** GetArticles.py only scans `ERR#` items. The METADATA item (SK=METADATA) already exists in DynamoDB and contains `englishTitle` if saved. The Dashboard shows `Article abc123` with no human-readable title.

**What to change:**

**Backend — GetArticles.py**

- Currently does a full `Scan` with `ProjectionExpression="PK, SK, Severity"` and only reads ERR# items.
- Change: also read SK=METADATA items to get `Title` and `Status`.
- Update the `ProjectionExpression` to `"PK, SK, Severity, #t, #s"` (using ExpressionAttributeNames for `Title` and `Status` reserved words).
- When SK equals `METADATA`, store `title` and `status` on the `dashboard_data[article_id]` object instead of counting it as an error.
- Add `"title": ""`, `"status": "Ready"` fields to `dashboard_data[article_id]` init block.

**Backend — SaveErrors.py**

- Add the English title to the METADATA item when saving.
- The `article_id` is the last slug of the AWS blog URL, but the title is available in the chunk data stored in S3 (`chunk_data` has `original_text` whose first line is the title).
- Read the title from the first line of the first chunk OR parse it from S3 original file metadata header.
- Add `"Title": title_value` to the `update_item` call's `UpdateExpression`.

**Frontend — translation.ts**

- Add `title?: string` and `status?: string` to the `Article` interface.

**Frontend — DashboardPage.vue**

- Replace `Article <code>{{ post.article_id }}</code>` in the template with `{{ post.title || post.article_id }}`.

---

## Feature 2: Save Review Progress

**Problem:** When a reviewer accepts fixes in PostDetailPage.vue, those choices are lost on page refresh. There is no Lambda or API endpoint to persist them.

**What to build:**

**New Lambda — `lambda/SaveReviewProgress.py`**

- Triggered by `POST /review-progress` on API Gateway (requires `Authorization` header = Cognito JWT, same auth pattern as the upload endpoint).
- Receives JSON body: `{ "article_id": "...", "accepted_error_ids": ["ERR#abc123", ...], "reviewed_by": "email@..." }`.
- Calls `table.update_item()` on the METADATA item: `PK=ART#{article_id}`, `SK=METADATA`.
- UpdateExpression: `SET AcceptedErrorIds = :ids, ReviewedBy = :email, ReviewedAt = :now`.
- Returns `{ "status": "success" }`.

**Enhance Lambda — GetErrors.py**

- Currently returns all ERR# items for an article.
- Also query the METADATA item (`SK = 'METADATA'`) in the same DynamoDB call using a `BatchGetItem` or a second `Query`.
- Return `accepted_error_ids` list from METADATA alongside the errors array so the frontend can pre-populate which errors were already accepted.

**Frontend — translationStore.ts**

- Add `saveReviewProgress(articleId, acceptedErrorIds, reviewedByEmail)` async function.
- Uses `getAuthToken()` (already exists in this file) for the `Authorization` header.
- `POST` to `${BASE_URL}/review-progress` with the body.
- Add `loadReviewProgress(articleId)` — called inside `fetchErrors()`, extracts `accepted_error_ids` from the METADATA part of the response.

**Frontend — PostDetailPage.vue**

- Add a `isSaving` ref (boolean) for button state feedback.
- Add a `handleSaveProgress()` async function that calls `translationStore.saveReviewProgress(...)`.
- The accepted error IDs to send are: `acceptedErrorIndices.value.map(i => errors.value[i].id)`.
- On `onMounted`, after fetching errors, call `loadReviewProgress` and pre-populate `acceptedErrorIndices` based on which error IDs come back as accepted.
- Add a "Save Progress" button in the `bulk-actions` div, next to "Accept all suggestions", styled similar to `bulk-btn`.

---

## Feature 3: Export Corrected Markdown

**Problem:** After a reviewer accepts fixes, there is no way to download the final corrected document. The corrected content already exists in `CorrectedBlogPreview.vue` but is not exportable.

**No new Lambda needed** — this is pure frontend work.

**What to change:**

**CorrectedBlogPreview.vue** (need to read this file first)

- Add a `defineEmits` or `defineExpose` to expose the current corrected markdown text as a string.
- Or emit it upward via an event `@corrected-text-change` whenever the computed corrected text changes.

**Frontend — PostDetailPage.vue**

- Capture the corrected markdown text (from a ref updated by the emit above, or computed directly in this file by replicating the replacement logic).
- Add `handleExportMarkdown()` function:
  ```
  1. Build the corrected text: start from translatedMarkdown.value
  2. For each accepted error index i:
     - Find errors.value[i].translated (the bad text)
     - Replace with errors.value[i].suggestion (the fix)
  3. Create a Blob of type 'text/markdown'
  4. Create a temporary anchor element, set href=URL.createObjectURL(blob)
  5. Set download attribute to `${post.value.article_id}-corrected.md`
  6. Click and revoke URL
  ```
- Add "⬇ Export Corrected .md" button in the `bulk-actions` div.

---

## Feature 4: Dashboard Search, Filter, and Status Badges

**Problem:** The Dashboard at DashboardPage.vue shows all articles in a plain list with no way to filter by status, error count, or search by name/ID. As volume grows this becomes unusable.

**No new Lambda needed** — all filtering happens in the frontend using `dashboardStore.posts`.

**What to change:**

**Frontend — dashboardStore.ts**

- Add a `searchQuery` ref (string).
- Add a `filterStatus` ref (string: `'all' | 'Ready' | 'In Review' | 'Approved'`).
- Add `filterSeverity` ref (string: `'all' | 'critical' | 'major' | 'minor'`).
- Add a `filteredPosts` computed that filters `posts.value` using those three refs.

**Frontend — DashboardPage.vue**

- Add a filter bar above the posts grid with:
  - Text input bound to `dashboardStore.searchQuery` (filters by title/article_id).
  - Dropdown bound to `dashboardStore.filterStatus`.
  - Dropdown bound to `dashboardStore.filterSeverity` (shows only articles with critical/major/minor > 0).
- Loop over `dashboardStore.filteredPosts` instead of `dashboardStore.posts`.
- Show a `Status` badge on each post card using `post.status` (from Feature 1). Color: `Ready=gray`, `In Review=orange`, `Approved=green`.
- Add a "no results" empty state when `filteredPosts.length === 0`.

---

## Feature 5: Review Status Workflow

**Problem:** There is no way for reviewers to move an article through stages (`Ready → In Review → Approved`). The `Status` field on the METADATA DynamoDB item exists (SaveErrors.py sets it to `'Ready'`) but there is no API to update it.

**New Lambda — `lambda/UpdateArticleStatus.py`**

- Triggered by `PATCH /articles/{article_id}/status` on API Gateway (requires Cognito JWT auth).
- Gets `article_id` from `pathParameters`.
- Gets `new_status` from JSON body: must be one of `['Ready', 'In Review', 'Approved', 'Published']`. Validate this — reject anything else to prevent injection.
- Gets `updated_by` from the decoded JWT claims (use `event['requestContext']['authorizer']['claims']['email']`).
- Calls `table.update_item()` on `PK=ART#{article_id}`, `SK=METADATA`:
  - UpdateExpression: `SET #s = :status, LastUpdated = :now, UpdatedBy = :user`
- Returns `{ "status": "success", "new_status": new_status }`.

**Frontend — translationStore.ts**

- Add `updateArticleStatus(articleId, newStatus)` async function using `getAuthToken()`.
- `PATCH` to `${BASE_URL}/articles/${articleId}/status` with body `{ new_status: newStatus }`.
- On success, update the matching article in `articles.value` locally so the UI updates without a full re-fetch.

**Frontend — DashboardPage.vue**

- On each post card, add a status dropdown (`<select>`) with options: `Ready`, `In Review`, `Approved`, `Published`.
- On change, call `translationStore.updateArticleStatus(post.article_id, newValue)`.
- Show a brief success toast or inline green tick when saved.

**Frontend — PostDetailPage.vue**

- Show current article status in the hero card.
- Add a "Mark as Approved" button that calls `updateArticleStatus` with `'Approved'` and triggers a success banner.

---

## Feature 6: Reviewer Notes

**Problem:** Reviewers have no way to leave comments or notes attached to an article that other team members can see.

**New Lambda — `lambda/SaveReviewNote.py`**

- Triggered by `POST /articles/{article_id}/notes` (requires Cognito JWT).
- Receives: `{ "note_text": "..." }`.
- Gets `written_by` from JWT claims email.
- Writes to DynamoDB: `PK=ART#{article_id}`, `SK=NOTE#{timestamp_ms}` with fields `NoteText`, `WrittenBy`, `CreatedAt`.
- Returns the saved note object.

**New Lambda — `lambda/GetReviewNotes.py`**

- Triggered by `GET /articles/{article_id}/notes` (requires Cognito JWT).
- Queries DynamoDB: `PK=ART#{article_id}` AND `SK begins_with NOTE#`.
- Returns sorted list of notes.

**Frontend — translationStore.ts**

- Add `saveNote(articleId, noteText)` — POSTs with auth.
- Add `fetchNotes(articleId)` — GETs with auth, returns note array.

**Frontend — PostDetailPage.vue**

- Add a new `<section class="notes-panel">` below the workspace card.
- Contains a scrollable list of existing notes (loaded in `onMounted` via `fetchNotes`).
- A textarea + "Add Note" button at the bottom.
- On submit, call `saveNote` then push the returned note into the local notes array.

---

## Relevant Files

- GetArticles.py — modify to return title + status from METADATA items
- SaveErrors.py — add Title to METADATA save
- GetErrors.py — also return METADATA (accepted_error_ids)
- translation.ts — add `title`, `status`, `accepted_error_ids` to `Article`
- translationStore.ts — add `saveReviewProgress`, `loadReviewProgress`, `updateArticleStatus`, `saveNote`, `fetchNotes`
- dashboardStore.ts — add filter/search refs and `filteredPosts` computed
- DashboardPage.vue — filter bar, status badges, status dropdown
- PostDetailPage.vue — Save Progress button, Export button, Status button, Notes panel
- CorrectedBlogPreview.vue — expose corrected text

**New files to create:**

- `lambda/SaveReviewProgress.py`
- `lambda/UpdateArticleStatus.py`
- `lambda/SaveReviewNote.py`
- `lambda/GetReviewNotes.py`

---

## Build Order (Dependencies matter)

| Phase       | What                                                       | Depends on                                |
| ----------- | ---------------------------------------------------------- | ----------------------------------------- |
| **Phase 0** | Feature 1 (Titles in Dashboard)                            | nothing — small backend + frontend change |
| **Phase 1** | Feature 4 frontend filter bar (without status)             | Phase 0                                   |
| **Phase 2** | Feature 5 (Status Workflow) — Lambda + API + frontend      | Phase 0                                   |
| **Phase 2** | Feature 2 (Save Review Progress) — Lambda + API + frontend | nothing independent                       |
| **Phase 3** | Feature 3 (Export .md)                                     | Feature 2 (so progress is saved first)    |
| **Phase 4** | Feature 6 (Notes) — 2 new Lambdas + frontend               | Phase 2 (auth pattern established)        |
| **Phase 4** | Feature 4 status filter                                    | Phase 2 (status data now exists)          |

---

## Verification Checklist

1. Dashboard shows article titles and status badges after Phase 0.
2. Filter bar narrows down the list correctly for text search and severity filter.
3. Accepting fixes → clicking Save Progress → refreshing page → fixes are still ticked.
4. Exporting downloads a `.md` file where accepted fixes replaced the original bad text.
5. Changing status in Dashboard from `Ready` to `In Review` persists after refresh.
6. Notes saved by one reviewer are visible to another admin after page reload.
7. All new Lambda endpoints return 403 if `Authorization` header is missing (security check).
