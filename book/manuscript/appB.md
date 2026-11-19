Most of the mathematics in circuit analysis is algebra, and most of the algebra comes down to two skills: rearranging a single equation, and solving several simultaneous equations. This appendix reviews both.

## B.1 Rearranging Equations

To make a particular quantity the subject of an equation, do the same thing to both sides until that quantity stands alone. Work in reverse order to the way the quantity was "built up".

**Example.** Make R~L~ the subject of I = V / (R~S~ + R~L~).

- Multiply both sides by (R~S~ + R~L~): I(R~S~ + R~L~) = V.
- Divide both sides by I: R~S~ + R~L~ = V / I.
- Subtract R~S~: R~L~ = V / I − R~S~.

**Example.** Make R~2~ the subject of the parallel formula 1/R~T~ = 1/R~1~ + 1/R~2~.

- Subtract 1/R~1~: 1/R~2~ = 1/R~T~ − 1/R~1~ = (R~1~ − R~T~) / (R~1~R~T~).
- Take reciprocals: R~2~ = R~1~R~T~ / (R~1~ − R~T~).

Always check a rearrangement by substituting simple numbers back into the original.

## B.2 Powers of Ten

When multiplying, add the powers: 10^3^ × 10^−6^ = 10^−3^. When dividing, subtract them: 10^3^ / 10^−6^ = 10^9^. So, for example, 2 mA × 4.7 kΩ = (2 × 10^−3^)(4.7 × 10^3^) = 9.4 × 10^0^ = 9.4 V.

## B.3 Simultaneous Equations by Substitution and Elimination

Nodal and mesh analysis produce sets of linear simultaneous equations. With two or three unknowns, they are easily solved by hand.

**Substitution.** Rearrange one equation to express one unknown in terms of the others, and substitute into the remaining equations.

**Elimination.** Multiply equations by suitable constants so that one unknown has the same coefficient in two equations, then add or subtract to remove it.

**Example.** Solve 3x + 2y = 16 and x − 4y = −4.

*By substitution:* from the second, x = 4y − 4. Then 3(4y − 4) + 2y = 16, so 14y = 28 and y = 2; then x = 4.

*By elimination:* multiply the first by 2: 6x + 4y = 32. Add the second: 7x = 28, so x = 4; then y = 2.

## B.4 Cramer's Rule for Two Unknowns

For the pair

::: eq
a~1~x + b~1~y = c~1~
a~2~x + b~2~y = c~2~
:::

define the **determinant** of the coefficients:

::: eq
Δ = {{mat|a~1~,b~1~;a~2~,b~2~}} = a~1~b~2~ − b~1~a~2~
:::

Then

::: eq
x = {{frac|Δ~x~|Δ}} = {{frac|c~1~b~2~ − b~1~c~2~|Δ}}     y = {{frac|Δ~y~|Δ}} = {{frac|a~1~c~2~ − c~1~a~2~|Δ}}
:::

Δ~x~ is the determinant formed by replacing the x column with the right-hand sides, and Δ~y~ by replacing the y column.

**Example.** For 3x + 2y = 16 and x − 4y = −4: Δ = (3)(−4) − (2)(1) = −14. Δ~x~ = (16)(−4) − (2)(−4) = −56, so x = 4. Δ~y~ = (3)(−4) − (16)(1) = −28, so y = 2.

## B.5 Cramer's Rule for Three Unknowns

For three equations in x, y and z, the determinant of the 3 × 3 coefficient matrix is found by expanding along the first row:

::: eq
Δ = {{mat|a~11~,a~12~,a~13~;a~21~,a~22~,a~23~;a~31~,a~32~,a~33~}}
= a~11~(a~22~a~33~ − a~23~a~32~)
− a~12~(a~21~a~33~ − a~23~a~31~)
+ a~13~(a~21~a~32~ − a~22~a~31~)
:::

Note the alternating signs: +, −, +. Then x = Δ~x~ / Δ, y = Δ~y~ / Δ and z = Δ~z~ / Δ, where each Δ with a subscript is formed by replacing the corresponding column with the right-hand sides.

**Example.** The nodal equations of Worked Example 10.3 were

::: eq
4V~1~ − V~2~ = 40
−5V~1~ + 9V~2~ − 2V~3~ = 0
−V~2~ + 3V~3~ = 10
:::

*Main determinant.* Expanding along the first row:

Δ = 4[(9)(3) − (−2)(−1)] − (−1)[(−5)(3) − (−2)(0)] + 0 = 4(25) + (−15) = 85

*For V~1~*, replace the first column with (40, 0, 10):

Δ~1~ = 40[(9)(3) − (−2)(−1)] − (−1)[(0)(3) − (−2)(10)] + 0 = 40(25) + 20 = 1020, so V~1~ = 1020 / 85 = 12 V.

*For V~2~*, replace the second column: Δ~2~ = 680, so V~2~ = 680 / 85 = 8 V.

*For V~3~*, replace the third column: Δ~3~ = 510, so V~3~ = 510 / 85 = 6 V.

These agree with the elimination solution in Chapter 10.

::: tip
**Practical Advice**

For three unknowns, Cramer's rule is systematic but laborious; elimination is often quicker when several coefficients are zero. For four or more unknowns, use a calculator's equation solver, a spreadsheet or a few lines of code. The skill that matters most is setting up the equations correctly; the arithmetic can be delegated.
:::

## B.6 Significant Figures

Component values are rarely known to better than 1 %, so answers quoted to more than three or four significant figures suggest a precision that does not exist. Keep at least four significant figures during a calculation to avoid rounding errors, then round the final answer sensibly – usually to three significant figures.
