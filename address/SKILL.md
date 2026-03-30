---
name: address
description: Address unresolved review comments on a pull request. Use when the user types /address, asks to "address PR comments", "handle review feedback", or wants to resolve PR threads.
---

Address unresolved review comments on a pull request.

usage: `/address [PR_NUMBER]`

## phase 1 — gather

1. `gh auth status` — stop if not authenticated
2. resolve PR: if `$ARGUMENTS` is a number, `gh pr view {number} --json number,url,isDraft`; otherwise `gh pr view --json number,url,isDraft`. store `{pr_url}`. warn if draft
3. resolve owner/repo: `gh repo view --json owner,name -q '.owner.login + "/" + .name'`
4. `git pull --rebase` — stop if conflicts
5. fetch unresolved threads via GraphQL:
   ```bash
   gh api graphql --paginate -f query='
     query($owner: String!, $repo: String!, $pr: Int!, $endCursor: String) {
       repository(owner: $owner, name: $repo) {
         pullRequest(number: $pr) {
           reviewThreads(first: 100, after: $endCursor) {
             pageInfo { hasNextPage endCursor }
             nodes {
               id
               isResolved
               comments(first: 50) {
                 nodes { databaseId body path line originalLine diffHunk author { login } createdAt }
               }
             }
           }
         }
       }
     }
   ' -f owner="{owner}" -f repo="{repo}" -F pr={pr_number}
   ```
   - `thread.id` → resolveReviewThread mutation. `comment.databaseId` → REST reply endpoint
   - collect **all comments** per thread (reviewer may refine/retract in follow-ups)
   - use `databaseId` from the last comment for replies
6. if no unresolved threads, stop

## phase 2 — verify

for each thread, **exhaustive** research:

1. **locate:** `path` + `line`, fall back to `originalLine` + `diffHunk` search, then `git log --follow` for renames. if unfound → "needs human judgment"
2. **read:** 50-100 lines of surrounding context around the referenced line
3. **trace:** LSP goToDefinition, findReferences, callers/callees, types, related tests
4. **understand:** read full thread. check for `suggestion` blocks (evaluate as proposed diff). rhetorical questions → classify as legitimate
5. **classify:**
   - **legitimate** — real issue requiring a code change
   - **question** — clarification request or style nit. if nit is trivial and agreed, fix it but leave thread open
   - **noise** — misunderstands code, outdated, or incorrect. heuristics: contradicted by types, check exists upstream, applies to old code, generic bot suggestion
6. **overlap check:** if multiple legitimate threads target overlapping lines, keep the most critical, reclassify rest as "needs human judgment"

present grouped results (legitimate / questions / noise) with comment text, file:line, and rationale citing specific code.

## phase 3 — rubric

invoke `/rubric` against the verification summary. must evaluate: research thoroughness, classification accuracy, rationale quality. re-research weak assessments once, then reclassify as "needs human judgment."

## phase 4 — address

**A. commits:** for each legitimate thread: fix → run tests/lints → commit (`fix: <what> (PR #N review)`)

**B. push:** ask permission. if declined or push fails → skip C, note in report.

**C. replies (only after successful push):**
- **legitimate:** reply with commit hash, resolve thread
  ```bash
  gh api repos/{owner}/{repo}/pulls/{pr}/comments/{databaseId}/replies -f body="<reply>"
  gh api graphql -f query='mutation($id: ID!) { resolveReviewThread(input: {threadId: $id}) { thread { isResolved } } }' -f id="<thread_node_id>"
  ```
- **question:** reply answering with code references. do NOT resolve
- **noise:** reply explaining why concern doesn't apply. do NOT resolve

**tone:** casual, lowercase, no emdashes, conversational. hookify pr-comment-style hook is active.

good replies:
- `"fixed in abc1234 — was mutating the array in place, now uses a copy"`
- `"this is fine — fetchUser already validates the id upstream (see user-service.ts:87)"`
- `"the retry caps at 3 with exponential backoff (client.ts:120-135)"`

bad (blocked by hooks): `"I've addressed this concern by implementing a more robust solution"`

## phase 5 — report

```
## PR #N — <pr_url>
**push status:** pushed / not pushed (local-only)
**summary:** N addressed, N answered, N noise, N needs judgment

## addressed (N)
- file.ts:42 — abc1234 — one-line summary of fix
## answered (N)
- file.ts:55 — one-line summary (thread open)
## noise (N)
- file.ts:99 — one-line reason (thread open)
## needs judgment (N)
- file.ts:77 — why it couldn't be addressed
```

## rules

- every comment must be exhaustively researched before acting (LSP, not just text search)
- one commit per fix, tests after each
- only auto-resolve threads with committed fixes
- never resolve without a reply first
- push before replies so hash links resolve; ask before pushing
- if push fails or declined, skip replies, report as local-only
- overlapping legitimate threads → keep most critical, rest → "needs human judgment"
- design decisions or architectural changes → "needs human judgment"
- if any `gh` command fails unexpectedly, report the error and stop
