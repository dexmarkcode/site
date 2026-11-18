# Preface

This book grew out of a frustration that I suspect many teachers of electric vehicle engineering share. The subject sits across four or five traditional disciplines: electrochemistry, electrical machines, power electronics, control, thermal engineering and vehicle dynamics. There are excellent specialist texts on each of them. But a student or a working engineer who wants to understand how those pieces fit together in a real vehicle has, for a long time, had to assemble the picture from a shelf of books, a pile of conference papers and whatever they could pick up from colleagues.

I wanted to write the book I would have liked to have when I started: one that follows the energy from the charging socket to the tyre, explains each component well enough that you could hold a sensible conversation with its specialist designer, and above all teaches you how to *think* about an electric vehicle when something does not behave as expected.

That last point shapes the whole book. Electric vehicles are not difficult because any single part of them is mysterious. They are difficult because everything is connected. A cell chemistry chosen for cost changes the voltage window, which changes the inverter's current rating, which changes the cooling demand, which changes the winter range. An engineer who understands only one link in that chain will make locally sensible decisions that hurt the vehicle as a whole. So, wherever I can, I have tried to show the connections, and I have filled the chapters with worked examples and case files that cross the boundaries between disciplines.

### Who this book is for

The book is written for three groups of readers. The first is undergraduate and postgraduate students in electrical, mechanical and automotive engineering who are taking a course on electric or hybrid vehicles. The second is practising engineers who have spent their careers on combustion powertrains, chassis or electronics and now find themselves working on electrified products. The third is the growing community of technicians, technical managers, analysts and investors who need more than a magazine-level understanding of the technology.

I assume you are comfortable with basic algebra and a little calculus, that you remember Ohm's law and Newton's second law, and that you have met the idea of a sine wave. I do not assume any prior knowledge of batteries, motors or power electronics. Where a topic needs more mathematics, such as the reference frame transformations used in motor control, I build it up step by step and always tie it back to what is physically happening.

### What this book is not

It is not a service manual. Nothing here tells you how to work on a particular model of car, and nothing replaces proper high-voltage safety training. Please do not open a battery pack or an inverter because you have read a chapter about it. The voltages and stored energies in these systems can kill.

It is also not a survey of every product on the market. Models change every year; physics does not. I have used representative numbers drawn from the general state of the industry around the time of writing, and I have deliberately avoided tying the examples to the specification of any particular vehicle. When I quote figures such as cell energy density or semiconductor losses, treat them as typical values for understanding, not as design data.

### A note on language and units

The book is written in British English and uses SI units throughout, with kilometres for distance, kilowatt-hours for energy and degrees Celsius for temperature. Where the industry habitually uses other units, such as miles per kilowatt-hour in some markets, I give a conversion. Appendix B collects the constants, conversions and material properties you will need for the problems.

### Acknowledgements

No book like this is written alone. I owe a great deal to the students who sat through early versions of this material and told me, sometimes very directly, which explanations did not work. I am grateful to the colleagues in industry and academia who answered questions, argued with my drafts and pointed out where I had oversimplified. Any errors that remain are mine. Finally, I thank my family, who put up with a great many evenings and weekends lost to batteries and inverters, and who never once asked whether it was finished yet. Well, not often.

*Marcus J. Thornton*
