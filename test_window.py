import customtkinter as ctk

# Force the app to open and be visible
ctk.set_appearance_mode("dark") 

app = ctk.CTk()
app.geometry("400x200")
app.title("Visibility Test")

# High-contrast label
label = ctk.CTkLabel(
    app, 
    text="TOTAL: $7.00", 
    font=("Arial", 40, "bold"),
    text_color="yellow" 
)
label.pack(expand=True)

app.mainloop()