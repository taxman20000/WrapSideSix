from dataclasses import dataclass


@dataclass(frozen=True)
class WSUnicodes:
    # General
    ADD: str = "\u2795"  # ➕ Heavy Plus Sign
    DELETE: str = "\u2796"  # ➖ Heavy Minus Sign
    # UP_ARROW: str = "\u2B06"  # ⬆️ Upwards Black Arrow
    # DOWN_ARROW: str = "\u2B07"  # ⬇️ Downwards Black Arrow
    UP_ARROW: str = "\u2191"  # ↑ Upwards Arrow
    DOWN_ARROW: str = "\u2193"  # ↓ Downwards Arrow
    RIGHT_ARROW: str = "\u2192"  # → Right Arrow
    LEFT_ARROW: str = "\u2190"  # ← Left Arrow

    RIGHT_ARROW_BLACK: str = "\u27A1"  # ➡ Rightwards Black Arrow
    LEFT_ARROW_BLACK: str = "\u2B05"  # ⬅ Leftwards Black Arrow
    UP_ARROW_BLACK: str = "\u2B06"  # ⬆ Upwards Black Arrow
    DOWN_ARROW_BLACK: str = "\u2B07"  # ⬇ Downwards Black Arrow

    RIGHT_POINTING_HAND: str = "\U0001F449"  # 👉 Right-Pointing Hand
    LEFT_POINTING_HAND: str = "\U0001F448"  # 👈 Left-Pointing Hand
    UP_POINTING_HAND: str = "\U0001F446"  # 👆 Up-Pointing Hand
    DOWN_POINTING_HAND: str = "\U0001F447"  # 👇 Down-Pointing Hand

    SAVE: str = "\U0001F4BE"  # 💾 Floppy Disk
    RESET_CLEAR: str = "\U0001F504"  # 🔄 Anticlockwise Downwards and Upwards Open Circle Arrows
    CANCEL: str = "\u2716"  # ✖ Heavy Multiplication X
    IMPORT: str = "\U0001F4E5"  # 📥 Inbox Tray

    # Navigation
    FIRST: str = "\u23EE"  # ⏮ Black Left-Pointing Double Triangle
    PREVIOUS: str = "\u25C0"  # ◀ Black Left-Pointing Triangle
    LAST: str = "\u23ED"  # ⏭ Black Right-Pointing Double Triangle
    NEXT: str = "\u25B6"  # ▶ Black Right-Pointing Triangle

    # Formatting
    BOLD: str = "B"  # Bold text (represented by bold 'B')
    BULLET: str = "\u2022"  # • Bullet
    UNDERLINE: str = "\u0332"  # Combining Low Line
    CHECKMARK: str = "\u2714"  # ✔ Check Mark
    ITALIC: str = "I"  # Italic text (represented by italic 'I')
    TEXT: str = "\U0001F170"  # 🅰 A Button (Blood Type)

    # Actions
    COPY: str = "\U0001F5D2"  # 🗒 Two Pages
    PASTE: str = "\u27B0"  # ➰ Curling Loop
    COPY2: str = "\U0001F5CE"  # 🗒 Two Pages
    PASTE2: str = "\U0001F4CB"  # 📋 Clipboard
    SCISSORS: str = "\u2702"  # ✂ Black Scissors
    DELETE_ACTION: str = "\U0001F5D1"  # 🗑 Wastebasket
    FILTER: str = "\U0001F5DC"  # 🗜 Funnel
    FIND: str = "\U0001F50E"  # 🔎 Magnifying Glass Tilted Right
    NEW: str = "\U0001F195"  # 🆕 New Button
    PRINT: str = "\U0001F5A8"  # 🖨 Printer
    TEMPLATE: str = "\U0001F4C4"  # 📄 Page Facing Up
    SETTINGS_WRENCH: str = "\U0001F527"  # 🔧 Wrench
    # RENAME: str = "\u270F"  # ✏️ Pencil
    RENAME: str = "\U0001F4DD"  # ✏️ Pencil
    OPEN: str = "\U0001F4C2"  # 📂 Open File Folder
    CLOSE: str = "\u274C"  # ❌ Cross Mark
    FILE: str = "\U0001F4C1"  # 📁 File Folder
    PAGE_WITH_CURL: str = "\U0001F4C3"  # 📃 Page with Curl
    KEYBOARD: str = "\u2328"  # ⌨️ Keyboard

    # Media Control
    PLAY: str = "\u25B6"  # ▶ Black Right-Pointing Triangle
    PAUSE: str = "\u23F8"  # ⏸ Double Vertical Bar
    STOP: str = "\u23F9"  # ⏹ Black Square For Stop
    RECORD: str = "\u23FA"  # ⏺ Black Circle For Record

    # Edit Actions
    CUT: str = "\u2702"  # ✂ Black Scissors
    UNDO: str = "\u21A9"  # ↩ Leftwards Arrow with Hook
    REDO: str = "\u21AA"  # ↪ Rightwards Arrow with Hook
    SELECT_ALL: str = "\U0001F5F9"  # 🗈 Ballot Box With Check

    # User Interface Elements
    HOME: str = "\U0001F3E0"  # 🏠 House Building
    SETTINGS: str = "\u2699"  # ⚙ Gear
    HELP: str = "\u2753"  # ❓ Black Question Mark Ornament
    INFO: str = "\u2139"  # ℹ️ Information Source
    ALERT: str = "\u26A0"  # ⚠️ Warning Sign
    LOCK: str = "\U0001F512"  # 🔒 Lock
    UNLOCK: str = "\U0001F513"  # 🔓 Open Lock
    CALCULATOR: str = "\U0001F5A9"  # 🖩 Calculator
    ABACUS: str = "\U0001F9EE"  # 🧮 Abacus
    NUMBER_SYMBOL: str = "\U0001F522"  # 🔢 Keycap: 1234
    LATIN_LETTERS: str = "\U0001F524"  # 🔤 Input Symbol for Latin Letters

    # DB Records
    TAGS: str = "\U0001F3F7"  # 🏷️ Label
    STATUS: str = "\U0001F4CB"  # 📋 Clipboard
    GENERATE_HAMMER_WRENCH: str = "\U0001F6E0"  # 🛠 Hammer and Wrench
    GENERATE_HAMMER: str = "\U0001F528"  # 🔨 Hammer
    GENERATE_FACTORY: str = "\U0001F3ED"  # 🏭 Factory
