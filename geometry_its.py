# geometry_its.py
from owlready2 import *
import tkinter as tk
from tkinter import ttk, messagebox

# === Load Ontology ===
onto_path.append(".")  # Look in current directory
onto = get_ontology("GeometryITS.rdf").load()

# Map shape names to ontology classes
SHAPE_CLASSES = {
    "Square": onto.Square,
    "Rectangle": onto.Rectangle,
    "Triangle": onto.Triangle,
    "Circle": onto.Circle
}

# === Compute Functions ===
def compute_area(shape, values):
    try:
        if shape == "Square":
            side = float(values["side"])
            return side * side
        elif shape == "Rectangle":
            length = float(values["length"])
            width = float(values["width"])
            return length * width
        elif shape == "Triangle":
            base = float(values["base"])
            height = float(values["height"])
            return 0.5 * base * height
        elif shape == "Circle":
            radius = float(values["radius"])
            return 3.14 * radius * radius
    except (ValueError, KeyError):
        return None

def compute_perimeter(shape, values):
    try:
        if shape == "Square":
            side = float(values["side"])
            return 4 * side
        elif shape == "Rectangle":
            length = float(values["length"])
            width = float(values["width"])
            return 2 * (length + width)
        elif shape == "Triangle":
            s1 = float(values["side1"])
            s2 = float(values["side2"])
            s3 = float(values["side3"])
            return s1 + s2 + s3
        elif shape == "Circle":
            radius = float(values["radius"])
            return 2 * 3.14 * radius
    except (ValueError, KeyError):
        return None

# === GUI Application ===
class GeometryITSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry Intelligent Tutoring System")
        self.root.geometry("650x550")
        
        # Shape selection
        ttk.Label(root, text="Select Shape:", font=("Arial", 12, "bold")).pack(pady=10)
        self.shape_var = tk.StringVar()
        shape_combo = ttk.Combobox(root, textvariable=self.shape_var, values=list(SHAPE_CLASSES.keys()), state="readonly", width=20)
        shape_combo.pack(pady=5)
        shape_combo.bind("<<ComboboxSelected>>", self.on_shape_select)
        
        # Input frame
        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(pady=10)
        
        # Buttons
        self.calc_button = ttk.Button(root, text="Calculate", command=self.calculate, style="Accent.TButton")
        self.calc_button.pack(pady=10)
        self.calc_button.config(state="disabled")
        
        # Results
        self.result_text = tk.Text(root, height=12, width=80, wrap=tk.WORD, font=("Arial", 10))
        self.result_text.pack(pady=10, padx=20)

    def on_shape_select(self, event=None):
        # Clear previous inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        shape = self.shape_var.get()
        self.entries = {}
        
        if shape == "Square":
            ttk.Label(self.input_frame, text="Side length:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.input_frame, width=15)
            entry.grid(row=0, column=1, padx=5, pady=5)
            self.entries["side"] = entry
            
        elif shape == "Rectangle":
            ttk.Label(self.input_frame, text="Length:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            len_entry = ttk.Entry(self.input_frame, width=15)
            len_entry.grid(row=0, column=1, padx=5, pady=5)
            self.entries["length"] = len_entry
            
            ttk.Label(self.input_frame, text="Width:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            wid_entry = ttk.Entry(self.input_frame, width=15)
            wid_entry.grid(row=1, column=1, padx=5, pady=5)
            self.entries["width"] = wid_entry
            
        elif shape == "Triangle":
            ttk.Label(self.input_frame, text="Base:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            base_entry = ttk.Entry(self.input_frame, width=15)
            base_entry.grid(row=0, column=1, padx=5, pady=5)
            self.entries["base"] = base_entry
            
            ttk.Label(self.input_frame, text="Height:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            h_entry = ttk.Entry(self.input_frame, width=15)
            h_entry.grid(row=1, column=1, padx=5, pady=5)
            self.entries["height"] = h_entry
            
            ttk.Label(self.input_frame, text="Side 1:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            s1 = ttk.Entry(self.input_frame, width=15)
            s1.grid(row=2, column=1, padx=5, pady=5)
            self.entries["side1"] = s1
            
            ttk.Label(self.input_frame, text="Side 2:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
            s2 = ttk.Entry(self.input_frame, width=15)
            s2.grid(row=3, column=1, padx=5, pady=5)
            self.entries["side2"] = s2
            
            ttk.Label(self.input_frame, text="Side 3:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
            s3 = ttk.Entry(self.input_frame, width=15)
            s3.grid(row=4, column=1, padx=5, pady=5)
            self.entries["side3"] = s3
            
        elif shape == "Circle":
            ttk.Label(self.input_frame, text="Radius:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            rad_entry = ttk.Entry(self.input_frame, width=15)
            rad_entry.grid(row=0, column=1, padx=5, pady=5)
            self.entries["radius"] = rad_entry
        
        self.calc_button.config(state="normal")

    def generate_hint(self, shape, values):
        """Generate rule-based hints based on student inputs."""
        hints = []

        # Rule 1: Non-positive values
        for key, val in values.items():
            if val <= 0:
                hints.append(f"{key.replace('_', ' ').title()} must be greater than zero.")

        # Rule 2: Shape-specific logic
        if shape == "Square":
            if "radius" in values:
                hints.append("Squares don't use radius! Use side length instead.")
            side = values.get("side", 0)
            if side > 100:
                hints.append("That's a very large square! Double-check your side length.")

        elif shape == "Circle":
            if "side" in values or "length" in values or "width" in values:
                hints.append("Circles use only radius — not side, length, or width.")
            radius = values.get("radius", 0)
            if radius > 50:
                hints.append("Large radius? Make sure you’re not confusing it with diameter.")

        elif shape == "Rectangle":
            length = values.get("length", 0)
            width = values.get("width", 0)
            if length == width and length > 0:
                hints.append("Length equals width — this is actually a square! Rectangles have different length and width.")

        elif shape == "Triangle":
            if "radius" in values:
                hints.append("Triangles don't use radius. Use base and height for area.")
            s1, s2, s3 = values.get("side1", 0), values.get("side2", 0), values.get("side3", 0)
            if s1 + s2 <= s3 or s2 + s3 <= s1 or s1 + s3 <= s2:
                hints.append("Invalid triangle! The sum of any two sides must be greater than the third side.")

        return hints[0] if hints else None

    def calculate(self):
        shape = self.shape_var.get()
        if not shape:
            messagebox.showerror("Error", "Please select a shape!")
            return

        # Parse inputs
        values = {}
        for key, entry in self.entries.items():
            val_str = entry.get().strip()
            if not val_str:
                messagebox.showerror("Error", f"Please enter a value for {key.replace('_', ' ').title()}!")
                return
            try:
                values[key] = float(val_str)
            except ValueError:
                messagebox.showerror("Error", f"Invalid number for {key.replace('_', ' ').title()}!")
                return

        # Rule-based hint
        hint = self.generate_hint(shape, values)

        # Compute area and perimeter
        area = compute_area(shape, values)
        perimeter = compute_perimeter(shape, values)
        
        if area is None or perimeter is None:
            messagebox.showerror("Error", "Calculation failed. Please check your inputs.")
            return

        # Retrieve formulas from ontology
        cls = SHAPE_CLASSES[shape]
        area_formula = cls.areaFormulaText[0] if getattr(cls, 'areaFormulaText', None) else "Formula not available"
        perim_formula = cls.perimeterFormulaText[0] if getattr(cls, 'perimeterFormulaText', None) else "Formula not available"

        # Build result message
        result = f"✅ Shape: {shape}\n\n"
        result += f"📐 Area Formula: {area_formula}\n"
        result += f"= {area:.2f}\n\n"
        result += f"📏 Perimeter Formula: {perim_formula}\n"
        result += f"= {perimeter:.2f}\n\n"

        if hint:
            result += f"💡 Hint: {hint}\n\n"
        else:
            result += "🌟 Great job! Your inputs look correct.\n\n"

        result += "Keep practicing geometry — you're doing awesome!"

        # Display result
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

# === Run App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryITSApp(root)
    root.mainloop()