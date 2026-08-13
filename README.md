# 🔋 Electrical Fundamentals Learning Lab

An interactive, beginner-friendly Streamlit web application for undergraduate
Physics and Electronics students taking their first look at the fundamentals
of electricity — voltage, current, resistance, power, energy, AC/DC, and the
key laws (Ohm's Law, Kirchhoff's Laws, series/parallel resistance).

## 📖 Project Overview

This is a single-file Streamlit application built as a self-contained virtual
learning laboratory — a companion to the Logic Gates and Electronic
Components modules. It covers 10 foundational electrical concepts and 6 core
laws, each with a plain-English explanation, a schematic diagram, key facts,
and — where it makes sense — a live interactive calculator driven by real
Python physics formulas (not hard-coded results).

No external APIs, AI models, databases, or internet services are used. The
whole app runs locally with just `streamlit`, `pandas`, and `matplotlib`.

## ✨ Features

- **🏠 Introduction** — what electricity is, the water-pipe analogy for
  voltage/current/resistance, and why fundamentals matter before studying
  components.
- **🔎 Core Concepts Explorer** — expandable cards for 10 concepts (Voltage,
  Current, Resistance, Power, Energy, Charge, Frequency/AC, Conductors &
  Insulators, AC vs DC, Series & Parallel Circuits), each with a real SVG
  schematic/diagram, unit, formula, plain-English explanation, applications,
  and safety notes.
- **📐 Laws & Relationships** — a filterable Pandas reference table of all
  concepts plus expandable cards for the 6 key laws (Ohm's Law, Power Law,
  KCL, KVL, Series Resistance, Parallel Resistance).
- **🎛️ Interactive Simulator** — a central hub to pick any concept or
  Kirchhoff's Laws and play with its live model.
- **🔬 Practical Applications** — expandable cards showing these fundamentals
  at work in home wiring, batteries, lighting, power grids, electronics, and
  electric vehicles.
- **🧪 Troubleshooting Lab** — 5 realistic beginner troubleshooting scenarios
  with multiple-choice questions and immediate, explained feedback.
- **📝 Quiz** — 10 multiple-choice questions (3 options each), scored out of
  100%, with a review of correct/incorrect answers, a progress bar, balloons
  for high scores, and a retake option.
- **Dashboard header** — quick stats shown via `st.metric()` on every page.

## 🎯 Learning Objectives

By the end of this module, a student should be able to:

1. Explain voltage, current, resistance, power, and energy in plain language.
2. Apply Ohm's Law and the Power Law to solve simple circuit problems.
3. Calculate total resistance for resistors in series and in parallel.
4. Apply Kirchhoff's Current Law and Voltage Law to simple circuits.
5. Distinguish AC from DC and convert between peak and RMS voltage.
6. Recognise how these fundamentals appear in real electrical systems.
7. Reason through simple circuit troubleshooting scenarios.

## 🧩 Concepts & Laws Covered

**Concepts:** Voltage, Current, Resistance, Power, Energy, Charge, Frequency
(AC), Conductors & Insulators, AC vs DC, Series & Parallel Circuits.

**Laws:** Ohm's Law, Power Law, Kirchhoff's Current Law, Kirchhoff's Voltage
Law, Series Resistance, Parallel Resistance.

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints in your terminal (usually
`http://localhost:8501`).

## 🗂️ Project Structure

```
.
├── app.py             # The complete Streamlit application (single file)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

Inside `app.py`, code is organised into clearly separated sections:

- Page config and custom CSS
- Pure calculation functions (`ohms_law_solve`, `power_solve`, `energy_kwh`,
  `series_resistance`, `parallel_resistance`, `ac_peak_from_rms`,
  `kcl_check`, `kvl_check`, …)
- The `CONCEPTS` and `LAWS` data dictionaries
- SVG schematic/diagram generator (`draw_concept_svg`) — every symbol is
  flattened to a single line of HTML before being injected, so Streamlit's
  Markdown renderer never mis-parses an embedded blank line as the end of
  the HTML block
- Interactive `render_*` functions (one per calculator/simulator), each
  reusable across the Explorer and Simulator pages via a `key_prefix` so
  widget keys never collide
- Quiz and troubleshooting data
- Session-state initialisation
- Sidebar navigation and the top dashboard
- One block per page (Introduction, Concepts Explorer, Laws, Simulator,
  Applications, Troubleshooting, Quiz)

## 🎓 Educational Use

This app is intended for classroom use, self-study, or as a lab companion
in an introductory electronics or physics course, ideally **before** the
Electronic Components module — these fundamentals underpin everything a
student will see there.

## ⚠️ Safety Considerations

- The application **never** encourages experimenting with mains/household
  electricity.
- Voltage, AC/DC, and conductor/insulator topics carry explicit safety
  warnings given their real-world hazard potential.
- All calculators are framed as educational tools using standard formulas;
  students are reminded that real circuits also involve tolerances,
  non-ideal components, and safety margins not modelled here.

## 🚀 Future Improvements

- Add a companion module on capacitive/inductive AC circuit behaviour
  (reactance, impedance, phase).
- Add a simple drag-and-drop circuit builder with live Ohm's Law/KCL/KVL
  verification.
- Add printable/exportable student progress reports.
- Cross-link directly into the Electronic Components module's calculators.
