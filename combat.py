import tkinter as tk  # Importe le module tkinter pour l'interface graphique
import random         # Importe le module random pour générer des nombres aléatoires

class CombatGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Combat Simple")

        self.player_hp = 100
        self.enemy_hp = 100

        self.info = tk.Label(root, text="Bienvenue dans le jeu de combat !")
        self.info.pack()

        self.status = tk.Label(root, text=self.get_status())
        self.status.pack()

        # Ajout d'un canvas pour dessiner le bonhomme
        self.canvas = tk.Canvas(root, width=200, height=200, bg="white")
        self.canvas.pack(pady=10)
        self.bonhomme = self.draw_bonhomme(50, 150)  # Position initiale

        self.attack_btn = tk.Button(root, text="Attaquer", command=self.attack)
        self.attack_btn.pack(pady=5)

        self.heal_btn = tk.Button(root, text="Soigner", command=self.heal)
        self.heal_btn.pack(pady=5)

        self.quit_btn = tk.Button(root, text="Quitter", command=root.quit)
        self.quit_btn.pack(pady=5)

        # Lance l'animation
        self.direction = 1
        self.animate_bonhomme()

    def get_status(self):
        # Retourne une chaîne affichant les PV du joueur et de l'ennemi
        return f"Votre vie: {self.player_hp} | Vie de l'ennemi: {self.enemy_hp}"

    def attack(self):
        # Fonction appelée quand le joueur attaque
        if self.player_hp <= 0 or self.enemy_hp <= 0:
            return  # Si la partie est finie, ne rien faire
        dmg = random.randint(10, 20)  # Dégâts infligés à l'ennemi
        self.enemy_hp -= dmg
        msg = f"Vous attaquez et infligez {dmg} dégâts !\n"
        if self.enemy_hp <= 0:
            self.enemy_hp = 0
            msg += "Vous avez gagné !"  # Victoire du joueur
            self.end_game(msg)
            return
        self.enemy_turn(msg)  # L'ennemi joue ensuite

    def heal(self):
        # Fonction appelée quand le joueur se soigne
        if self.player_hp <= 0 or self.enemy_hp <= 0:
            return  # Si la partie est finie, ne rien faire
        heal = random.randint(10, 15)  # Points de vie récupérés
        self.player_hp += heal
        if self.player_hp > 100:
            self.player_hp = 100  # Limite les PV à 100
        msg = f"Vous vous soignez de {heal} points de vie.\n"
        self.enemy_turn(msg)  # L'ennemi joue ensuite

    def enemy_turn(self, msg):
        # Tour de l'ennemi (attaque le joueur)
        dmg = random.randint(8, 18)  # Dégâts infligés au joueur
        self.player_hp -= dmg
        msg += f"L'ennemi attaque et inflige {dmg} dégâts !"
        if self.player_hp <= 0:
            self.player_hp = 0
            msg += "\nVous avez perdu !"  # Défaite du joueur
            self.end_game(msg)
        self.status.config(text=self.get_status())  # Met à jour l'affichage des PV
        self.info.config(text=msg)                 # Met à jour le message d'info

    def end_game(self, msg):
        # Fonction appelée à la fin de la partie
        self.status.config(text=self.get_status())
        self.info.config(text=msg)
        self.attack_btn.config(state=tk.DISABLED)  # Désactive le bouton Attaquer
        self.heal_btn.config(state=tk.DISABLED)    # Désactive le bouton Soigner

    def draw_bonhomme(self, x, y):
        # Dessine un bonhomme bâton à la position (x, y)
        head = self.canvas.create_oval(x-10, y-40, x+10, y-20, fill="black")
        body = self.canvas.create_line(x, y-20, x, y+20, width=2)
        left_arm = self.canvas.create_line(x, y, x-20, y-10, width=2)
        right_arm = self.canvas.create_line(x, y, x+20, y-10, width=2)
        left_leg = self.canvas.create_line(x, y+20, x-15, y+40, width=2)
        right_leg = self.canvas.create_line(x, y+20, x+15, y+40, width=2)
        return [head, body, left_arm, right_arm, left_leg, right_leg]

    def animate_bonhomme(self):
        # Fait bouger le bonhomme de gauche à droite
        for part in self.bonhomme:
            self.canvas.move(part, self.direction, 0)
        pos = self.canvas.coords(self.bonhomme[0])
        if pos[0] <= 10 or pos[2] >= 190:
            self.direction *= -1
        self.root.after(30, self.animate_bonhomme)

if __name__ == "__main__":
    root = tk.Tk()              # Crée la fenêtre principale
    game = CombatGame(root)     # Instancie le jeu
    root.mainloop()             # Lance la boucle principale de l'interface

