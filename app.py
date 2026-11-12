"""
Electrical Fundamentals Learning Lab

Built for first-year undergraduate Physics / Electronics students.
Single-file Streamlit application. No external APIs, databases, or internet
services are used — only streamlit, pandas, and matplotlib.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Навчальна лабораторія з основ електротехніки",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# NOTE: every HTML string below avoids blank lines inside a block — Streamlit's
# Markdown renderer treats a blank line inside an HTML block as the end of
# that block, and anything after gets shown as literal text instead of being
# rendered. The only exception is the <style> tag itself, which CommonMark
# treats as a raw block that isn't terminated by blank lines.
# ============================================================================
st.markdown(
    """
    <style>
    .main {background-color: #0e1117;}

    .concept-card {
        background: linear-gradient(135deg, #7c2d12, #9a3412);
        border: 1px solid #fb923c;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    }
    .concept-card, .concept-card h4, .concept-card p, .concept-card b, .concept-card li {
        color: #ffffff !important;
    }

    .app-card {
        background: linear-gradient(135deg, #164e2e, #14532d);
        border-left: 5px solid #4ade80;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    }
    .app-card, .app-card b, .app-card li { color: #ffffff !important; }

    .comp-banner {
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        color: #ffffff !important;
        box-shadow: 0 3px 12px rgba(0,0,0,0.35);
    }

    .symbol-box {
        background: #f9fafb;
        color: #111827;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #374151;
    }

    .status-good {
        background: #14532d;
        border-left: 5px solid #22c55e;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-weight: 600;
    }
    .status-bad {
        background: #7f1d1d;
        border-left: 5px solid #ef4444;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-weight: 600;
    }

    .bulb-wrap { text-align: center; padding: 0.6rem 0 0.3rem 0; }
    .bulb-on {
        width: 90px; height: 90px; border-radius: 50%; margin: 0 auto;
        background: radial-gradient(circle at 35% 30%, #fff9c4, #ffd60a 45%, #f59e0b 75%, #b45309 100%);
        box-shadow: 0 0 22px 9px rgba(255,214,10,0.85), 0 0 55px 26px rgba(255,176,10,0.45), inset 0 0 12px rgba(255,255,255,0.6);
    }
    .bulb-off {
        width: 90px; height: 90px; border-radius: 50%; margin: 0 auto;
        background: radial-gradient(circle at 35% 30%, #6b7280, #374151 60%, #111827 100%);
        box-shadow: inset 0 0 10px rgba(0,0,0,0.7);
        opacity: 0.85;
    }

    .safety-note {
        background: #451a03;
        border-left: 5px solid #f59e0b;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-top: 0.5rem;
        font-size: 0.92rem;
    }

    h1, h2, h3 { color: #f9fafb; }
    </style>
    """,
    unsafe_allow_html=True,
)


def flat(html):
    """Collapse multi-line/indented HTML into one line with no blank lines,
    so Streamlit's Markdown renderer never mistakes it for a code block."""
    return "".join(line.strip() for line in html.strip().splitlines())


# ============================================================================
# CORE ELECTRICAL CALCULATIONS (pure functions, no widgets — reused everywhere)
# ============================================================================

def ohms_law_solve(v=None, i=None, r=None):
    """Given exactly two of (voltage, current, resistance), solve the third."""
    if v is None:
        if i in (None, 0) or r is None:
            return None, "Щоб обчислити напругу, сила струму має бути ненульовою."
        return i * r, "Напруга (V)"
    if i is None:
        if r in (None, 0):
            return None, "Щоб обчислити силу струму, опір має бути ненульовим."
        return v / r, "Сила струму (A)"
    if r is None:
        if i in (None, 0):
            return None, "Щоб обчислити опір, сила струму має бути ненульовою."
        return v / i, "Опір (Ω)"
    return None, "Введіть рівно два відомі значення."


def power_solve(v=None, i=None, p=None):
    """Given exactly two of (voltage, current, power), solve the third using P = VI."""
    if p is None:
        if v is None or i is None:
            return None, "Для обчислення потужності потрібні напруга й сила струму."
        return v * i, "Потужність (W)"
    if v is None:
        if i in (None, 0):
            return None, "Щоб обчислити напругу, сила струму має бути ненульовою."
        return p / i, "Напруга (V)"
    if i is None:
        if v in (None, 0):
            return None, "Щоб обчислити силу струму, напруга має бути ненульовою."
        return p / v, "Сила струму (A)"
    return None, "Введіть рівно два відомі значення."


def energy_kwh(power_w, hours):
    """Energy in kWh from power (Watts) used over a number of hours."""
    return (power_w * hours) / 1000.0


def series_resistance(values):
    """Total resistance of resistors in series: simple sum."""
    return sum(values)


def parallel_resistance(values):
    """Total resistance of resistors in parallel: 1/Rt = sum(1/R)."""
    values = [v for v in values if v > 0]
    if not values:
        return None
    return 1.0 / sum(1.0 / v for v in values)


def ac_peak_from_rms(v_rms):
    return v_rms * (2 ** 0.5)


def ac_rms_from_peak(v_peak):
    return v_peak / (2 ** 0.5)


def kcl_check(currents_in, currents_out):
    """Kirchhoff's Current Law: sum(in) should equal sum(out) at a node."""
    total_in = sum(currents_in)
    total_out = sum(currents_out)
    balanced = abs(total_in - total_out) < 1e-9
    return balanced, total_in, total_out


def kvl_check(source_voltage, drops):
    """Kirchhoff's Voltage Law: source voltage should equal the sum of drops
    around a single closed loop."""
    total_drops = sum(drops)
    balanced = abs(source_voltage - total_drops) < 1e-9
    return balanced, total_drops


# ============================================================================
# CORE CONCEPTS DATA
# 10 foundational electrical concepts, each with the fields the Explorer /
# Comparison pages need. "calc_key" links a concept to its interactive
# render function further down.
# ============================================================================
CONCEPTS = {
    "Voltage": {
        "label": "Напруга",
        "desc": "Різниця електричних потенціалів між двома точками, яка зумовлює протікання струму в колі.",
        "unit": "Вольт (V)",
        "formula": "V = I × R",
        "category": ["basic_quantity", "source"],
        "explanation": "Напруга подібна до перепаду тиску в трубі. За однакового опору більша напруга спричиняє більший струм. Напругу завжди вимірюють *між двома точками*.",
        "applications": "Номінальна напруга батарей, живлення від електромережі, шини живлення електронних пристроїв.",
        "safety": "Висока напруга може спричинити проходження небезпечного струму крізь тіло людини. Будьте особливо обережні поблизу обладнання під мережевою напругою.",
        "calc_key": "ohms_law",
    },
    "Current": {
        "label": "Сила струму",
        "desc": "Електричний заряд, що проходить через поперечний переріз провідника за одиницю часу.",
        "unit": "Ампер (A)",
        "formula": "I = V / R",
        "category": ["basic_quantity"],
        "explanation": "Сила струму подібна до витрати води в трубі. Завдяки струму в колі світиться лампа, обертається двигун або заряджається акумулятор.",
        "applications": "Вибір номіналу запобіжника й перерізу проводу, оцінювання ємності акумуляторів (mAh).",
        "safety": "Струм, що проходить крізь тіло, може бути небезпечним. Навіть кілька десятків міліамперів через серце становлять загрозу.",
        "calc_key": "ohms_law",
    },
    "Resistance": {
        "label": "Опір",
        "desc": "Величина, що характеризує протидію матеріалу проходженню електричного струму.",
        "unit": "Ом (Ω)",
        "formula": "R = V / I",
        "category": ["basic_quantity"],
        "explanation": "Опір нагадує звуження труби, яке обмежує потік води. Мідь добре проводить струм, а гума є добрим ізолятором.",
        "applications": "Обмеження струму, нагрівальні елементи, датчики (терморезистори й фоторезистори).",
        "safety": "Дотримуйтеся загальних правил безпеки під час роботи з низьковольтними колами.",
        "calc_key": "ohms_law",
    },
    "Power": {
        "label": "Потужність",
        "desc": "Кількість електричної енергії, що передається або перетворюється за одиницю часу, наприклад на тепло, світло чи механічну енергію.",
        "unit": "Ват (W)",
        "formula": "P = V × I",
        "category": ["basic_quantity", "energy_related"],
        "explanation": "Потужність показує, як швидко витрачається енергія. Лампа потужністю 100 W за той самий час перетворює вдвічі більше електричної енергії на світло й тепло, ніж лампа потужністю 50 W.",
        "applications": "Номінальна потужність приладів, добір джерел живлення, проєктування нагрівальних елементів.",
        "safety": "Велика потужність у малому просторі може спричинити перегрів. Перевіряйте, чи відповідають компоненти й проводка робочим навантаженням.",
        "calc_key": "power",
    },
    "Energy": {
        "label": "Енергія",
        "desc": "Електрична енергія, передана або перетворена за певний проміжок часу.",
        "unit": "Джоуль (J). Для обліку споживання використовують кіловат-години (kWh).",
        "formula": "Енергія (kWh) = потужність (kW) × час (h)",
        "category": ["energy_related"],
        "explanation": "Потужність показує, як *швидко* витрачається енергія. Енергія показує, *скільки* електроенергії витрачено загалом. У рахунку за електроенергію споживання вказують у кіловат-годинах.",
        "applications": "Облік електроенергії, розрахунок запасу енергії акумуляторів, порівняння енергоефективності.",
        "safety": "Дотримуйтеся загальних правил безпеки під час роботи з низьковольтними колами.",
        "calc_key": "energy",
    },
    "Charge": {
        "label": "Електричний заряд",
        "desc": "Властивість частинок і тіл, завдяки якій на них діє електричне поле. Упорядкований рух зарядів утворює електричний струм.",
        "unit": "Кулон (C)",
        "formula": "Q = I × t",
        "category": ["basic_quantity"],
        "explanation": "За сталої сили струму перенесений заряд дорівнює добутку сили струму на час. Наприклад, за сили струму 20 mA через поперечний переріз провідника за секунду проходить заряд 0,02 C.",
        "applications": "Ємність акумуляторів в ампер-годинах, накопичення заряду в конденсаторах, статична електрика.",
        "safety": "Дотримуйтеся загальних правил безпеки під час роботи з низьковольтними колами.",
        "calc_key": None,
    },
    "Frequency (AC)": {
        "label": "Частота змінного струму",
        "desc": "Кількість повних циклів змінного струму або напруги за секунду.",
        "unit": "Герц (Hz)",
        "formula": "f = 1 / T",
        "category": ["ac_dc"],
        "explanation": "Струм в електромережі періодично змінює напрямок. Частота показує, скільки повних циклів відбувається за секунду. У більшості країн частота мережі становить 50 або 60 Hz.",
        "applications": "Електромережі, звукові сигнали, радіозв’язок.",
        "safety": "Дотримуйтеся загальних правил безпеки під час роботи з низьковольтними колами.",
        "calc_key": "ac",
    },
    "Conductors & Insulators": {
        "label": "Провідники та ізолятори",
        "desc": "Матеріали, які розрізняють за здатністю проводити електричний струм.",
        "unit": "Характеризують якісно або за питомим опором (Ω·m)",
        "formula": "Не застосовується",
        "category": ["materials"],
        "explanation": "У провідниках, як-от мідь та алюміній, є електрони, які можуть вільно переміщатися. У гумі й пластмасі електрони міцно зв’язані, тому ці матеріали використовують для ізоляції проводів.",
        "applications": "Проводка (мідна жила й пластмасова ізоляція), доріжки друкованих плат, високовольтні ізолятори на лініях електропередачі.",
        "safety": "Пошкоджена ізоляція може оголити провідник під напругою, що створює ризик ураження струмом і пожежі. Перевіряйте кабелі на порізи та зношення.",
        "calc_key": None,
    },
    "AC vs DC": {
        "label": "Змінний і постійний струм",
        "desc": "Постійний струм (DC) тече в одному напрямку. Змінний струм (AC) періодично змінює напрямок.",
        "unit": "Не застосовується",
        "formula": "Не застосовується",
        "category": ["ac_dc", "source"],
        "explanation": "Батарея є джерелом постійного струму. У побутовій електромережі використовують змінний струм. Його напругу легко змінювати трансформаторами, що дає змогу ефективно передавати енергію на великі відстані.",
        "applications": "Постійний струм використовують у батареях, живленні через USB та електроніці. Змінний струм використовують в електромережах і двигунах.",
        "safety": "Мережева напруга небезпечна. Проводьте роботи з побутовою електромережею лише під наглядом кваліфікованого фахівця.",
        "calc_key": None,
    },
    "Series & Parallel Circuits": {
        "label": "Послідовне та паралельне з’єднання",
        "desc": "Компоненти можна з’єднати послідовно, один за одним, або паралельно, між тими самими двома вузлами.",
        "unit": "Не застосовується",
        "formula": "Послідовно: Rt = R1+R2+…  |  Паралельно: 1/Rt = 1/R1+1/R2+…",
        "category": ["circuit_configuration"],
        "explanation": "У послідовному колі через усі компоненти тече той самий струм, а напруга розподіляється між ними. У паралельному колі напруга на всіх гілках однакова, а струм розподіляється між гілками.",
        "applications": "Побутова проводка (розетки з’єднані паралельно), гірлянди (у старих моделях лампи часто з’єднували послідовно), акумуляторні блоки (послідовне з’єднання підвищує напругу, паралельне збільшує ємність).",
        "safety": "Дотримуйтеся загальних правил безпеки під час роботи з низьковольтними колами.",
        "calc_key": "series_parallel",
    },
}

CONCEPT_ORDER = list(CONCEPTS.keys())
CATEGORY_LABELS = {
    "basic_quantity": "Основні величини",
    "energy_related": "Енергія та потужність",
    "ac_dc": "Змінний і постійний струм",
    "materials": "Матеріали",
    "source": "Джерела живлення",
    "circuit_configuration": "З’єднання в колі",
}

# ============================================================================
# LAWS DATA
# ============================================================================
LAWS = {
    "Закон Ома": {
        "formula": "V = I × R",
        "explanation": "Напруга на резисторі дорівнює добутку сили струму, що проходить через нього, на його опір. Це основне співвідношення для аналізу електричних кіл.",
        "use": "Обчислення напруги, сили струму або опору за двома відомими величинами.",
    },
    "Формула електричної потужності": {
        "formula": "P = V × I  (також P = I²R або P = V²/R)",
        "explanation": "Електрична потужність дорівнює добутку напруги на силу струму. За законом Ома її також можна виразити через опір і силу струму або через опір і напругу.",
        "use": "Добір джерел живлення, розрахунок тепловиділення, вибір компонентів за допустимою потужністю.",
    },
    "Перший закон Кірхгофа (KCL)": {
        "formula": "ΣI(вх) = ΣI(вих)",
        "explanation": "У кожному вузлі кола сума вхідних струмів дорівнює сумі вихідних. Електричний заряд у вузлі зберігається.",
        "use": "Аналіз кіл із кількома гілками, що сходяться в одному вузлі.",
    },
    "Другий закон Кірхгофа (KVL)": {
        "formula": "Σ V(джерел) = Σ V(спадів)",
        "explanation": "У замкненому контурі алгебраїчна сума напруг джерел дорівнює алгебраїчній сумі спадів напруги на компонентах.",
        "use": "Аналіз кіл із кількома компонентами в одному чи кількох контурах.",
    },
    "Опір за послідовного з’єднання": {
        "formula": "Rt = R1 + R2 + R3 + …",
        "explanation": "За послідовного з’єднання опори резисторів додаються. Загальний опір більший за найбільший з окремих додатних опорів.",
        "use": "Розрахунок загального опору в колі з однією гілкою.",
    },
    "Опір за паралельного з’єднання": {
        "formula": "1/Rt = 1/R1 + 1/R2 + 1/R3 + …",
        "explanation": "За паралельного з’єднання резисторів між тими самими вузлами загальний опір менший за найменший з окремих додатних опорів.",
        "use": "Розрахунок загального опору, коли струм має кілька шляхів проходження.",
    },
}

# ============================================================================
# SVG SCHEMATIC SYMBOLS
# Clean, standard-style diagrams illustrating each concept. Every returned
# string is flattened to one line with flat() so Streamlit's Markdown
# renderer never mis-parses an embedded blank line as the end of the block.
# ============================================================================
CONCEPT_COLORS = {
    "Voltage": "#f97316",
    "Current": "#3b82f6",
    "Resistance": "#8b5cf6",
    "Power": "#eab308",
    "Energy": "#22c55e",
    "Charge": "#ec4899",
    "Frequency (AC)": "#06b6d4",
    "Conductors & Insulators": "#84cc16",
    "AC vs DC": "#f43f5e",
    "Series & Parallel Circuits": "#0ea5e9",
}


def _lead(x1, y1, x2, y2, color="#111827", width=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def draw_concept_svg(name):
    """Return a flattened, single-line SVG diagram illustrating the concept."""
    color = CONCEPT_COLORS.get(name, "#3b82f6")
    open_tag = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg" width="100%" height="170">'
    close_tag = "</svg>"

    if name == "Voltage":
        # Battery symbol: long thin plate (+) and short thick plate (-), repeated
        body = f"""
        {_lead(0, 70, 70, 70)}
        <line x1="70" y1="30" x2="70" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="85" y1="45" x2="85" y2="95" stroke="{color}" stroke-width="9"/>
        <line x1="100" y1="30" x2="100" y2="110" stroke="{color}" stroke-width="4"/>
        <line x1="115" y1="45" x2="115" y2="95" stroke="{color}" stroke-width="9"/>
        {_lead(115, 70, 220, 70)}
        <text x="60" y="20" font-size="18" font-weight="bold" fill="#111827">+</text>
        <text x="108" y="128" font-size="18" font-weight="bold" fill="#111827">−</text>
        """

    elif name == "Current":
        # Wire with a directional current arrow
        body = f"""
        {_lead(15, 70, 205, 70, color, 5)}
        <polygon points="180,70 160,58 160,82" fill="{color}"/>
        <text x="90" y="45" font-size="15" font-weight="bold" fill="#111827">I</text>
        <circle cx="30" cy="70" r="4" fill="{color}"/>
        <circle cx="60" cy="70" r="4" fill="{color}"/>
        <circle cx="90" cy="70" r="4" fill="{color}"/>
        """

    elif name == "Resistance":
        body = f"""
        {_lead(0, 70, 60, 70)}
        <path d="M60,70 L72,45 L88,95 L104,45 L120,95 L136,45 L150,70"
              fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>
        {_lead(150, 70, 220, 70)}
        """

    elif name == "Power":
        # Lightning bolt inside a circle
        body = f"""
        <circle cx="110" cy="70" r="55" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <polygon points="120,20 80,80 105,80 95,120 140,60 112,60" fill="{color}"/>
        """

    elif name == "Energy":
        # Battery + clock combined
        body = f"""
        <rect x="45" y="45" width="60" height="50" rx="6" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <rect x="103" y="60" width="8" height="20" fill="{color}"/>
        <circle cx="150" cy="70" r="40" fill="none" stroke="{color}" stroke-width="4"/>
        <line x1="150" y1="70" x2="150" y2="45" stroke="{color}" stroke-width="3"/>
        <line x1="150" y1="70" x2="168" y2="80" stroke="{color}" stroke-width="3"/>
        """

    elif name == "Charge":
        # Plus and minus charge circles with field lines
        body = f"""
        <circle cx="65" cy="70" r="28" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="55" y="80" font-size="26" font-weight="bold" fill="{color}">+</text>
        <circle cx="155" cy="70" r="28" fill="{color}22" stroke="{color}" stroke-width="4"/>
        <text x="147" y="80" font-size="30" font-weight="bold" fill="{color}">−</text>
        <line x1="93" y1="70" x2="127" y2="70" stroke="{color}" stroke-width="2" stroke-dasharray="4,4"/>
        """

    elif name == "Frequency (AC)":
        # Sine wave
        body = f"""
        {_lead(0, 70, 25, 70)}
        <path d="M25,70 C40,20 55,20 70,70 C85,120 100,120 115,70 C130,20 145,20 160,70 C175,120 190,120 205,70"
              fill="none" stroke="{color}" stroke-width="4"/>
        {_lead(205, 70, 220, 70)}
        """

    elif name == "Conductors & Insulators":
        # Bare wire (conductor) vs insulated wire cross-section
        body = f"""
        <circle cx="60" cy="70" r="22" fill="{color}" stroke="{color}" stroke-width="2"/>
        <text x="60" y="115" text-anchor="middle" font-size="12" font-weight="bold" fill="#111827">Провідник</text>
        <circle cx="160" cy="70" r="30" fill="none" stroke="#9ca3af" stroke-width="10"/>
        <circle cx="160" cy="70" r="16" fill="{color}"/>
        <text x="160" y="115" text-anchor="middle" font-size="12" font-weight="bold" fill="#111827">Провід в ізоляції</text>
        """

    elif name == "AC vs DC":
        # DC steady line vs AC sine wave, side by side
        body = f"""
        <line x1="15" y1="70" x2="95" y2="70" stroke="{color}" stroke-width="4"/>
        <text x="55" y="115" text-anchor="middle" font-size="13" font-weight="bold" fill="#111827">Постійний</text>
        <path d="M115,70 C127,35 138,35 150,70 C162,105 173,105 185,70 C197,35 205,35 210,55"
              fill="none" stroke="{color}" stroke-width="4"/>
        <text x="165" y="115" text-anchor="middle" font-size="13" font-weight="bold" fill="#111827">Змінний</text>
        <line x1="105" y1="20" x2="105" y2="120" stroke="#9ca3af" stroke-width="2" stroke-dasharray="3,3"/>
        """

    elif name == "Series & Parallel Circuits":
        # Two small diagrams: series resistors on top, parallel on bottom
        body = f"""
        {_lead(5, 35, 40, 35, color, 3)}
        <path d="M40,35 L48,22 L58,48 L68,22 L78,48 L86,35" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(86, 35, 105, 35, color, 3)}
        <path d="M105,35 L113,22 L123,48 L133,22 L143,48 L151,35" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(151, 35, 215, 35, color, 3)}
        <text x="0" y="20" font-size="11" font-weight="bold" fill="#111827">Послідовно</text>
        {_lead(5, 100, 5, 130, color, 3)}
        {_lead(215, 100, 215, 130, color, 3)}
        {_lead(5, 100, 60, 100, color, 3)}
        <path d="M60,100 L68,90 L78,112 L88,90 L96,100" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(96, 100, 215, 100)}
        {_lead(5, 130, 60, 130, color, 3)}
        <path d="M60,130 L68,120 L78,140 L88,120 L96,130" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>
        {_lead(96, 130, 215, 130, color, 3)}
        <text x="0" y="95" font-size="11" font-weight="bold" fill="#111827">Паралельно</text>
        """

    else:
        body = ""

    return flat(open_tag + body + close_tag)

# ============================================================================
# INTERACTIVE RENDER FUNCTIONS
# Each function draws its own widgets + results. key_prefix keeps widget
# keys unique when the same concept is rendered on more than one page.
# ============================================================================

def render_ohms_law_calc(key_prefix):
    st.markdown("**⚙️ Калькулятор закону Ома** — `V = I × R`")
    solve_for = st.radio(
        "Що обчислити?", ["Напруга (V)", "Сила струму (I)", "Опір (R)"],
        horizontal=True, key=f"{key_prefix}_ohm_solve",
    )
    c1, c2 = st.columns(2)
    if solve_for == "Напруга (V)":
        i = c1.number_input("Сила струму (A)", min_value=0.0, value=0.5, step=0.1, key=f"{key_prefix}_ohm_i")
        r = c2.number_input("Опір (Ω)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_ohm_r")
        result, label = ohms_law_solve(i=i, r=r)
        r_plot = r
    elif solve_for == "Сила струму (I)":
        v = c1.number_input("Напруга (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_ohm_v")
        r = c2.number_input("Опір (Ω)", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_ohm_r2")
        result, label = ohms_law_solve(v=v, r=r)
        r_plot = r
    else:
        v = c1.number_input("Напруга (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_ohm_v2")
        i = c2.number_input("Сила струму (A)", min_value=0.0, value=0.5, step=0.1, key=f"{key_prefix}_ohm_i2")
        result, label = ohms_law_solve(v=v, i=i)
        r_plot = result if result else 100

    if result is None:
        st.warning(f"⚠️ {label}")
    else:
        st.markdown(f'<div class="status-good">✅ {label} = {result:.3f}</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3))
        currents = [x * 0.05 for x in range(21)]
        voltages = [i_val * r_plot for i_val in currents]
        ax.plot(currents, voltages, color="#f97316", linewidth=2)
        ax.set_xlabel("Сила струму (A)")
        ax.set_ylabel("Напруга (V)")
        ax.set_title(f"Залежність V від I (R = {r_plot:.1f} Ω)")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


def render_power_calc(key_prefix):
    st.markdown("**⚙️ Калькулятор потужності** — `P = V × I`")
    solve_for = st.radio(
        "Що обчислити?", ["Потужність (P)", "Напруга (V)", "Сила струму (I)"],
        horizontal=True, key=f"{key_prefix}_pow_solve",
    )
    c1, c2 = st.columns(2)
    if solve_for == "Потужність (P)":
        v = c1.number_input("Напруга (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_pow_v")
        i = c2.number_input("Сила струму (A)", min_value=0.0, value=2.0, step=0.1, key=f"{key_prefix}_pow_i")
        result, label = power_solve(v=v, i=i)
    elif solve_for == "Напруга (V)":
        p = c1.number_input("Потужність (W)", min_value=0.0, value=24.0, step=1.0, key=f"{key_prefix}_pow_p")
        i = c2.number_input("Сила струму (A)", min_value=0.0, value=2.0, step=0.1, key=f"{key_prefix}_pow_i2")
        result, label = power_solve(p=p, i=i)
    else:
        p = c1.number_input("Потужність (W)", min_value=0.0, value=24.0, step=1.0, key=f"{key_prefix}_pow_p2")
        v = c2.number_input("Напруга (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_pow_v2")
        result, label = power_solve(p=p, v=v)

    if result is None:
        st.warning(f"⚠️ {label}")
    else:
        st.markdown(f'<div class="status-good">✅ {label} = {result:.3f}</div>', unsafe_allow_html=True)


def render_energy_calc(key_prefix):
    st.markdown("**⚙️ Калькулятор споживання енергії** — `Енергія (kWh) = потужність (kW) × час (h)`")
    c1, c2 = st.columns(2)
    power_w = c1.number_input("Потужність приладу (W)", min_value=0.0, value=1000.0, step=50.0, key=f"{key_prefix}_energy_p")
    hours = c2.number_input("Тривалість роботи (h)", min_value=0.0, value=3.0, step=0.5, key=f"{key_prefix}_energy_h")
    kwh = energy_kwh(power_w, hours)
    st.markdown(f'<div class="status-good">✅ Спожита енергія ≈ {kwh:.3f} kWh</div>', unsafe_allow_html=True)
    st.caption("Лічильник реєструє спожиту енергію. За сталої потужності вона дорівнює добутку потужності на час роботи.")


def render_series_parallel_calc(key_prefix):
    st.markdown("**⚙️ Калькулятор опору для послідовного й паралельного з’єднань**")
    mode = st.radio("Тип з’єднання", ["Послідовне", "Паралельне"], horizontal=True, key=f"{key_prefix}_sp_mode")
    n = st.slider("Кількість резисторів", 2, 5, 2, key=f"{key_prefix}_sp_n")
    values = []
    cols = st.columns(n)
    for idx in range(n):
        v = cols[idx].number_input(f"R{idx+1} (Ω)", min_value=0.1, value=100.0, step=10.0, key=f"{key_prefix}_sp_r{idx}")
        values.append(v)
    if mode == "Послідовне":
        total = series_resistance(values)
        st.markdown(f'<div class="status-good">✅ Загальний опір за послідовного з’єднання = {total:.2f} Ω</div>', unsafe_allow_html=True)
        st.caption("За послідовного з’єднання загальний опір більший за найбільший з окремих опорів.")
    else:
        total = parallel_resistance(values)
        st.markdown(f'<div class="status-good">✅ Загальний опір за паралельного з’єднання = {total:.2f} Ω</div>', unsafe_allow_html=True)
        st.caption("За паралельного з’єднання загальний опір менший за найменший з окремих опорів.")


def render_ac_calc(key_prefix):
    st.markdown("**⚙️ Амплітудне й діюче значення змінної напруги**")
    direction = st.radio("Напрям перетворення", ["Діюче → амплітудне", "Амплітудне → діюче"], horizontal=True, key=f"{key_prefix}_ac_dir")
    if direction == "Діюче → амплітудне":
        vrms = st.number_input("Діюча напруга (V)", min_value=0.0, value=230.0, step=1.0, key=f"{key_prefix}_ac_rms")
        vpeak = ac_peak_from_rms(vrms)
        st.markdown(f'<div class="status-good">✅ Амплітудна напруга ≈ {vpeak:.2f} V</div>', unsafe_allow_html=True)
    else:
        vpeak = st.number_input("Амплітудна напруга (V)", min_value=0.0, value=325.0, step=1.0, key=f"{key_prefix}_ac_peak")
        vrms = ac_rms_from_peak(vpeak)
        st.markdown(f'<div class="status-good">✅ Діюча напруга ≈ {vrms:.2f} V</div>', unsafe_allow_html=True)
    st.caption("Діюче (середньоквадратичне, RMS) значення змінної напруги дорівнює сталій напрузі, за якої на тому самому резисторі виділяється така сама середня потужність. Калькулятор призначений для синусоїдальної напруги.")
    fig, ax = plt.subplots(figsize=(4.5, 3))
    import math
    t = [x * 0.02 for x in range(101)]
    wave = [vpeak * math.sin(2 * math.pi * x) for x in t]
    ax.plot(t, wave, color="#06b6d4", linewidth=2)
    ax.axhline(vrms, color="#f97316", linestyle="--", linewidth=1.5, label="Діюче значення")
    ax.axhline(-vrms, color="#f97316", linestyle="--", linewidth=1.5)
    ax.set_xlabel("Час (у періодах)")
    ax.set_ylabel("Напруга (V)")
    ax.set_title("Синусоїда, амплітуда й діюче значення")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


CALC_RENDERERS = {
    "ohms_law": render_ohms_law_calc,
    "power": render_power_calc,
    "energy": render_energy_calc,
    "series_parallel": render_series_parallel_calc,
    "ac": render_ac_calc,
}

def render_kcl_kvl_sim(key_prefix):
    st.markdown("**⚙️ Перевірка законів Кірхгофа**")
    law = st.radio("Який закон перевірити?", ["Перший закон (KCL)", "Другий закон (KVL)"], horizontal=True, key=f"{key_prefix}_kirch_law")
    if law == "Перший закон (KCL)":
        st.caption("Введіть значення струмів, що входять у вузол і виходять з нього.")
        c1, c2 = st.columns(2)
        in1 = c1.number_input("Вхідний струм 1 (A)", min_value=0.0, value=3.0, step=0.5, key=f"{key_prefix}_kcl_in1")
        in2 = c1.number_input("Вхідний струм 2 (A)", min_value=0.0, value=2.0, step=0.5, key=f"{key_prefix}_kcl_in2")
        out1 = c2.number_input("Вихідний струм 1 (A)", min_value=0.0, value=3.0, step=0.5, key=f"{key_prefix}_kcl_out1")
        out2 = c2.number_input("Вихідний струм 2 (A)", min_value=0.0, value=2.0, step=0.5, key=f"{key_prefix}_kcl_out2")
        balanced, total_in, total_out = kcl_check([in1, in2], [out1, out2])
        if balanced:
            st.markdown(f'<div class="status-good">✅ Баланс виконується. Сума вхідних струмів ({total_in:.2f} A) дорівнює сумі вихідних ({total_out:.2f} A).</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-bad">⛔ Баланс порушено. Сума вхідних струмів становить {total_in:.2f} A, сума вихідних — {total_out:.2f} A. У вузлі ці суми мають збігатися.</div>', unsafe_allow_html=True)
    else:
        st.caption("Введіть напругу джерела та спади напруги в одному замкненому контурі.")
        c1, c2 = st.columns(2)
        source = c1.number_input("Напруга джерела (V)", min_value=0.0, value=12.0, step=0.5, key=f"{key_prefix}_kvl_src")
        d1 = c2.number_input("Спад напруги на R1 (V)", min_value=0.0, value=7.0, step=0.5, key=f"{key_prefix}_kvl_d1")
        d2 = c2.number_input("Спад напруги на R2 (V)", min_value=0.0, value=5.0, step=0.5, key=f"{key_prefix}_kvl_d2")
        balanced, total_drops = kvl_check(source, [d1, d2])
        if balanced:
            st.markdown(f'<div class="status-good">✅ Баланс виконується. Напруга джерела ({source:.2f} V) дорівнює сумі спадів напруги ({total_drops:.2f} V).</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-bad">⛔ Баланс порушено. Напруга джерела становить {source:.2f} V, сума спадів напруги — {total_drops:.2f} V. У цьому замкненому контурі ці значення мають збігатися.</div>', unsafe_allow_html=True)


CALC_RENDERERS["kirchhoff"] = render_kcl_kvl_sim


# ============================================================================
# QUIZ DATA (10 questions, 3 options each)
# ============================================================================
QUIZ = [
    {"q": "1. Що таке напруга між двома точками кола?", "options": ["Заряд, що проходить за одиницю часу", "Різниця електричних потенціалів", "Міра протидії проходженню струму"], "answer": "Різниця електричних потенціалів"},
    {"q": "2. У чому вимірюють силу струму?", "options": ["Вольт", "Ом", "Ампер"], "answer": "Ампер"},
    {"q": "3. Як за законом Ома зміниться сила струму, якщо збільшити напругу за сталого опору?", "options": ["Збільшиться", "Зменшиться", "Залишиться сталою"], "answer": "Збільшиться"},
    {"q": "4. За якою формулою обчислюють електричну потужність?", "options": ["P = V × I", "P = V / I", "P = I / V"], "answer": "P = V × I"},
    {"q": "5. Що вимірюють у кіловат-годинах (kWh)?", "options": ["Потужність", "Опір", "Енергія"], "answer": "Енергія"},
    {"q": "6. Яка величина однакова для всіх компонентів послідовного кола?", "options": ["Напруга", "Сила струму", "Опір"], "answer": "Сила струму"},
    {"q": "7. Яка величина однакова на всіх гілках паралельного кола?", "options": ["Напруга", "Сила струму", "Потужність"], "answer": "Напруга"},
    {"q": "8. Що стверджує перший закон Кірхгофа?", "options": ["Сума вхідних струмів у вузлі дорівнює сумі вихідних", "Напруга завжди стала", "Опір завжди сталий"], "answer": "Сума вхідних струмів у вузлі дорівнює сумі вихідних"},
    {"q": "9. Яка ознака характеризує змінний струм (AC)?", "options": ["Тече лише в одному напрямку", "Періодично змінює напрямок", "Існує лише в батареях"], "answer": "Періодично змінює напрямок"},
    {"q": "10. Як називають матеріал, що добре проводить струм?", "options": ["Ізолятор", "Провідник", "Резистор"], "answer": "Провідник"},
]

# ============================================================================
# TROUBLESHOOTING SCENARIOS (5 scenarios, immediate feedback)
# ============================================================================
TROUBLESHOOTING = [
    {
        "scenario": "Ви виміряли 0 V на справному резисторі в послідовному колі. Джерело живлення ввімкнене й напруга на його затискачах відповідає очікуваній.",
        "question": "Яка найімовірніша причина?",
        "options": ["Десь на шляху струму є розрив кола", "Компонент має занадто малий опір", "Частота занадто висока"],
        "answer": "Десь на шляху струму є розрив кола",
        "explanation": "Якщо в послідовній гілці є розрив, струм у ній не тече. Тому спад напруги на справному резистивному компоненті цієї гілки дорівнює нулю.",
    },
    {
        "scenario": "Запобіжник щоразу перегорає невдовзі після ввімкнення кола.",
        "question": "Про що це свідчить?",
        "options": ["Струм у колі перевищує номінал запобіжника", "Джерело напруги занадто стабільне", "Опір занадто великий"],
        "answer": "Струм у колі перевищує номінал запобіжника",
        "explanation": "Якщо запобіжник неодноразово перегорає, імовірно, струм завеликий. Часті причини — коротке замикання, перевантаження або несправність компонента.",
    },
    {
        "scenario": "Два резистори з’єднані паралельно. За вашим розрахунком загальний опір більший за опір кожного з них.",
        "question": "Де помилка?",
        "options": ["У розрахунку є помилка. Загальний опір має бути меншим за найменший з окремих опорів", "Для паралельного кола такий результат правильний", "За паралельного з’єднання опори додаються"],
        "answer": "У розрахунку є помилка. Загальний опір має бути меншим за найменший з окремих опорів",
        "explanation": "Додаткова паралельна гілка дає струму ще один шлях. Загальний опір стає меншим за опір кожної окремої гілки.",
    },
    {
        "scenario": "У вузол входить струм 5 A. За вимірюваннями через видимі гілки з нього виходить лише 3 A.",
        "question": "Що слід перевірити за першим законом Кірхгофа?",
        "options": ["Пошукати невраховану гілку, через яку виходять решта 2 A", "Припустити, що закон тут не діє", "Проігнорувати розбіжність"],
        "answer": "Пошукати невраховану гілку, через яку виходять решта 2 A",
        "explanation": "За першим законом Кірхгофа суми вхідних і вихідних струмів мають збігатися. Перевірте, чи врахували всі гілки й чи правильно виміряли струм.",
    },
    {
        "scenario": "Прилад потужністю 2000 W працював 3 години. Хтось стверджує, що він спожив 2000 kWh.",
        "question": "Який результат правильний?",
        "options": ["Прилад потужністю 2000 W за 3 години споживає 6 kWh", "Потужність і енергія — та сама величина", "Прилад спожив 2000 kWh"],
        "answer": "Прилад потужністю 2000 W за 3 години споживає 6 kWh",
        "explanation": "Переведіть потужність у кіловати, а тоді помножте її на час роботи: 2 kW × 3 h = 6 kWh.",
    },
]

# ============================================================================
# SESSION STATE INITIALISATION
# ============================================================================
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {i: None for i in range(len(QUIZ))}

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.title("🔋 ОСНОВИ ЕЛЕКТРОТЕХНІКИ")
st.sidebar.subheader("НАВЧАЛЬНА ЛАБОРАТОРІЯ")
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Порядок роботи**")
st.sidebar.markdown(
    "1. Почніть зі вступу\n"
    "2. Ознайомтеся з основними поняттями\n"
    "3. Вивчіть основні закони\n"
    "4. Поекспериментуйте із симулятором\n"
    "5. Розгляньте практичні застосування\n"
    "6. Розберіть типові несправності\n"
    "7. Пройдіть тест"
)
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Навігація",
    [
        "🏠 Вступ",
        "🔎 Основні поняття",
        "📐 Закони та співвідношення",
        "🎛️ Інтерактивний симулятор",
        "🔬 Практичні застосування",
        "🧪 Лабораторія діагностики",
        "📝 Тест",
    ],
)
st.sidebar.markdown("---")
st.sidebar.info("💡 Проходьте розділи по черзі, щоб спиратися на вже вивчене.")

# ============================================================================
# TOP DASHBOARD (visible on every page)
# ============================================================================
st.title("🔋 Навчальна лабораторія з основ електротехніки")
st.caption("Інтерактивний посібник з основ електротехніки для початківців")
d1, d2, d3, d4 = st.columns(4)
d1.metric("🔎 Основні поняття", len(CONCEPTS))
d2.metric("📐 Основні закони", len(LAWS))
d3.metric("🧪 Завдання з діагностики", len(TROUBLESHOOTING))
d4.metric("📝 Тест Questions", len(QUIZ))
st.markdown("---")

# ============================================================================
# 1. INTRODUCTION
# ============================================================================
if page.startswith("🏠"):
    st.header("🏠 Вступ до основ електротехніки")

    st.markdown(
        """
        ### Що таке електричний струм?
        **Електричний струм** — це впорядкований рух заряджених частинок.
        У металах, наприклад у мідному проводі, носіями заряду є **електрони**.

        Для опису електричних кіл використовують кілька основних величин:
        напругу, силу струму, опір, потужність та енергію. З них починається
        вивчення електроніки.
        """
    )

    st.subheader("💧 Аналогія з водою в трубі")
    st.write("Рух води в трубах допомагає уявити зв’язок між напругою, силою струму й опором.")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(
            '<div class="concept-card"><h4>💧 Напруга → перепад тиску</h4>'
            '<p>Перепад тиску змушує воду текти. За однакового звуження більший перепад дає більшу витрату води.</p></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="concept-card"><h4>🌊 Сила струму → витрата води</h4>'
            '<p>Кількість води, що проходить через поперечний переріз труби за секунду.</p></div>',
            unsafe_allow_html=True,
        )
    with b3:
        st.markdown(
            '<div class="concept-card"><h4>🚧 Опір → звуження</h4>'
            '<p>Звуження труби обмежує витрату води за певного перепаду тиску.</p></div>',
            unsafe_allow_html=True,
        )
    st.caption(
        "⚠️ Ця аналогія спрощена. У реальних електричних колах "
        "діють електричні та магнітні поля."
    )

    st.subheader("⚡ Навіщо вивчати основи")
    st.markdown(
        '<div class="app-card">Роботу резисторів, конденсаторів, '
        'транзисторів та інтегральних схем описують ті самі закони, що пов’язують напругу, силу струму, '
        'опір, потужність та енергію. Ці поняття допоможуть вам '
        'розібратися в складніших темах електроніки.</div>',
        unsafe_allow_html=True,
    )

    st.success("👉 Відкрийте розділ **«Основні поняття»** в бічному меню, щоб докладніше розглянути кожне з них.")

# ============================================================================
# 2. CORE CONCEPTS EXPLORER
# ============================================================================
elif page.startswith("🔎"):
    st.header("🔎 Основні поняття")
    st.caption("Розгорніть картку поняття, щоб побачити схему, основні відомості, пояснення та калькулятор, якщо він доступний.")

    for name in CONCEPT_ORDER:
        c = CONCEPTS[name]
        with st.expander(f"**{c['label']}** — {c['desc']}", expanded=False):
            col1, col2 = st.columns([1, 1.3])
            with col1:
                st.markdown(f'<div class="symbol-box">{draw_concept_svg(name)}</div>', unsafe_allow_html=True)
                st.markdown(f"**Одиниця вимірювання** {c['unit']}")
                st.markdown(f"**Формула** `{c['formula']}`")
            with col2:
                st.markdown(f"**Простими словами** {c['explanation']}")
                st.markdown(f"**Типові застосування** {c['applications']}")
                if c["safety"]:
                    st.markdown(f'<div class="safety-note">⚠️ {c["safety"]}</div>', unsafe_allow_html=True)

            if c["calc_key"] is not None:
                st.markdown("---")
                CALC_RENDERERS[c["calc_key"]](key_prefix=f"explorer_{name}")

# ============================================================================
# 3. LAWS & RELATIONSHIPS
# ============================================================================
elif page.startswith("📐"):
    st.header("📐 Закони та співвідношення")
    st.caption("Основні математичні співвідношення для аналізу електричних кіл.")

    filter_tags = st.multiselect(
        "Фільтр за категорією",
        list(CATEGORY_LABELS),
        default=[],
        format_func=CATEGORY_LABELS.__getitem__,
    )
    if filter_tags:
        filtered_names = [n for n in CONCEPT_ORDER if any(t in CONCEPTS[n]["category"] for t in filter_tags)]
    else:
        filtered_names = CONCEPT_ORDER

    st.subheader("🧮 Довідкова таблиця понять")
    rows = []
    for name in filtered_names:
        c = CONCEPTS[name]
        rows.append({
            "Поняття": c["label"],
            "Одиниця вимірювання": c["unit"],
            "Формула": c["formula"],
            "Категорія": ", ".join(CATEGORY_LABELS[tag] for tag in c["category"]),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📏 Основні закони")
    for law_name, law in LAWS.items():
        with st.expander(f"**{law_name}** — `{law['formula']}`"):
            st.markdown(f"**Пояснення** {law['explanation']}")
            st.markdown(f"**Застосування** {law['use']}")

# ============================================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================================
elif page.startswith("🎛️"):
    st.header("🎛️ Інтерактивний симулятор")
    st.caption("Виберіть поняття з інтерактивною моделлю й подивіться, як зміна параметрів впливає на результат.")

    simulatable = [n for n in CONCEPT_ORDER if CONCEPTS[n]["calc_key"] is not None]
    labels = {name: CONCEPTS[name]["label"] for name in simulatable}
    labels["kirchhoff"] = "Закони Кірхгофа"
    sel = st.selectbox("Виберіть поняття або закон", list(labels), format_func=labels.__getitem__)

    if sel == "kirchhoff":
        st.markdown(
            flat('<div class="comp-banner" style="background: linear-gradient(90deg, #7c3aed, #4c1d95);">'
                 '⚡ <b>Закони Кірхгофа</b> &nbsp;|&nbsp; Правила для струмів у вузлах і напруг у контурах</div>'),
            unsafe_allow_html=True,
        )
        render_kcl_kvl_sim(key_prefix="sim_kirchhoff")
    else:
        c = CONCEPTS[sel]
        st.markdown(
            flat(f'<div class="comp-banner" style="background: linear-gradient(90deg, #ea580c, #9a3412);">'
                 f'⚡ <b>{c["label"]}</b> &nbsp;|&nbsp; {c["desc"]}</div>'),
            unsafe_allow_html=True,
        )
        col_symbol, col_calc = st.columns([1, 1.6])
        with col_symbol:
            st.markdown("##### 🔷 Позначення або схема")
            st.markdown(f'<div class="symbol-box">{draw_concept_svg(sel)}</div>', unsafe_allow_html=True)
            st.markdown(f"**Одиниця вимірювання** {c['unit']}")
        with col_calc:
            CALC_RENDERERS[c["calc_key"]](key_prefix=f"sim_{sel}")

# ============================================================================
# 5. PRACTICAL APPLICATIONS
# ============================================================================
elif page.startswith("🔬"):
    st.header("🔬 Практичні застосування")
    st.caption("Дізнайтеся, як ці закони й поняття застосовують у техніці та побуті.")

    APPLICATIONS = [
        ("🏠 Побутова електропроводка", "Побутові розетки з’єднують паралельно. Кожна працює незалежно за тієї самої напруги. Автоматичний вимикач відключає коло в разі надмірного струму. Роботу такого кола пояснюють закон Ома й перший закон Кірхгофа."),
        ("🔋 Акумулятори й павербанки", "Послідовне з’єднання елементів підвищує загальну напругу, а паралельне збільшує ємність в ампер-годинах."),
        ("💡 Кола освітлення", "За однакового світлового потоку світлодіодні лампи мають меншу споживану потужність, ніж лампи розжарювання. За однаковий час роботи вони споживають менше електроенергії."),
        ("⚡ Мережі електропередачі", "Для передавання електроенергії на великі відстані підвищують змінну напругу. За тієї самої переданої потужності це зменшує струм і теплові втрати в проводах (P = I²R). Перед подачею до споживачів напругу знижують трансформаторами."),
        ("📱 Електронні пристрої", "Стабілізатори напруги та резистивні кола підтримують потрібні рівні напруги й струму для захисту чутливих компонентів. Під час їх розрахунку використовують закон Ома й формулу потужності."),
        ("🚗 Електромобілі", "Елементи акумуляторного блока з’єднують послідовно та паралельно, щоб отримати потрібні напругу та ємність. Запас енергії вимірюють у кіловат-годинах, а запас ходу залежить від енергії, яку автомобіль витрачає на кілометр."),
    ]
    for title, body in APPLICATIONS:
        with st.expander(title):
            st.markdown(f'<div class="app-card">{body}</div>', unsafe_allow_html=True)

# ============================================================================
# 6. TROUBLESHOOTING LAB
# ============================================================================
elif page.startswith("🧪"):
    st.header("🧪 Лабораторія діагностики")
    st.caption("Розгляньте кожну ситуацію, виберіть відповідь і прочитайте пояснення.")

    for idx, item in enumerate(TROUBLESHOOTING):
        st.markdown(f"##### Ситуація {idx + 1}")
        st.markdown(f'<div class="concept-card">{item["scenario"]}</div>', unsafe_allow_html=True)
        choice = st.radio(item["question"], item["options"], index=None, key=f"trouble_{idx}")
        if choice is not None:
            if choice == item["answer"]:
                st.markdown(f'<div class="status-good">✅ Правильно! {item["explanation"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="status-bad">❌ Правильна відповідь — <b>{item["answer"]}</b>. {item["explanation"]}</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("---")

# ============================================================================
# 7. QUIZ
# ============================================================================
elif page.startswith("📝"):
    st.header("📝 Тест з основ електротехніки")
    st.caption("10 запитань · 3 варіанти відповіді в кожному · результат у відсотках")

    with st.form("quiz_form"):
        for i, item in enumerate(QUIZ):
            st.markdown(f"**{item['q']}**")
            choice = st.radio(
                label=item["q"],
                options=item["options"],
                index=None,
                key=f"quiz_radio_{i}",
                label_visibility="collapsed",
            )
            st.session_state.quiz_answers[i] = choice
            st.markdown("")
        submitted = st.form_submit_button("✅ Завершити тест")

    if submitted:
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        answers = st.session_state.quiz_answers
        if any(v is None for v in answers.values()):
            st.warning("⚠️ Дайте відповіді на всі 10 запитань.")
        else:
            correct_count = sum(1 for i, item in enumerate(QUIZ) if answers[i] == item["answer"])
            score_pct = round((correct_count / len(QUIZ)) * 100)

            st.markdown("## 📊 Ваш результат")
            m1, m2 = st.columns(2)
            m1.metric("Правильні відповіді", f"{correct_count}/{len(QUIZ)}")
            m2.metric("Результат у відсотках", f"{score_pct}%")
            st.progress(score_pct / 100)

            if score_pct >= 80:
                st.success(f"🎉 Чудово! Ваш результат — {score_pct}%.")
                st.balloons()
            elif score_pct >= 50:
                st.info(f"👍 Ваш результат — {score_pct}%. Перегляньте запитання, у яких помилилися.")
            else:
                st.error(f"📚 Ваш результат — {score_pct}%. Перегляньте розділ «Основні поняття» та спробуйте ще раз.")

            st.markdown("### Розбір відповідей")
            for i, item in enumerate(QUIZ):
                user_ans = answers[i]
                is_correct = user_ans == item["answer"]
                icon = "✅" if is_correct else "❌"
                st.markdown(f"{icon} **{item['q']}**")
                st.write(f"Ваша відповідь — {user_ans}")
                if not is_correct:
                    st.write(f"Правильна відповідь — **{item['answer']}**")
                st.markdown("---")

            if st.button("🔄 Пройти тест ще раз"):
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {i: None for i in range(len(QUIZ))}
                for i in range(len(QUIZ)):
                    st.session_state.pop(f"quiz_radio_{i}", None)
                st.rerun()
