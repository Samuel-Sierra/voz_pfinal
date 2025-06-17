import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

def seleccionar_audio():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de audio",
        filetypes=[("Archivos de audio", "*.wav *.mp3 *.ogg *.flac")]
    )
    if archivo:
        label_audio.config(text=f"Audio seleccionado:\n{archivo}")
        mostrar_imagen()

def mostrar_imagen():
    try:
        imagen = Image.open("imagen.jpg")  # Usa tu propia imagen aquí
        imagen = imagen.resize((300, 300))  # Redimensionar si es necesario
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen.config(image=imagen_tk)
        label_imagen.image = imagen_tk  # Mantener referencia
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Fonemas")
ventana.geometry("400x500")
# Texto debajo del título
label_descripcion = tk.Label(
    ventana,
    text="Programa hecho para identificar fonemas",
    font=("Arial", 10),
    fg="gray"
)
label_descripcion.pack(pady=10)

# Botón para cargar audio
btn_cargar_audio = tk.Button(ventana, text="Seleccionar Audio", command=seleccionar_audio)
btn_cargar_audio.pack(pady=20)

# Etiqueta para mostrar el nombre del archivo
label_audio = tk.Label(ventana, text="No se ha seleccionado ningún audio")
label_audio.pack(pady=10)

# Imagen fija
label_imagen = tk.Label(ventana)
label_imagen.pack(pady=10)

# Iniciar la aplicación
ventana.mainloop()
