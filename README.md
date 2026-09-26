# Math Tutor v1.20.0

A Standard Notes editor that gives kids adaptive math practice. This release is
built on v1.18.0 (the version live on GitHub Pages as of August 10, 2026).

## Installing the update

1. In the GitHub repo, replace `index.html` and `ext.json` with the ones from this folder.
2. Add `src/`, `build.py`, `tests/`, `README.md` and `.github/` so future edits have a source to work from.
3. **Delete `Index.html` and `Math Tutor.html` from the repo.** They are old builds that
   GitHub Pages still serves publicly. Also, `Index.html` and `index.html` differ only in
   capitalization, which clashes when the repo is cloned on Mac or Windows.
4. Open the editor in Standard Notes and check that saved progress loads. Please test on
   desktop *and* mobile (see "Not yet tested" below).

Your saved progress carries over automatically. An existing parent PIN is converted to a
hash the first time the new version loads, and tiers earned under the old rules are kept.

## First run for grown-ups

Open **For grown-ups** on the home screen and set a parent PIN (4–8 digits) in
**Parent controls**. Until a PIN exists, rewards can't be claimed and quests can't be
approved, so a child can't set the PIN himself by being the first to type one.

Behind the PIN: quest approvals, reward claims, adding or removing rewards, the settings
below, changing the PIN, and resetting progress. After unlocking, controls stay open for
10 minutes or until you tap **Lock**. Five wrong guesses lock the PIN for 30 seconds,
doubling with each further miss (up to an hour).

| Setting | Default | What it does |
|---|---|---|
| Approve quests with the PIN | On | Self-reported quests wait for a grown-up |
| Timed challenges | On | Off hides Math Sprint and stops speed from affecting game hits |
| Speed counts toward Gold/Diamond | Off | On restores the old speed thresholds (20 s / 12 s average) |
| Ask & Explain | Try first | *Try first*: one guess before the answer. *Open*: answer right away. *Off*: hidden |

**Forgot the PIN?** Use "Forgot the PIN?" in Parent controls and type ERASE. This
removes the PIN *and* erases all points, stars and levels (name, grade and settings stay).
That cost is deliberate, so it isn't a useful trick for a child.

The PIN is a deterrent, not strong security. Anyone who can open the browser's
developer tools can edit the saved data directly.

## What changed in v1.20.0

v1.19 made practice too easy. Its difficulty rule settled near 4 in 5 right and climbed
only one level per 3 right answers, while most subjects have 30–40 levels.

- **Fast climb.** Each subject starts in climbing mode. Two right answers in a row (first
  try, no hint) jump several levels: 5 for adding/subtracting, 4 for ×/÷, 2 for smaller
  subjects. A miss steps back half a jump and halves the jump size. Once the jump size
  drops below 2, the subject uses the normal rule. Pressing Easier ends climbing. After
  "Find the right levels" or a skill check, jumps are limited to 2. Existing progress
  gets climbing too.
- **Harder target.** The normal rule is now 2 right → up, 1 miss → down, which settles near
  7 in 10 right. It was 3 right → up (about 4 in 5).
- **Mixed review at his actual level.** It used to be one level below.
- **Trivial problems removed:**
  - Fraction multiplication had a fraction equal to 1 (like 3/3) in about half of its
    problems, and levels 5–8 were identical. Now fractions are always less than 1,
    denominators grow with level (up to 12), and the wrong choices come from common
    mistakes, such as adding across.
  - Fraction comparison no longer uses fractions equal to 1.
  - Division level 5 no longer drops back to "2 ÷ 2".
  - From level 3 up, adding, subtracting, multiplying and dividing skip ×0, ×1, +0, −0,
    ÷1 and "a ÷ a". Order of operations still has these; I left it alone.

In a simple simulation of a strong student (about 80% right at level 19 of 40, starting
at level 1), v1.19 needed about 51 answers to reach level 18 and he'd get 99% of his first
50 right. v1.20 needs about 8 and he'd get about 74% right. This is a model, not
measurements of your son; real levels don't form a perfectly smooth difficulty curve.

## What changed in v1.19.0

| Area | Change |
|---|---|
| Difficulty | 3 right in a row moves up a level, 1 miss moves down; settled near 79% correct. *Changed in v1.20.* |
| Mixed review | New home-screen button: 10 questions, never the same topic twice in a row, favoring topics not seen lately (mastered ones included). It doesn't change levels. It ran one level below; *now at his level in v1.20.* |
| Mistake Gym | Missed problems return after 1, 3, 7, 21 and 60 days, instead of 1, 3, 7. |
| Points | No points on levels below where he tapped **Easier**; they resume once he's back up. Practice shows recent accuracy ("✅ 8/10 lately"). The Store has a note for parents on phasing out tangible rewards. |
| Timing | Parent switch for timed challenges. Sprints unlock per subject only at 80% accuracy over 10+ practice questions. |
| Ask & Explain | Try-first mode. Worked steps for ×, ÷, +, −, percent-of, and adding or subtracting fractions; other questions keep their one-line explanation. Accepts "176 r 2" style answers. |
| After a miss | The next problem is "one like it": same topic, level, operation and similar wording. |
| Language | Adds numerator/denominator, reciprocal and regrouping next to the kid-friendly shortcuts. This covers first mentions, not every occurrence. |
| Accessibility | Pinch-zoom works again. Diagrams and heatmap cells have text labels for screen readers. |
| Mastery | Gold needs one correct, unhinted answer after 7+ days away; Diamond needs two. Speed counts only if switched on. |
| Security | Parent controls behind the PIN; hashed PIN with lockout; Reset keeps name, grade, PIN and settings. Standard Notes messages from windows other than the parent are ignored. The test hook is removed from release builds. |

## Editing and rebuilding

Edit `src/app.js` (logic and screens), or `src/head.html` / `src/tail.html` (styles and
markup). Then run:

```
python3 build.py          # writes index.html (needs only Python 3)
python3 build.py --check  # confirms the security-policy hash matches the script
```

Never edit `index.html` by hand. The page only runs the one script whose hash appears in
its security policy, so a hand edit makes the whole app stop loading.

`src/app.js` is a formatted version of the original minified bundle, so most names are
short (`m` is the saved state, `g` the current session, `w()` redraws the screen).
Useful tuning knobs (search for them):

- `UP_AFTER` / `DOWN_AFTER`: staircase rule; `2`/`1` targets about 71% correct, `3`/`1` about 79%.
- `climbStart`: first jump size per subject.
- `ts = [1, 3, 7, 21, 60]`: Mistake Gym intervals, in days.
- `RETAIN_GAP_DAYS`: gap that counts as "remembered later".
- `MIX_TOTAL`: mixed-review round length.

### Tests

```
npm install jsdom@24
python3 build.py --test   # writes index.test.html, which keeps the test hook
node tests/tests.mjs
```

There are 90 checks covering the features above; all pass on this build. Don't upload
`index.test.html` to the repo.

The included GitHub Action (`.github/workflows/check-build.yml`) fails if `index.html`
doesn't match a fresh build from `src/`.

## Securing the GitHub account

Whoever controls this repo controls the code running inside your notes app.

- Turn on two-factor authentication, ideally a passkey or security key.
- Add a branch protection rule on `main` that requires the check-build workflow to pass.
- Review changes before uploading. The published file is now readable and matches `src/`
  line for line, which makes review possible.

## Not yet tested

- **Real Standard Notes, desktop or mobile.** The tests run in a simulated browser
  (jsdom). A simulated iframe test confirmed that v1.18 accepted a fake "I'm Standard
  Notes" message from a sibling frame, and v1.19 ignores it. The new check allows messages
  with no source window, which is how native mobile bridges usually deliver them, but I
  couldn't verify the actual Standard Notes mobile app.
- **Where Standard Notes stores the data.** Per the code, full progress goes to the
  editor's component data and a text summary goes into the note. Confirm on your setup if
  it matters to you (for example, siblings sharing one account would share one profile).
- **File size.** The release is unminified so it matches the source, which makes it about
  22% larger compressed than v1.18: roughly 168 KB vs 138 KB gzipped.
