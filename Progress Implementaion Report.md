# Adding New Features Reports — Version 1

**Project:** FCAJ Translation Validator  
**Period:** March 18, 2026  
**Author:** Admin

---

## 1. Completed Tasks

| #          | Task                                                     | Status  | Action / Notes                                                                                                                                                                             | Time Spent |
| ---------- | -------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| 0.1        | `SaveErrors.py` — Add Title to METADATA                  | ✅ Done | Added `get_article_title()` reading from S3 original file metadata; added `Title` to UpdateExpression                                                                                      | ~30 min    |
| 0.2        | `GetArticles.py` — Return Title & Status                 | ✅ Done | Updated Scan to include `Title, #s` with ExpressionAttributeNames; extract from METADATA item, skip error counting for METADATA SK                                                         | ~30 min    |
| 0.3        | `translation.ts` — Add title/status to Article interface | ✅ Done | Added `title?: string` and `status?: string`                                                                                                                                               | ~5 min     |
| 0.4        | `DashboardPage.vue` — Display title & status badge       | ✅ Done | Show `post.title` with fallback to `post.article_id`; added colored status badge                                                                                                           | ~20 min    |
| 0.5–0.6    | Phase 0 verification                                     | ✅ Done | Titles and status badges visible on dashboard                                                                                                                                              | ~10 min    |
| 1.1        | `dashboardStore.ts` — Search & filter state              | ✅ Done | Added `searchQuery`, `filterSeverity` refs and `filteredPosts` computed                                                                                                                    | ~15 min    |
| 1.2        | `DashboardPage.vue` — Filter bar UI                      | ✅ Done | Text input for search, dropdown for severity                                                                                                                                               | ~15 min    |
| 1.3        | `DashboardPage.vue` — Use filteredPosts                  | ✅ Done | Replaced `posts` loop with `filteredPosts`                                                                                                                                                 | ~5 min     |
| 1.4        | `DashboardPage.vue` — Empty state                        | ✅ Done | "No articles match" message + Clear Filters button                                                                                                                                         | ~10 min    |
| 1.5–1.6    | Phase 1 verification                                     | ✅ Done | Search and severity filter working                                                                                                                                                         | ~10 min    |
| 2A.1       | `UpdateArticleStatus.py` — New Lambda                    | ✅ Done | POST endpoint; validates status in `['Ready','In Review','Approved','Published']`; updates DynamoDB METADATA; reads reviewer from JWT                                                      | ~30 min    |
| 2A.2       | API Gateway — `/update-status` route                     | ✅ Done | Created resource, POST method, Lambda proxy integration, Cognito authorizer, CORS, deployed to `dev` stage. **Debugging:** proxy integration was initially missing, causing 400/502 errors | ~45 min    |
| 2A.3       | `translationStore.ts` — `updateArticleStatus()`          | ✅ Done | POST with Cognito JWT; updates local articles array for instant UI feedback                                                                                                                | ~15 min    |
| 2A.4       | `DashboardPage.vue` — Status dropdown per card           | ✅ Done | `<select>` with colored classes; guarded `@change` to prevent re-render triggers                                                                                                           | ~20 min    |
| 2A.5       | `PostDetailPage.vue` — Status in hero + Approve button   | ✅ Done | Status badge in eyebrow row; "Mark as Approved" button hidden when already approved/published                                                                                              | ~20 min    |
| 2A.6       | `dashboardStore.ts` — `filterStatus` ref                 | ✅ Done | Added to `filteredPosts` computed alongside search and severity                                                                                                                            | ~10 min    |
| 2A.7       | `DashboardPage.vue` — Status filter dropdown             | ✅ Done | Third dropdown in filter bar: All / Ready / In Review / Approved / Published                                                                                                               | ~10 min    |
| 2A.8–2A.10 | Phase 2A verification                                    | ✅ Done | Status persists on refresh, filter works, Approve button works. **Required debugging:** Lambda IAM policy, proxy integration, CORS headers                                                 | ~60 min    |
| 2B.1       | `SaveReviewProgress.py` — New Lambda                     | ✅ Done | POST `/review-progress`; receives `article_id` + `accepted_error_ids`; updates METADATA with `AcceptedErrorIds` list                                                                       | ~20 min    |
| 2B.2       | API Gateway — `/review-progress` route                   | ✅ Done | Same setup pattern as `/update-status`: POST + proxy + Cognito + CORS                                                                                                                      | ~15 min    |
| 2B.3       | `GetErrors.py` — Return AcceptedErrorIds                 | ✅ Done | Added `get_item` for METADATA; includes `accepted_error_ids` in response                                                                                                                   | ~15 min    |
| 2B.4       | `translationStore.ts` — `saveReviewProgress()`           | ✅ Done | POST with JWT auth; sends accepted error ID list                                                                                                                                           | ~10 min    |
| 2B.5       | `translationStore.ts` — `fetchErrors` return type        | ✅ Done | No code change needed; existing function returns full JSON body including new field                                                                                                        | ~5 min     |
| 2B.6       | `PostDetailPage.vue` — Save Progress button              | ✅ Done | Blue button in bulk-actions; maps accepted indices to error IDs; shows loading + feedback message                                                                                          | ~15 min    |
| 2B.7       | `PostDetailPage.vue` — Pre-populate on mount             | ✅ Done | Reads `errData.accepted_error_ids`, builds index set, restores `acceptedErrorIndices`. **Bug fixed:** initially placed outside `onMounted` causing `errData is not defined`                | ~20 min    |
| 2B.8–2B.9  | Phase 2B verification                                    | ✅ Done | Accepted fixes persist after refresh; button shows loading state and "Progress saved!"                                                                                                     | ~15 min    |
| —          | Prompt translation (PromptGenerated.vue)                 | ✅ Done | Converted Vietnamese AI prompt to simplified English                                                                                                                                       | ~15 min    |
| —          | Prompt translation (MultiBlogPromptGenerator.vue)        | ✅ Done | Converted Vietnamese batch-scoring prompt to English                                                                                                                                       | ~15 min    |
| —          | ESLint / TypeScript error diagnosis                      | ✅ Done | Explained `isAdminRoute` unused warning and `no-explicit-any` rule from oxlint config                                                                                                      | ~10 min    |
| —          | Auth headers for all GET endpoints                       | ✅ Done | Added `getAuthToken()` + `Authorization` header to `fetchTranslations` and `fetchErrors`; updated Lambda CORS headers to allow `Authorization`                                             | ~15 min    |

**Total estimated time: ~9 hours**

---

## 2. Plan for Next Week

| #         | Task                                                  | Phase    | Priority | Expected Outcome                                                                                                    |
| --------- | ----------------------------------------------------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------- |
| 3.1       | Add `handleExportMarkdown()` to PostDetailPage        | Phase 3  | High     | Function iterates accepted errors, replaces translated text with suggestions, creates Blob, triggers `.md` download |
| 3.2       | Add "Export Corrected .md" button                     | Phase 3  | High     | Button in bulk-actions bar next to Save Progress                                                                    |
| 3.3–3.5   | Phase 3 verification                                  | Phase 3  | High     | Downloaded file contains corrected text for accepted fixes; unaccepted errors unchanged                             |
| 4A.1      | Create `SaveReviewNote.py` Lambda                     | Phase 4A | Medium   | POST endpoint writes `PK=ART#{id}, SK=NOTE#{timestamp}` with NoteText, WrittenBy, CreatedAt                         |
| 4A.2      | Create `GetReviewNotes.py` Lambda                     | Phase 4A | Medium   | GET endpoint queries `SK begins_with NOTE#`, returns sorted note list                                               |
| 4A.3      | Wire up API Gateway routes for notes                  | Phase 4A | Medium   | Two new routes with Cognito auth + CORS                                                                             |
| 4A.4      | `translationStore.ts` — `saveNote()` + `fetchNotes()` | Phase 4A | Medium   | Store functions with JWT auth for both endpoints                                                                    |
| 4A.5      | `PostDetailPage.vue` — Notes UI section               | Phase 4A | Medium   | Scrollable note list + textarea + "Add Note" button below workspace card                                            |
| 4A.6      | `PostDetailPage.vue` — Load notes on mount            | Phase 4A | Medium   | Notes fetched and displayed with author email + timestamp                                                           |
| 4A.7–4A.9 | Phase 4A verification                                 | Phase 4A | Medium   | Notes persist, show author/time, appear in chronological order                                                      |

---

## 3. Summary — Weekly Reflection

### Key Tasks Done

- Completed **Phase 0** (Article Titles in Dashboard) — backend + frontend, titles and status now visible on every card
- Completed **Phase 1** (Dashboard Search + Filter Bar) — text search, severity filter, and empty state
- Completed **Phase 2A** (Review Status Workflow) — full end-to-end status management with dropdown on Dashboard, "Mark as Approved" on detail page, status filter, DynamoDB persistence
- Completed **Phase 2B** (Save Review Progress) — accepted error selections persist across page refreshes via DynamoDB
- Translated two Vietnamese AI prompts to English
- Diagnosed and resolved multiple TypeScript/ESLint configuration issues

### Key Things Learned

- **Lambda Proxy Integration is critical** — without it, API Gateway sends the event in a different format and wraps Lambda returns incorrectly, causing silent failures where the frontend thinks the call succeeded but nothing was saved
- **IAM permissions must be explicitly granted** — new Lambdas need `dynamodb:UpdateItem` / `dynamodb:GetItem` attached to their execution role; missing policies cause 502 responses
- **Vue `<select>` @change fires on re-render** — when reactive data changes the `:value` binding, the `@change` event can trigger unintentionally; must guard with a value comparison
- **CORS `Access-Control-Allow-Headers`** must include `Authorization` on any endpoint that receives a JWT token
- **Variable scoping in `<script setup>`** — `errData` declared inside `onMounted` is not accessible at the top level; code referencing it must be inside the same async callback

### Literature Read

- AWS API Gateway Lambda Proxy Integration documentation
- AWS DynamoDB single-table design patterns (PK/SK with METADATA and ERR# prefixes)
- Vue 3 Composition API — `<script setup>` scoping rules and reactive lifecycle
- Pinia store composition patterns for cross-store dependencies

### Issues/Problems

- **Status resetting on Dashboard refresh** — Root cause: `GetArticles` Lambda on AWS still had old code that didn't return `Status` field; combined with unguarded `@change` on `<select>`, the dropdown was auto-triggering `updateArticleStatus("Ready")` on every re-render
- **"Failed to load response data"** — Two causes discovered: (1) Lambda Proxy Integration not enabled on API Gateway POST methods, (2) missing DynamoDB IAM permissions causing Lambda to crash before returning
- **`errData is not defined` ReferenceError** — The 2B.7 pre-population code was placed outside `onMounted` where `errData` didn't exist; moved inside the async callback to fix
- **Cognito auth on GET endpoints** — Adding Cognito authorizer to `/articles` broke the unauthenticated `fetchTranslations` call; resolved by adding auth tokens to all fetch functions
