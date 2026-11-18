BOOK = {
    "title": "Electric Vehicle Engineering: A Modern Textbook on EV Powertrains, Batteries, Motors, Charging, and Power Electronics",
    "subtitle": "A Modern Textbook on EV Powertrains, Batteries, Motors, Charging, and Power Electronics",
    "author": "Marcus J. Thornton, Ph.D.",
    "blurb": "A problem-solving textbook on how battery electric vehicles are engineered: vehicle energy demand, lithium-ion cells and packs, battery management, traction motors and their control, power semiconductors, inverters, converters, chargers, charging standards, integration, functional safety and fault diagnosis. Written for students, graduate engineers and technical professionals, with worked examples, field case files and end-of-chapter problems.",
    "front": [
        {"file": "preface.md"},
        {"file": "howto.md"},
    ],
    "parts": [
        {
            "title": "Foundations of the Electric Vehicle",
            "intro": "Before we take a battery apart or wind a stator, we need to agree on what an electric vehicle is asked to do. These three chapters set out the vehicle as a system, work out how much energy it needs to move, and lay down the electrical ideas that every later chapter leans on.\n\nIf you already work in the field, skim them anyway. Most of the expensive mistakes I have seen in EV programmes began with a number from this part of the book that somebody got slightly wrong.",
            "chapters": ["ch01.md", "ch02.md", "ch03.md"],
        },
        {
            "title": "Batteries and Energy Storage",
            "intro": "The battery is the most expensive, heaviest and most closely watched component in the vehicle. It decides range, cost, charging time and, very often, the warranty bill.\n\nThis part moves from the chemistry inside a single cell, through the mechanical and thermal design of a complete pack, to the software that keeps the whole thing safe and tells the driver the truth about how far they can go.",
            "chapters": ["ch04.md", "ch05.md", "ch06.md"],
        },
        {
            "title": "Electric Machines and Their Control",
            "intro": "An electric motor is a beautifully simple machine on paper and a stubborn one in practice. Here we look at how traction motors make torque, why the industry settled on the designs it did, how engineers trade efficiency against cost and heat, and how a few hundred lines of control code turn three alternating currents into smooth, silent acceleration.",
            "chapters": ["ch07.md", "ch08.md", "ch09.md"],
        },
        {
            "title": "Power Electronics",
            "intro": "Between the battery and the motor sits a box of switches that turns thousands of times a second. Power electronics is where much of the recent progress in EVs has come from: wide-bandgap semiconductors, 800-volt platforms and integrated chargers.\n\nThese chapters start with the switching devices themselves and build up to the inverter, the DC-DC converter and the on-board charger.",
            "chapters": ["ch10.md", "ch11.md", "ch12.md"],
        },
        {
            "title": "Charging, Integration and the Road Ahead",
            "intro": "A vehicle is only as useful as the network that refuels it and only as good as the way its systems work together. The final part covers charging hardware and protocols, the integration of thermal, electrical and safety systems, and the practical craft of testing a vehicle and finding out why it has gone wrong.\n\nWe finish by looking honestly at what is coming next and how to judge it.",
            "chapters": ["ch13.md", "ch14.md", "ch15.md"],
        },
    ],
    "back": [
        {"file": "appendix-a.md", "cls": "answers"},
        {"file": "appendix-b.md"},
        {"file": "glossary.md", "cls": "glossary"},
        {"file": "reading.md"},
        {"file": "about.md"},
    ],
}
