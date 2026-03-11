import random
import tkinter as tk
from tkinter import ttk

from flashCards import FlashCardDeck

KANA_CSV = "kana.csv"
JAP_VOCAB_CSV = "jap-vocab.csv"


class FlashcardsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kana Flashcards")
        self.root.geometry("680x420")

        self.decks = {
            "Kana": FlashCardDeck(KANA_CSV),
            "Vocabulary": FlashCardDeck(JAP_VOCAB_CSV),
        }

        self.deck_var = tk.StringVar(value="Kana")
        self.show_side_var = tk.StringVar(value="hiragana")
        self.answer_side_var = tk.StringVar(value="romaji")

        self.session_cards = []
        self.current_card = None
        self.total_answered = 0
        self.correct_answers = 0

        self._build_ui()
        self._sync_side_options()

    def _build_ui(self):
        controls = ttk.LabelFrame(self.root, text="Session Settings", padding=12)
        controls.pack(fill="x", padx=12, pady=(12, 6))

        ttk.Label(controls, text="Deck").grid(row=0, column=0, sticky="w")
        deck_combo = ttk.Combobox(
            controls,
            textvariable=self.deck_var,
            values=list(self.decks.keys()),
            width=14,
            state="readonly",
        )
        deck_combo.grid(row=0, column=1, padx=(8, 16), sticky="w")
        deck_combo.bind("<<ComboboxSelected>>", lambda _event: self._sync_side_options())

        ttk.Label(controls, text="Show Side").grid(row=0, column=2, sticky="w")
        self.show_side_combo = ttk.Combobox(controls, textvariable=self.show_side_var, width=16, state="readonly")
        self.show_side_combo.grid(row=0, column=3, padx=(8, 16), sticky="w")

        ttk.Label(controls, text="Answer Side").grid(row=0, column=4, sticky="w")
        self.answer_side_combo = ttk.Combobox(
            controls,
            textvariable=self.answer_side_var,
            width=16,
            state="readonly",
        )
        self.answer_side_combo.grid(row=0, column=5, padx=(8, 0), sticky="w")

        ttk.Button(controls, text="Start Session", command=self.start_session).grid(
            row=0, column=6, padx=(16, 0), sticky="e"
        )

        card_frame = ttk.LabelFrame(self.root, text="Card", padding=12)
        card_frame.pack(fill="both", expand=True, padx=12, pady=6)

        self.prompt_label = ttk.Label(card_frame, text="Click 'Start Session' to begin.", font=("Arial", 18))
        self.prompt_label.pack(pady=(24, 16))

        answer_row = ttk.Frame(card_frame)
        answer_row.pack()

        ttk.Label(answer_row, text="Your Answer:").pack(side="left")
        self.answer_entry = ttk.Entry(answer_row, width=30)
        self.answer_entry.pack(side="left", padx=(8, 8))
        self.answer_entry.bind("<Return>", lambda _event: self.submit_answer())

        ttk.Button(answer_row, text="Submit", command=self.submit_answer).pack(side="left")
        ttk.Button(answer_row, text="Next Card", command=self.next_card).pack(side="left", padx=(8, 0))

        self.feedback_label = ttk.Label(card_frame, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=(14, 4))

        self.score_label = ttk.Label(card_frame, text="Score: 0/0")
        self.score_label.pack()

    def _sync_side_options(self):
        deck = self.decks[self.deck_var.get()]
        options = [key for key in deck.cards[0].sides.keys() if key != "tags"]

        self.show_side_combo["values"] = options
        self.answer_side_combo["values"] = options

        if self.show_side_var.get() not in options:
            self.show_side_var.set(options[0])
        if self.answer_side_var.get() not in options:
            self.answer_side_var.set(options[min(1, len(options)-1)])

    def start_session(self):
        deck = self.decks[self.deck_var.get()]
        self.session_cards = [card for card in deck.cards if self._card_is_usable(card)]
        random.shuffle(self.session_cards)

        self.total_answered = 0
        self.correct_answers = 0
        self.score_label.config(text="Score: 0/0")
        self.feedback_label.config(text="")
        self.next_card()

    def _card_is_usable(self, card):
        shown = card.sides.get(self.show_side_var.get(), "n/a")
        answer = card.sides.get(self.answer_side_var.get(), "n/a")
        return shown != "n/a" and answer != "n/a"

    def next_card(self):
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")

        if not self.session_cards:
            self.current_card = None
            self.prompt_label.config(text="Session complete! Click 'Start Session' to play again.")
            return

        self.current_card = self.session_cards.pop()
        show_key = self.show_side_var.get()
        self.prompt_label.config(text=self.current_card.sides[show_key])
        self.answer_entry.focus_set()

    def submit_answer(self):
        if self.current_card is None:
            self.feedback_label.config(text="No active card. Start a session first.")
            return

        guess = self.answer_entry.get().strip()
        answer_key = self.answer_side_var.get()
        expected = self.current_card.sides[answer_key]

        self.total_answered += 1
        if guess == expected:
            self.correct_answers += 1
            self.feedback_label.config(text="✅ Correct!")
        else:
            self.feedback_label.config(text=f"❌ Incorrect. Answer: {expected}")

        self.score_label.config(text=f"Score: {self.correct_answers}/{self.total_answered}")


def run_gui():
    root = tk.Tk()
    FlashcardsGUI(root)
    root.mainloop()
