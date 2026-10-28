HUB FIX — two replacement files

This package contains a corrected copy of the current public generator and a manual-only deploy workflow.
The generator removes fabricated generic buying checklists, cleans source descriptions, adds homepage search, and keeps related-video links within the same channel.
The workflow removes automatic schedules so a rebuild happens only when manually started.

To apply:
1. Extract this ZIP.
2. In the GitHub repository, replace the root autopilot_generator.py with the one in this ZIP.
3. Replace .github/workflows/deploy.yml with the one in this ZIP.
4. In GitHub Actions, enable the workflow if needed, then run “Manual Hub Rebuild” once.

Do not connect Make to the generated RSS feeds yet; those feeds still need a new-only/deduplicated redesign.
No XML post batches or video-library files are included or changed.
