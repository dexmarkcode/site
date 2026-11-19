## Preface {.unnumbered}

::: dropcap
Every year I watch the same thing happen. A capable student sits through a well-taught lecture on the Laplace transform, follows every line on the board, nods at the worked example, and goes home convinced that the topic is understood. Then they open the problem sheet, and nothing works. The partial fractions will not come out. The sign on the phase is wrong. The region of convergence, which seemed so obvious in the lecture, has become a mystery. By the following week they have concluded that they are 'not a maths person', which is almost never true.
:::

What has actually happened is simpler and far more fixable. Understanding a method when someone else performs it is a different skill from performing it yourself, and the second skill is built only by practice: lots of it, with immediate and honest feedback. That is what this book provides.

It contains six hundred problems on signals and systems, arranged into twelve chapters and four parts, from the basic language of signals through the Fourier, Laplace and Z-transforms to the design of digital filters. Every problem has a complete, step-by-step solution. Not a bare answer, and not a solution that skips the awkward line in the middle, but the working I would want a student to write in an examination, together with the reasoning behind each step and, wherever possible, a check that confirms the result by an independent route.

Each chapter opens with a focused account of the theory you need, written in the way I would explain it across a desk rather than from a lectern. These sections are not a substitute for a full textbook; they are the essential ideas, the standard results, the methods that work, and the pitfalls I have seen catch students again and again. They are followed by fifty graded problems and then by the full solutions.

#### Who this book is for {.unnumbered}

The book is written for undergraduate students of electrical, electronic, communications, control and biomedical engineering, and for anyone studying signals and systems as part of physics, computer science or applied mathematics. It suits a first course in signals and systems, and it will also serve students taking follow-on courses in control, communications and digital signal processing who need to make the core transform methods automatic.

It is equally intended for practising engineers. If you studied this material some years ago and now need it again, because you are designing a filter, tuning a control loop or preparing for a professional examination, working through a chapter of problems is the fastest way I know to bring the methods back to your fingertips.

#### What makes this workbook different {.unnumbered}

*The problems are graded.* Each chapter's fifty problems are divided into warm-up, core and challenge bands. The warm-up problems test definitions; the core problems are the kind you will meet in examinations; the challenge problems combine ideas and reward care.

*The solutions teach.* Every solution is broken into labelled steps, and each step says not only what to do but why. Where a method has a common trap, the solution points it out. Where an answer can be checked, by an initial value, a sum rule, a symmetry or a direct recursion, the check is shown.

*The answers are right.* Every problem in this book was generated and solved with exact symbolic arithmetic, and the results were verified independently: inverse transforms were transformed back, sequences were checked against long division and recursion, and stability results were confirmed against computed roots. There will inevitably be typographical blemishes in a book of this size, and I would be grateful to hear of any, but the mathematics has been checked with unusual thoroughness.

*The illustrations explain.* The figures are not decoration. Each was drawn to show something that is easier to see than to say: the flip and slide of convolution, the Gibbs overshoot, the spectral copies created by sampling, the link between pole positions and time responses.

I hope you find the book useful, and I hope that by the end of it you will have the quiet confidence that comes from having solved a great many problems correctly on your own.

*Marcus J. Thornton*

## How to Use This Book {.unnumbered}

The chapters are designed to be worked through in order, because the later material leans heavily on the earlier. Part I (signals, systems and convolution) is the foundation for everything else. That said, each part is reasonably self-contained, and a reader who is already comfortable with convolution can begin with Part II, III or IV as their course requires.

#### A suggested routine {.unnumbered}

For each chapter, I recommend the following.

1. **Read the opening sections** with a pencil in hand. Work through the examples yourself before reading their solutions.
2. **Attempt the warm-up problems** without looking at the solutions. They should be quick. If they are not, reread the relevant part of the chapter.
3. **Work the core problems** in batches of five or six. Write full solutions, as you would in an examination.
4. **Check each solution carefully.** Do not merely compare final answers. Compare your method step by step with the one given, and note any difference.
5. **Return to the problems you got wrong** two or three days later and try them again from scratch. This is where most of the learning happens.
6. **Attempt the challenge problems** once the core problems feel routine.

#### Reading a solution actively {.unnumbered}

When you read a solution, cover everything below the current step. Before revealing the next step, ask yourself what you would do. If your plan matches the book's, move on. If it does not, stop and work out why. Either you have found a better route, which happens, or you have found a gap in your understanding, which is far more valuable.

#### A note on notation and numbering {.unnumbered}

Problems are numbered by chapter: Problem 7.23 is the twenty-third problem of Chapter 7, and its solution is Solution 7.23. Decimal values in solutions are rounded, usually to three or four significant figures; exact values are given wherever they are reasonably compact.

## A General Method for Solving Problems {.unnumbered}

Most failures in signals and systems problems are not failures of knowledge. They are failures of process: starting to calculate before deciding what to calculate, skipping the sketch, or failing to check. The following routine applies to almost every problem in this book. It will feel slow at first. With practice it becomes automatic, and it is how experienced engineers work.

::: strategy
**Five questions before, during and after every problem.**

1. **What kind of object is this?** Continuous or discrete? Periodic or not? Energy or power signal? Causal? Is the system LTI? The answer decides which tools are legitimate.
2. **What does it look like?** Sketch the signal, the pole–zero plot or the spectrum, however roughly. A picture fixes signs, limits and regions before any algebra begins.
3. **Which tool fits?** Is the problem easiest in time or in a transform domain? Is there a table entry plus a property that does the job, or a symmetry that halves the work?
4. **Carry out the method one step at a time.** Write each step. Most errors occur when two operations, such as a shift and a scaling, are combined in the head.
5. **Check the answer by an independent route.** Initial and final values, DC gain, area or sum rules, symmetry, units, or a direct recursion. Never submit an unchecked answer if a check is available.
:::

There are also some habits worth cultivating.

**Estimate first.** Before calculating the period of a sum of sinusoids, guess it. Before inverting a transform, say whether the answer will decay, oscillate or grow. The estimate costs seconds and catches gross errors.

**Keep exact values as long as possible.** Write $\sqrt{2}/2$ rather than 0.707 until the very end. Rounding early accumulates error and hides structure, such as the cancellation of a pole by a zero.

**Know a few results cold.** The transform of $e^{-at}u(t)$, the geometric series, Euler's formula, the cover-up rule, the sinc function and its zeros. Everything else can be derived from a handful of results like these, but they must be instant.

**Respect the region of convergence.** Many of the subtlest errors in transform problems come from ignoring it. If a problem involves anything other than causal signals, write the ROC down at every stage.

**When stuck, go back to the definition.** Every property and table entry is a consequence of a definition. If you cannot see which property to apply, write out the defining integral or sum and manipulate it directly. You will usually see the shortcut halfway through.

## Notation {.unnumbered}

| Symbol | Meaning |
|:--|:--|
| $x(t)$, $x[n]$ | continuous-time and discrete-time signals |
| $u(t)$, $u[n]$ | unit step |
| $\delta(t)$, $\delta[n]$ | unit impulse |
| $r(t) = t\,u(t)$ | unit ramp |
| $h(t)$, $h[n]$ | impulse response of an LTI system |
| $*$ | convolution |
| $\circledast$ | circular convolution |
| $T_0$, $\omega_0$, $N_0$ | fundamental period and frequency |
| $a_k$ | Fourier series coefficients |
| $X(j\omega)$ | continuous-time Fourier transform |
| $X(e^{j\omega})$ | discrete-time Fourier transform |
| $X[k]$ | discrete Fourier transform |
| $X(s)$, $H(s)$ | Laplace transform, transfer function |
| $X(z)$, $H(z)$ | Z-transform, system function |
| $\operatorname{sinc}(x)$ | $\sin(\pi x)/(\pi x)$ |
| $\operatorname{sgn}(t)$ | sign function |
| $j$ | $\sqrt{-1}$ |
| $\omega_n$, $\zeta$ | natural frequency and damping ratio |
| ROC | region of convergence |
| LTI | linear time-invariant |
| BIBO | bounded-input, bounded-output |
