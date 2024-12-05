import tkinter as tk
from tkinter import messagebox, ttk
from sympy import sympify, symbols, lambdify

def parse_function(func_input):
    try:
        
        func_input = func_input.replace("^", "**")
        
        x = symbols('x')
        func_expr = sympify(func_input)  
        func = lambdify(x, func_expr, "numpy")  
        return func
    except Exception as e:
        return None

def bisection(func, a, b, tol=1e-7, max_iter=100):
    results = []
    iteration = 0
    prev_c = None  

    if func(a) == 0:
        return results, a
    if func(b) == 0:
        return results, b

    if func(a) * func(b) > 0:
        raise ValueError("El intervalo inicial no cumple con f(a)*f(b) < 0.")

    while iteration < max_iter:
        c = (a + b) / 2
        f_a = func(a)
        f_b = func(b)
        f_c = func(c)

        error = None if prev_c is None else abs((c - prev_c) / c) * 100
        results.append([iteration + 1, a, b, c, f_a, f_b, f_c, f_a * f_c, error])

        if abs(f_c) < tol:
            break

        if error is not None and error < tol:
            break

        if f_a * f_c < 0:
            b = c
        else:
            a = c

        prev_c = c 
        iteration += 1

    return results, c

def false_position(func, a, b, tol=1e-7, max_iter=100):
    results = []
    prev_xr = None  
    f_a = func(a)
    f_b = func(b)

    if f_a * f_b >= 0:
        raise ValueError("El intervalo inicial no cumple con f(a)*f(b) < 0.")

    for iteration in range(1, max_iter + 1):
        xr = b - (f_b * (b - a) / (f_b - f_a ))
        f_xr = func(xr)

        error = abs((xr - prev_xr) / xr) * 100 if prev_xr is not None else None

        results.append([iteration, a, b, xr, f_a, f_b, f_xr, f_a * f_xr, error])

        if abs(f_xr) < tol or (error is not None and error < tol):
            return results, xr

        if f_a * f_xr < 0:
            b = xr
            f_b = f_xr
            f_a /= 2  
        else:
            a = xr
            f_a = f_xr
            f_b /= 2  

        prev_xr = xr  

    return results, xr


def show_results(results):
    window = tk.Toplevel()
    window.title("Resultados")
    window.geometry("900x500+300+150")  
    window.config(bg="darkslategray") 

    text_box = tk.Text(window, width=90, height=20, wrap=tk.WORD, font=("Courier", 10))
    text_box.pack(pady=10)

    text_box.insert(tk.END, "Iteración | x1 | x2 | xr | f(x1) | f(x2) | f(xr) | f(x1)*f(xr) | Error\n")
    text_box.insert(tk.END, "-"*100 + "\n")

    for result in results:
        result_line = " | ".join([f"{val:.5f}" if isinstance(val, float) else str(val) for val in result]) + "\n"
        text_box.insert(tk.END, result_line)

    text_box.config(state=tk.DISABLED)  

    window.mainloop()

def show_answer_window(root, answer, results):
    window = tk.Toplevel(root)
    window.title("Resultado de la raíz")
    window.geometry("400x200+500+250") 
    window.config(bg="lightseagreen")  

    result_label = tk.Label(window, text=f"Raíz obtenida: {answer}", font=("Helvetica", 14), fg="white", bg="lightseagreen")
    result_label.pack(pady=20)

    tk.Button(window, text="Mostrar tabla", command=lambda: show_results(results), bg="lightblue", fg="black").pack(pady=5)
    tk.Button(window, text="Regresar", command=window.destroy, bg="lightcoral", fg="black").pack(pady=5)

    window.mainloop()

def calculate():
    func_input = entry_func.get()
    func = parse_function(func_input)

    if func is None:
        messagebox.showerror("Error", "La función no es válida.")
        return

    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
    except ValueError:
        messagebox.showerror("Error", "Los valores de a y b deben ser numéricos.")
        return

    try:
        if method_var.get() == "Bisección":
            results, answer = bisection(func, a, b)
        elif method_var.get() == "Falsa Posición":
            results, answer = false_position(func, a, b)
        else:
            messagebox.showerror("Error", "Seleccione un método válido.")
            return
        show_answer_window(window, answer, results)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def show_main_window():
    global window
    window = tk.Tk()
    window.title("Calculadora de Ecuaciones")

    window.geometry("800x500+300+150") 
    window.config(bg="darkslategray")  

    tk.Label(window, text="Ingrese la función f(x): (Ejemplo: x^3 + x^2 - 4)", bg="darkslategray", fg="white").pack(pady=10)
    global entry_func
    entry_func = tk.Entry(window, width=40)
    entry_func.pack(pady=5)

    tk.Label(window, text="Valor de a:", bg="darkslategray", fg="white").pack(pady=5)
    global entry_a
    entry_a = tk.Entry(window)
    entry_a.pack(pady=5)

    tk.Label(window, text="Valor de b:", bg="darkslategray", fg="white").pack(pady=5)
    global entry_b
    entry_b = tk.Entry(window)
    entry_b.pack(pady=5)

    tk.Label(window, text="Seleccionar método:", bg="darkslategray", fg="white").pack(pady=10)
    global method_var
    method_var = tk.StringVar(value="Bisección")
    
    tk.Radiobutton(window, text="Método Bisección", variable=method_var, value="Bisección", bg="darkseagreen", fg="black").pack(pady=5)
    tk.Radiobutton(window, text="Método Falsa Posición", variable=method_var, value="Falsa Posición", bg="darkorange", fg="black").pack(pady=5)

    tk.Button(window, text="Calcular", command=calculate, bg="lightgreen", fg="black").pack(pady=20)
    window.mainloop()

show_main_window()



# Presentado por:
# Albert Samuel Fuel Rodriguez
# Juan Martin Romo 
# Jean Carlos Romero
