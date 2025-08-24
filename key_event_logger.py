import tkinter as tk
from datetime import datetime
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"keystrokes_{datetime.now():%Y%m%d_%H%M%S}.txt"

SESSION_HEADER = (
    "=== ENREGISTREUR DE FRAPPES (dans cette fenêtre uniquement) ===\n"
    f"Session démarrée : {datetime.now():%Y-%m-%d %H:%M:%S}\n"
    "⚠️ Les touches sont enregistrées UNIQUEMENT dans cette fenêtre, avec consentement.\n"
    "===============================================================\n"
)

def write_log(text: str, newline: bool = True):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + ("\n" if newline else ""))

write_log(SESSION_HEADER, newline=True)


root = tk.Tk()
root.title("Key Event Logger (Fenêtre uniquement • Avec consentement)")
root.geometry("800x400")

banner = tk.Label(
    root,
    text=(
        "Les touches saisies dans CETTE fenêtre seront enregistrées dans un fichier.\n"
        "Appuie sur ESC pour arrêter ou clique sur Quitter.\n"
        "Logs enregistrés dans ./logs/"
    ),
    font=("Segoe UI", 11),
    pady=8
)
banner.pack()

text = tk.Text(root, wrap="word", font=("Consolas", 12))
text.insert("1.0", "Clique ici et commence à taper. Seules ces touches seront enregistrées.\n")
text.pack(expand=True, fill="both")
text.focus_set()

def represent(event: tk.Event) -> str:
    """Donner une version lisible de la touche pressée"""
    ks = event.keysym
    ch = event.char

    if ks == "space":
        return " "
    if ks in ("Return", "KP_Enter"):
        return "\\n"
    if ks == "Tab":
        return "\\t"
    if ks == "BackSpace":
        return "[SUPPRIMER]"
    if ks == "Escape":
        return "[ESC]"
    if ch and ch.isprintable():
        return ch
    return f"[{ks}]"

def on_key(event: tk.Event):
    rep = represent(event)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    write_log(f"{timestamp} {rep}")

    if event.keysym == "Escape":
        root.quit()

root.bind("<KeyPress>", on_key)

btn = tk.Button(root, text="Quitter", command=root.quit)
btn.pack(pady=8)

root.mainloop()
