# Sanchin Masterclass — working plan (read this after any context reset)

Book: *Goju-Ryu Karate Sanchin Masterclass* — subtitle: *Illustrated Textbook With Frame-by-Frame Diagrams, Testing Drills, Posture Corrections, and Strength Progressions for the Foundational Form*. Author: **Dr Beverly J. Stivers**.

User requirements: black & white only (incl. illustrations), 6 x 9 in KDP trim, one column, premium bestseller formatting, UK English, humanised (no AI filler words: delve, tapestry, testament, journey-cliché, "in today's fast-paced world", etc.), problem-solving book, each chapter > 2,500 words (aim 3,000–3,400), parts of 3 chapters, 300+ pages, illustrations included, export PDF + EPUB + DOCX.

Pipeline: `sanchin/` (adapted from `book/`). `python3 build.py all` -> output/*.pdf, *.epub, *.docx. Figures drawn by `figs/*.py` into `figures/` (pure B&W line art, matplotlib). Use `figs/common.py` mannequin helpers.

Markdown conventions (pandoc): first line `# Title`; `::: chapter-intro`; `## Section` (auto-numbered n.m); `### sub`; boxes: `::: drill` (**Drill 4.1 – Name**), `::: fault` (**Problem / Fix**), `::: note` (**Teacher's Note**), `::: test` (**Test Yourself**), `::: keypoints` (### Chapter Summary), `::: practice` (### Practice Questions / Training Tasks). Figures: `![**Figure 4.1** caption](figures/fig4_1.png)`.
Use spaced en dashes ( – ) not em dashes. Japanese terms in italics first use.

## Structure (9 parts x 3 chapters = 27)
Front: copyright, dedication, contents, preface, safety (Before You Begin), howto.
P1 Origins and Understanding: 1 The Form at the Root of the Style; 2 From Fuzhou to Naha; 3 The Three Battles.
P2 Building the Stance: 4 Sanchin Dachi from the Ground Up; 5 Knees, Hips and the Pelvic Lock; 6 Spine, Shoulders and Head.
P3 Breath and Tension: 7 Breathing in Sanchin; 8 Dynamic Tension Without Damage; 9 Rhythm, Timing and Slowness.
P4 The Form Frame by Frame: 10 Opening (frames 1–8); 11 The Advance (frames 9–24); 12 Turns, Retreat and Closing (frames 25–48).
P5 Hands and Arms: 13 The Sanchin Block; 14 The Punch and Hikite; 15 Open Hands: Nukite and Mawashi Uke.
P6 Testing (Shime): 16 Why Teachers Test; 17 The Testing Map; 18 Partner Drills and Self-Testing.
P7 Posture Corrections: 19 Feet and Legs; 20 Hips, Trunk and Shoulders; 21 Breath, Eyes and Mind.
P8 Strength Progressions: 22 Conditioning Principles and Assessment; 23 Hojo Undo for Sanchin; 24 The Twelve-Week Programme.
P9 Mastery for Life: 25 Sanchin and Tensho; 26 Sanchin in Application; 27 Training for Life.
Back: Appendix A Sanchin at a Glance (frame checklist); Appendix B Testing scorecards & logs; Appendix C 12-week planner; Glossary; Further Reading; About the Author.

## Form version used (state variation caveat in ch10)
Miyagi-lineage closed-fist version: musubi dachi/rei -> yoi (open hands crossed) -> step R into R sanchin, cross arms, morote chudan uke -> [L hikite, L tsuki, L uke] in R stance -> step L: R tsuki/uke -> step R: L tsuki/uke -> turn 180 (mawatte) -> tsuki/uke -> step, tsuki/uke -> turn 180 back to front -> tsuki/uke -> step back x2 with morote nukite (hands to hips, double spear-hand) -> mawashi uke (tora guchi) R then L -> close: step back to musubi, rei.
Frames numbered 1–48 across chs 10–12.

## Status
- [x] scaffold/build  - [x] fig library  - chapters written: front matter, ch01-ch06 (figs done). Next: ch07+
