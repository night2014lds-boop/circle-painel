# Circle-painel 🛰️

A circular, rotating application launcher styled like a revolver cylinder, designed for extreme desktop customization on Linux (XFCE and other desktop environments).

---

## 👤 Creator and Copyright

This project was envisioned, designed, and developed entirely by **night2014lds-boop** (GitHub: [night26](https://github.com)).

### ⚠️ 
1. **When you modify the files to fix**
2.  them or sell them claiming they are yours—don't do that; simply include the creator's name at the beginning or end of the code.

---

## 🕹️ How Does the Panel Work?

The **Revolver Panel** creates a perfectly circular, semi-transparent window positioned on the right edge of your screen, simulating a revolver cylinder loaded with applications.

1. **Spin the Cylinder:** Hover your mouse over the dark circle and use the **scroll wheel** to rotate the applications in a circular orbit.
2. **Open Apps:** Left-click on any application. The system will execute the program in the background and automatically slide the panel away.
3. **Smart Hiding:** When enabled via the menu, the panel smoothly slides out of the screen. To bring it back, simply touch the mouse pointer against the far-right edge of the screen.
4. **Manual Retract:** If the panel is open and you decide not to launch any app, simply **left-click on the dark area of the circle** and it will slide back into hiding.

---

## 📥 What to Do After Downloading (Automatic Installation)

You do not need to install dependencies manually. Open your terminal, copy the command below, paste it, and press **Enter**. The installer will download the project, set up the system libraries (Python 3, GTK 3, and Cairo), and configure the app to launch automatically when your computer starts:

```bash
curl -sSL https://githubusercontent.com | bash raw
```

---

## 🛠️ How to Modify and Customize the Panel

Since you have full access to the source code, any user can change how the "revolver" works by editing the main file. In your terminal, open the file using:
```bash
nano ~/.config/revolver-panel/main.py
```

### 1. Default Pre-Configured Applications
By default, the panel loads with universal Linux applications that exist on almost every XFCE system:

```python
        self.apps = [
            ("Apps Finder", "xfce4-appfinder", "edit-find"),
            ("Terminal", "xfce4-terminal", "utilities-terminal"),
            ("Web Browser", "x-www-browser", "browser"),
            ("Files", "thunar", "system-file-manager"),
            ("Settings", "xfce4-settings-manager", "preferences-system"),
            ("Text Editor", "mousepad", "text-editor")
        ]
```
Users can easily open this file and swap these commands to match their personal favorite programs or games.

### 2. How to Change the Circle Size or Spin Speed
Inside `main.py`, you can alter the numbers to tweak the physics to your liking:
- **Window Size:** Find `self.resize(400, 400)` and change the values if you want a larger or smaller circle.
- **Rotation Radius:** Change `self.raio = 140` to push the buttons further away or closer to the center of the circle.
- **Scroll Sensitivity:** In the `ao_girar_mouse` function, adjust the `0.25` values to increase or decrease how fast the cylinder rotates with each tick of the mouse scroll wheel.
