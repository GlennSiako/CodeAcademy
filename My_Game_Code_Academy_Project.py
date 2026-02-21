import tkinter as tk
from tkinter import ttk
import random
import time

# ── ROBOT DEFINITIONS ──────────────────────────────────────────────────────────
ROBOTS = [
    {
        "name": "Boltinator", "emoji": "⚡", "color": "#FFD700",
        "hp": 70, "attack": 28, "defense": 5, "speed": 9,
        "special_name": "THUNDERSTRIKE", "special_desc": "3x damage!",
        "special": lambda atk: {"dmg": atk * 3, "msg": "fires THUNDERSTRIKE! ⚡⚡⚡"}
    },
    {
        "name": "Ironclad", "emoji": "🛡️", "color": "#C0C0C0",
        "hp": 160, "attack": 14, "defense": 18, "speed": 3,
        "special_name": "IRON FORTRESS", "special_desc": "Heals 50 HP!",
        "special": lambda atk: {"heal": 50, "msg": "activates IRON FORTRESS! +50 HP 🛡️"}
    },
    {
        "name": "Inferno", "emoji": "🔥", "color": "#FF4500",
        "hp": 95, "attack": 22, "defense": 8, "speed": 6,
        "special_name": "FLAME BURST", "special_desc": "Burns enemy 3 turns!",
        "special": lambda atk: {"dmg": int(atk * 1.2), "burn": 3, "msg": "erupts with FLAME BURST! 🔥🔥🔥"}
    },
    {
        "name": "Frosty", "emoji": "🧊", "color": "#00BFFF",
        "hp": 110, "attack": 18, "defense": 12, "speed": 5,
        "special_name": "FREEZE RAY", "special_desc": "Enemy skips next turn!",
        "special": lambda atk: {"dmg": int(atk * 0.8), "freeze": True, "msg": "fires the FREEZE RAY! 🧊🧊🧊"}
    },
    {
        "name": "Boomer", "emoji": "💣", "color": "#FF69B4",
        "hp": 80, "attack": 35, "defense": 6, "speed": 4,
        "special_name": "KABOOM", "special_desc": "2.5x dmg, -25 self!",
        "special": lambda atk: {"dmg": int(atk * 2.5), "self_dmg": 25, "msg": "triggers KABOOM! 💥💥💥"}
    },
]

# ── GAME STATE ─────────────────────────────────────────────────────────────────
class GameState:
    def __init__(self):
        self.player = None
        self.enemy = None
        self.player_hp = 0
        self.enemy_hp = 0
        self.player_burn = 0
        self.enemy_burn = 0
        self.player_frozen = False
        self.enemy_frozen = False
        self.player_special_used = False
        self.enemy_special_used = False
        self.player_turn = True
        self.game_over = False

    def start(self, player_robot):
        self.player = player_robot
        self.enemy = random.choice([r for r in ROBOTS if r["name"] != player_robot["name"]])
        self.player_hp = player_robot["hp"]
        self.enemy_hp = self.enemy["hp"]
        self.player_burn = self.enemy_burn = 0
        self.player_frozen = self.enemy_frozen = False
        self.player_special_used = self.enemy_special_used = False
        self.player_turn = True
        self.game_over = False

# ── MAIN APP ───────────────────────────────────────────────────────────────────
class RobotRumble:
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ Robot Rumble")
        self.root.configure(bg="#0a0a1e")
        self.root.resizable(False, False)
        self.state = GameState()
        self.show_pick_screen()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ── PICK SCREEN ─────────────────────────────────────────────────────────────
    def show_pick_screen(self):
        self.clear()
        self.root.geometry("820x560")

        tk.Label(self.root, text="🤖 ROBOT RUMBLE", font=("Courier", 26, "bold"),
                 fg="#FFD700", bg="#0a0a1e").pack(pady=(18, 2))
        tk.Label(self.root, text="SELECT YOUR FIGHTER", font=("Courier", 10),
                 fg="#444", bg="#0a0a1e").pack(pady=(0, 16))

        frame = tk.Frame(self.root, bg="#0a0a1e")
        frame.pack()

        for i, robot in enumerate(ROBOTS):
            self.robot_card(frame, robot, i)

    def robot_card(self, parent, robot, col):
        card = tk.Frame(parent, bg="#0d0d22", bd=0, relief="flat",
                        highlightthickness=2, highlightbackground="#1a1a3e",
                        cursor="hand2", width=148, height=300)
        card.grid(row=0, column=col, padx=6, pady=4)
        card.grid_propagate(False)

        def hover_in(e):
            card.config(highlightbackground=robot["color"])
        def hover_out(e):
            card.config(highlightbackground="#1a1a3e")
        def click(e):
            self.state.start(robot)
            self.show_battle_screen()

        card.bind("<Enter>", hover_in)
        card.bind("<Leave>", hover_out)
        card.bind("<Button-1>", click)

        def bind_all(widget):
            widget.bind("<Enter>", hover_in)
            widget.bind("<Leave>", hover_out)
            widget.bind("<Button-1>", click)

        tk.Label(card, text=robot["emoji"], font=("Segoe UI Emoji", 28),
                 fg=robot["color"], bg="#0d0d22").pack(pady=(12, 2))
        tk.Label(card, text=robot["name"], font=("Courier", 10, "bold"),
                 fg=robot["color"], bg="#0d0d22").pack()
        bind_all(card.children.get(list(card.children)[-1], card))

        stats = [
            ("❤️ HP", robot["hp"], 160, "#00e676"),
            ("⚔️ ATK", robot["attack"], 35, "#FF6B6B"),
            ("🛡️ DEF", robot["defense"], 20, "#4ECDC4"),
            ("💨 SPD", robot["speed"], 10, "#FFD700"),
        ]

        for label, val, mx, color in stats:
            row = tk.Frame(card, bg="#0d0d22")
            row.pack(fill="x", padx=10, pady=1)
            tk.Label(row, text=label, font=("Courier", 7), fg="#555",
                     bg="#0d0d22", width=6, anchor="w").pack(side="left")
            tk.Label(row, text=str(val), font=("Courier", 7, "bold"),
                     fg=color, bg="#0d0d22", width=3, anchor="e").pack(side="right")
            bind_all(row)

            bar_frame = tk.Frame(card, bg="#111", height=4)
            bar_frame.pack(fill="x", padx=10, pady=0)
            fill = tk.Frame(bar_frame, bg=color, height=4,
                            width=int((val / mx) * 110))
            fill.place(x=0, y=0)

        spc = tk.Label(card, text=f"✨ {robot['special_name']}\n{robot['special_desc']}",
                       font=("Courier", 7), fg=robot["color"], bg="#0d0d22",
                       wraplength=130, justify="center")
        spc.pack(pady=(8, 10))

        for child in card.winfo_children():
            bind_all(child)

    # ── BATTLE SCREEN ────────────────────────────────────────────────────────────
    def show_battle_screen(self):
        self.clear()
        self.root.geometry("760x580")
        s = self.state
        p, e = s.player, s.enemy

        bg = "#0a0a1e"

        # Title
        tk.Label(self.root, text="⚔️  ROBOT RUMBLE  ⚔️", font=("Courier", 18, "bold"),
                 fg="#FFD700", bg=bg).pack(pady=(12, 4))

        # ── HP BARS ───────────────────────────────────────────────────────────────
        hp_frame = tk.Frame(self.root, bg=bg)
        hp_frame.pack(fill="x", padx=24, pady=4)

        # Player HP
        self.player_side = tk.Frame(hp_frame, bg=bg)
        self.player_side.pack(side="left", fill="x", expand=True)
        tk.Label(self.player_side, text=f"YOU — {p['emoji']} {p['name']}", font=("Courier", 10, "bold"),
                 fg=p["color"], bg=bg, anchor="w").pack(anchor="w")
        self.p_hp_label = tk.Label(self.player_side, text=f"HP: {s.player_hp}/{p['hp']}",
                                    font=("Courier", 8), fg="#888", bg=bg, anchor="w")
        self.p_hp_label.pack(anchor="w")
        self.p_bar_bg = tk.Frame(self.player_side, bg="#111", height=14)
        self.p_bar_bg.pack(fill="x", pady=2)
        self.p_bar = tk.Frame(self.p_bar_bg, bg="#00e676", height=14)
        self.p_bar.place(x=0, y=0, relwidth=1.0)
        self.p_status = tk.Label(self.player_side, text="", font=("Courier", 8),
                                  fg="#FF4500", bg=bg)
        self.p_status.pack(anchor="w")

        tk.Label(hp_frame, text="VS", font=("Courier", 16, "bold"),
                 fg="#333", bg=bg).pack(side="left", padx=16)

        # Enemy HP
        self.enemy_side = tk.Frame(hp_frame, bg=bg)
        self.enemy_side.pack(side="left", fill="x", expand=True)
        tk.Label(self.enemy_side, text=f"ENEMY — {e['emoji']} {e['name']}", font=("Courier", 10, "bold"),
                 fg=e["color"], bg=bg, anchor="w").pack(anchor="w")
        self.e_hp_label = tk.Label(self.enemy_side, text=f"HP: {s.enemy_hp}/{e['hp']}",
                                    font=("Courier", 8), fg="#888", bg=bg, anchor="w")
        self.e_hp_label.pack(anchor="w")
        self.e_bar_bg = tk.Frame(self.enemy_side, bg="#111", height=14)
        self.e_bar_bg.pack(fill="x", pady=2)
        self.e_bar = tk.Frame(self.e_bar_bg, bg="#FF5252", height=14)
        self.e_bar.place(x=0, y=0, relwidth=1.0)
        self.e_status = tk.Label(self.enemy_side, text="", font=("Courier", 8),
                                  fg="#FF4500", bg=bg)
        self.e_status.pack(anchor="w")

        # ── BIG ROBOT DISPLAY ────────────────────────────────────────────────────
        arena_frame = tk.Frame(self.root, bg="#080818", bd=0,
                               highlightthickness=1, highlightbackground="#1a1a3e")
        arena_frame.pack(fill="x", padx=24, pady=6)

        self.arena_canvas = tk.Canvas(arena_frame, bg="#080818", height=130,
                                       highlightthickness=0)
        self.arena_canvas.pack(fill="x")
        self.arena_canvas.bind("<Configure>", self.draw_arena)

        # ── BATTLE LOG ───────────────────────────────────────────────────────────
        log_frame = tk.Frame(self.root, bg=bg)
        log_frame.pack(fill="both", expand=True, padx=24, pady=(0, 4))

        self.log_text = tk.Text(log_frame, height=7, bg="#050510", fg="#888",
                                font=("Courier", 9), bd=0, relief="flat",
                                state="disabled", wrap="word",
                                highlightthickness=1, highlightbackground="#1a1a3e")
        self.log_text.pack(fill="both", expand=True)

        # Tags for colors
        for tag, color in [("gold","#FFD700"),("player", p["color"]),("enemy", e["color"]),
                            ("burn","#FF4500"),("freeze","#00BFFF"),("heal","#00e676"),
                            ("dmg","#FF6B6B"),("win","#FFD700"),("lose","#FF1744"),("gray","#555")]:
            self.log_text.tag_config(tag, foreground=color)

        # ── ACTION BUTTONS ────────────────────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg=bg)
        btn_frame.pack(pady=6)

        self.atk_btn = tk.Button(btn_frame, text="⚔️  ATTACK",
                                  font=("Courier", 11, "bold"), fg="#FF6B6B", bg="#1a0808",
                                  activeforeground="#fff", activebackground="#331010",
                                  bd=0, padx=20, pady=10, cursor="hand2",
                                  command=self.player_attack)
        self.atk_btn.pack(side="left", padx=8)

        self.spc_btn = tk.Button(btn_frame, text=f"✨  {p['special_name']}",
                                  font=("Courier", 11, "bold"), fg="#FF69B4", bg="#1a0818",
                                  activeforeground="#fff", activebackground="#330830",
                                  bd=0, padx=20, pady=10, cursor="hand2",
                                  command=self.player_special)
        self.spc_btn.pack(side="left", padx=8)

        self.turn_label = tk.Label(self.root, text="▶  YOUR TURN", font=("Courier", 9, "bold"),
                                    fg="#00e676", bg=bg)
        self.turn_label.pack(pady=(0, 6))

        self.add_log(f"⚔️  {p['name']} VS {e['name']} — FIGHT!", "gold")
        self.draw_arena()
        self.update_hud()

    def draw_arena(self, event=None):
        c = self.arena_canvas
        c.delete("all")
        w = c.winfo_width() or 700
        h = 130
        s = self.state

        # Background grid lines
        for x in range(0, w, 40):
            c.create_line(x, 0, x, h, fill="#0f0f20", width=1)
        for y in range(0, h, 30):
            c.create_line(0, y, w, y, fill="#0f0f20", width=1)

        # Player robot (left)
        px, py = w // 4, h // 2
        pc = s.player["color"]
        self.draw_robot(c, px, py, pc, s.player["name"], s.player["emoji"],
                        s.player["hp"], s.player["hp"], flip=False,
                        frozen=s.player_frozen, burn=s.player_burn > 0)

        # Enemy robot (right)
        ex, ey = (w * 3) // 4, h // 2
        ec = s.enemy["color"]
        self.draw_robot(c, ex, ey, ec, s.enemy["name"], s.enemy["emoji"],
                        s.enemy_hp, s.enemy["hp"], flip=True,
                        frozen=s.enemy_frozen, burn=s.enemy_burn > 0)

        # VS in center
        c.create_text(w // 2, h // 2, text="VS", fill="#1a1a3e",
                      font=("Courier", 20, "bold"))

    def draw_robot(self, c, x, y, color, name, emoji, hp, max_hp, flip, frozen, burn):
        # Body shape
        size = 28
        body_color = "#00BFFF" if frozen else color
        outline = "#fff" if not frozen else "#88EEFF"
        c.create_oval(x-size, y-size, x+size, y+size, fill=body_color,
                      outline=outline, width=2)

        # Eyes
        ex_off = -10 if not flip else 10
        c.create_oval(x+ex_off-7, y-10, x+ex_off+1, y-2, fill="white", outline="")
        c.create_oval(x+ex_off-5, y-8, x+ex_off-1, y-4, fill="#000", outline="")
        c.create_oval(x-ex_off+7, y-10, x-ex_off-1, y-2, fill="white", outline="")
        c.create_oval(x-ex_off+5, y-8, x-ex_off+1, y-4, fill="#000", outline="")

        # Mouth
        mouth_x = x + (6 if flip else -6)
        c.create_arc(mouth_x-8, y+4, mouth_x+8, y+16, start=0, extent=180,
                     style="arc", outline=color, width=2)

        # Antenna
        c.create_line(x, y-size, x, y-size-16, fill=color, width=2)
        c.create_oval(x-4, y-size-20, x+4, y-size-12, fill=color, outline="")

        # Burn effect
        if burn:
            c.create_text(x, y-size-28, text="🔥", font=("Segoe UI Emoji", 10))

        # Name below
        c.create_text(x, y+size+12, text=name, fill=color, font=("Courier", 8, "bold"))

    def add_log(self, msg, tag="gray"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"› {msg}\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def update_hud(self):
        s = self.state
        p, e = s.player, s.enemy

        # Player HP bar
        pct = max(0, s.player_hp / p["hp"])
        self.p_bar.place(relwidth=pct)
        p_color = "#00e676" if pct > 0.5 else "#FFD600" if pct > 0.25 else "#FF1744"
        self.p_bar.config(bg=p_color)
        self.p_hp_label.config(text=f"HP: {max(0, s.player_hp)} / {p['hp']}")

        p_stat = ""
        if s.player_burn > 0: p_stat += f"🔥 BURN×{s.player_burn}  "
        if s.player_frozen: p_stat += "🧊 FROZEN"
        self.p_status.config(text=p_stat)

        # Enemy HP bar
        epct = max(0, s.enemy_hp / e["hp"])
        self.e_bar.place(relwidth=epct)
        e_color = "#FF5252" if epct > 0.5 else "#FF9800" if epct > 0.25 else "#B71C1C"
        self.e_bar.config(bg=e_color)
        self.e_hp_label.config(text=f"HP: {max(0, s.enemy_hp)} / {e['hp']}")

        e_stat = ""
        if s.enemy_burn > 0: e_stat += f"🔥 BURN×{s.enemy_burn}  "
        if s.enemy_frozen: e_stat += "🧊 FROZEN"
        self.e_status.config(text=e_stat)

        self.draw_arena()

    def calc_dmg(self, attack, defense):
        raw = attack - defense * 0.3 + random.randint(-4, 4)
        return max(1, int(raw))

    def check_win(self):
        s = self.state
        if s.enemy_hp <= 0:
            self.add_log(f"🏆 {s.player['name']} WINS! You are victorious!", "win")
            self.end_game(True)
            return True
        if s.player_hp <= 0:
            self.add_log(f"💀 {s.enemy['name']} wins... You were defeated.", "lose")
            self.end_game(False)
            return True
        return False

    def end_game(self, player_won):
        self.state.game_over = True
        self.atk_btn.config(state="disabled")
        self.spc_btn.config(state="disabled")
        color = "#FFD700" if player_won else "#FF1744"
        text = "🏆 VICTORY!" if player_won else "💀 DEFEATED!"
        self.turn_label.config(text=text, fg=color, font=("Courier", 11, "bold"))

        replay_btn = tk.Button(self.root, text="▶  PLAY AGAIN",
                                font=("Courier", 10, "bold"), fg="#000", bg="#FFD700",
                                bd=0, padx=16, pady=8, cursor="hand2",
                                command=self.show_pick_screen)
        replay_btn.pack(pady=4)

    # ── PLAYER ACTIONS ────────────────────────────────────────────────────────────
    def player_attack(self):
        if self.state.game_over or not self.state.player_turn:
            return
        self.do_player_turn("attack")

    def player_special(self):
        if self.state.game_over or not self.state.player_turn or self.state.player_special_used:
            return
        self.do_player_turn("special")

    def do_player_turn(self, action):
        s = self.state
        s.player_turn = False
        self.atk_btn.config(state="disabled")
        self.spc_btn.config(state="disabled")
        self.turn_label.config(text="⏳ ENEMY THINKING...", fg="#555")

        # Apply player burn
        if s.player_burn > 0:
            s.player_hp = max(0, s.player_hp - 8)
            s.player_burn -= 1
            self.add_log(f"🔥 You take 8 burn damage! ({s.player_burn} ticks left)", "burn")
            self.update_hud()
            if self.check_win(): return

        # Check if frozen
        if s.player_frozen:
            self.add_log("🧊 You are FROZEN and skip your turn!", "freeze")
            s.player_frozen = False
            self.update_hud()
            self.root.after(1000, self.do_enemy_turn)
            return

        # Perform action
        if action == "attack":
            dmg = self.calc_dmg(s.player["attack"], s.enemy["defense"])
            s.enemy_hp = max(0, s.enemy_hp - dmg)
            self.add_log(f"{s.player['emoji']} You attack {s.enemy['name']} for {dmg} damage!", "player")
        elif action == "special":
            s.player_special_used = True
            self.spc_btn.config(state="disabled", text="✨ USED")
            res = s.player["special"](s.player["attack"])
            self.add_log(f"{s.player['emoji']} {s.player['name']} {res['msg']}", "player")
            if "dmg" in res:
                dmg = self.calc_dmg(res["dmg"], s.enemy["defense"])
                s.enemy_hp = max(0, s.enemy_hp - dmg)
                self.add_log(f"💥 {s.enemy['name']} takes {dmg} damage!", "dmg")
            if "heal" in res:
                s.player_hp = min(s.player["hp"], s.player_hp + res["heal"])
                self.add_log(f"💚 You heal to {s.player_hp} HP!", "heal")
            if "burn" in res:
                s.enemy_burn = res["burn"]
                self.add_log(f"🔥 {s.enemy['name']} is BURNING for {res['burn']} turns!", "burn")
            if "freeze" in res:
                s.enemy_frozen = True
                self.add_log(f"🧊 {s.enemy['name']} is FROZEN! They skip their turn!", "freeze")
            if "self_dmg" in res:
                s.player_hp = max(0, s.player_hp - res["self_dmg"])
                self.add_log(f"💀 You take {res['self_dmg']} self-damage from the explosion!", "dmg")

        self.update_hud()
        if self.check_win(): return
        self.root.after(1000, self.do_enemy_turn)

    def do_enemy_turn(self):
        s = self.state
        if s.game_over: return

        # Apply enemy burn
        if s.enemy_burn > 0:
            s.enemy_hp = max(0, s.enemy_hp - 8)
            s.enemy_burn -= 1
            self.add_log(f"🔥 {s.enemy['name']} takes 8 burn damage! ({s.enemy_burn} ticks left)", "burn")
            self.update_hud()
            if self.check_win(): return

        # Check if frozen
        if s.enemy_frozen:
            self.add_log(f"🧊 {s.enemy['name']} is FROZEN and skips their turn!", "freeze")
            s.enemy_frozen = False
            self.update_hud()
            self.enable_player_turn()
            return

        # Enemy AI: use special sometimes
        use_special = not s.enemy_special_used and (
            s.enemy_hp / s.enemy["hp"] < 0.4 or random.random() < 0.2
        )

        if use_special:
            s.enemy_special_used = True
            res = s.enemy["special"](s.enemy["attack"])
            self.add_log(f"{s.enemy['emoji']} {s.enemy['name']} {res['msg']}", "enemy")
            if "dmg" in res:
                dmg = self.calc_dmg(res["dmg"], s.player["defense"])
                s.player_hp = max(0, s.player_hp - dmg)
                self.add_log(f"💥 You take {dmg} damage!", "dmg")
            if "heal" in res:
                s.enemy_hp = min(s.enemy["hp"], s.enemy_hp + res["heal"])
                self.add_log(f"💚 {s.enemy['name']} heals to {s.enemy_hp} HP!", "heal")
            if "burn" in res:
                s.player_burn = res["burn"]
                self.add_log(f"🔥 You are BURNING for {res['burn']} turns!", "burn")
            if "freeze" in res:
                s.player_frozen = True
                self.add_log(f"🧊 You are FROZEN! Your next turn is skipped!", "freeze")
            if "self_dmg" in res:
                s.enemy_hp = max(0, s.enemy_hp - res["self_dmg"])
                self.add_log(f"💀 {s.enemy['name']} takes {res['self_dmg']} self-damage!", "dmg")
        else:
            dmg = self.calc_dmg(s.enemy["attack"], s.player["defense"])
            s.player_hp = max(0, s.player_hp - dmg)
            self.add_log(f"{s.enemy['emoji']} {s.enemy['name']} attacks you for {dmg} damage!", "enemy")

        self.update_hud()
        if self.check_win(): return
        self.enable_player_turn()

    def enable_player_turn(self):
        s = self.state
        s.player_turn = True
        self.atk_btn.config(state="normal")
        if not s.player_special_used:
            self.spc_btn.config(state="normal")
        self.turn_label.config(text="▶  YOUR TURN", fg="#00e676")


# ── RUN ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotRumble(root)
    root.mainloop()