from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3


class Harina():


    def __init__(self,window):

        self.wind = window
        self.wind.title('Novedades')
        self.wind.geometry('+400+300')


        # Creacion de las barra menu
        self.barra_menu = Menu(self.wind)
        self.wind.config(menu=self.barra_menu, width=300, height=300)

        self.borrar_menu = Menu(self.barra_menu, tearoff=0)
        self.borrar_menu.add_command(label='Borrar campos', command=self.limpiar_campos)

        self.crud_menu = Menu(self.barra_menu, tearoff=0)
        self.crud_menu.add_command(label='Insertar', command = self.insertar)
        self.crud_menu.add_command(label='Consultar', command = self.consultar)
        self.crud_menu.add_command(label='Actualizar', command = self.acualizar)
        self.crud_menu.add_command(label='Borrar', command = self.eliminar)

        self.ayuda_menu = Menu(self.barra_menu, tearoff=0)
        self.ayuda_menu.add_command(label='Licencia')
        self.ayuda_menu.add_command(label='Acerca de...')

        self.barra_menu.add_cascade(label='Borrar', menu=self.borrar_menu)
        self.barra_menu.add_cascade(label='CRUD', menu=self.crud_menu)
        self.barra_menu.add_cascade(label='Ayuda', menu=self.ayuda_menu)

        # Comienzan los campos
        self.mi_frame = Frame(self.wind)
        self.mi_frame.pack()

        self.mi_falla = StringVar()

        self.cuadro_falla = Entry(self.mi_frame, width=50, textvariable=self.mi_falla)
        self.cuadro_falla.grid(row=0, column=1, padx=10, pady=10)

        self.texto_comentario = Text(self.mi_frame, width=58, height=15)
        self.texto_comentario.grid(row=1, column=1, padx=10, pady=10)
        scrollVert = Scrollbar(self.mi_frame, command=self.texto_comentario.yview)
        scrollVert.grid(row=1, column=2, sticky='nsew')

        self.texto_comentario.config(yscrollcommand=scrollVert.set)

        # Comienzan los label

        self.falla_label = Label(self.mi_frame, text='Sintoma:')
        self.falla_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)

        self.comentario_label = Label(self.mi_frame, text='Comentarios:')
        self.comentario_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)

        # Boton
        self.btn_consultar = Button(self.mi_frame, text='Consultar', command = self.consultar)
        self.btn_consultar.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky='ew')


    def limpiar_campos(self):
        self.mi_falla.set('')
        self.texto_comentario.delete(1.0, END)


    def insertar(self):
        mi_conexion = sqlite3.connect('noverdades.db')

        mi_cursor = mi_conexion.cursor()

        datos = self.mi_falla.get(), self.texto_comentario.get('1.0', END)

        mi_cursor.execute('INSERT INTO novedades VALUES(NULL,?,?)', datos)

        mi_conexion.commit()

        messagebox.showinfo('BBDD', 'Registro insertado con exito')

    def consultar(self):
        mi_conexion = sqlite3.connect('noverdades.db')

        mi_cursor = mi_conexion.cursor()

        f = (self.mi_falla.get(),)

        mi_cursor.execute('SELECT * FROM novedades WHERE falla = ?', f)

        el_usuario = mi_cursor.fetchall()

        for usuario in el_usuario:
            self.mi_falla.set(usuario[1])
            self.texto_comentario.insert(1.0, usuario[2])

        mi_conexion.commit()


    def acualizar(self):
        mi_conexion = sqlite3.connect('noverdades.db')

        mi_cursor = mi_conexion.cursor()

        datos = (self.mi_falla.get(), self.texto_comentario.get('1.0', END), self.mi_falla.get() )

        mi_cursor.execute('UPDATE novedades SET falla = ?, comentario = ? WHERE falla = ?',  (datos))

        mi_conexion.commit()

        messagebox.showinfo('BBDD', 'Registro actualizado con exito')


    def eliminar(self):
        mi_conexion = sqlite3.connect('noverdades.db')

        mi_cursor = mi_conexion.cursor()

        f = (self.mi_falla.get(),)

        mi_cursor.execute('DELETE FROM novedades WHERE falla = ?', f)

        mi_conexion.commit()

        self.limpiar_campos()

        messagebox.showinfo('BBDD', 'Registro borrado con exito')


if __name__ == '__main__':
    window = Tk()
    app = Harina(window)
    window.mainloop()


