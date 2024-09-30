import time 
import threading
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from datetime import datetime
import os

# Caminho do WebDriver
webdriver_path = "C:/Users/rubens.farias/Desktop/edgedriver_win64/msedgedriver.exe"
linkedin_url = "https://www.linkedin.com/login"

# Função para login no LinkedIn
def linkedin_login(driver, username, password, console):
    console.insert(END, "Abrindo navegador...\n")
    console.see(END)  # Rola automaticamente para o final
    try:
        driver.get(linkedin_url)
        time.sleep(2)
        
        console.insert(END, "Realizando login...\n")
        console.see(END)  # Rola automaticamente para o final
        # Tentativa de login
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        console.insert(END, "Login realizado com sucesso!\n")
        console.see(END)  # Rola automaticamente para o final
    except Exception as e:
        console.insert(END, "Erro ao realizar login. Verifique suas credenciais.\n")
        console.see(END)  # Rola automaticamente para o final
        driver.quit()

# Função para enviar conexões
def send_connections(driver, status_label, console):
    count = 0
    try:
        while not stop_event.is_set():
            driver.get("https://www.linkedin.com/mynetwork/")
            time.sleep(2)

            # Localiza e clica nos botões de conectar
            connect_buttons = driver.find_elements(By.XPATH, "//span[text()='Conectar']/..")
            for button in connect_buttons:
                if stop_event.is_set():
                    break
                try:
                    button.click()
                    time.sleep(2)
                    count += 1
                    status_label.config(text=f"{count} conexões enviadas")
                    console.insert(END, f"Conexão enviada com sucesso para: {count}\n")
                    console.see(END)  # Rola automaticamente para o final
                except Exception as e:
                    continue  # Pula a tentativa com erro e vai para a próxima

            # Role a página para carregar mais conexões
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3)

    except Exception as e:
        console.insert(END, "Erro inesperado ao enviar conexões.\n")
        console.see(END)  # Rola automaticamente para o final
    finally:
        driver.quit()
        console.insert(END, "Navegador fechado.\n")
        console.see(END)  # Rola automaticamente para o final

        # Salva relatório com a contagem de conexões
        today = datetime.now().strftime("%Y-%m-%d")
        base_path = os.path.join(os.path.expanduser("~"), "Desktop", "LinkedIn_Connections")
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        base_filename = "connections_report"
        extension = ".txt"
        counter = 1
        while os.path.exists(f"{base_path}/{base_filename}({counter}){extension}"):
            counter += 1
        file_path = f"{base_path}/{base_filename}({counter}){extension}"
        with open(file_path, "w") as file:
            file.write(f"Foram enviadas {count} conexões na data {today}\n")

# Função para iniciar o script
def start_script(status_label, console, start_button):
    global stop_event
    stop_event.clear()

    # Configurações do WebDriver
    options = Options()
    driver = webdriver.Edge(service=Service(webdriver_path), options=options)
    
    username = "icsrubensfarias@gmail.com"  # Considere usar variáveis de ambiente
    password = "f;jU_A9&9J8."  # Considere usar variáveis de ambiente
    
    # Tenta realizar o login no LinkedIn
    linkedin_login(driver, username, password, console)
    
    # Inicia thread para enviar as conexões
    threading.Thread(target=send_connections, args=(driver, status_label, console)).start()
    
    # Desabilita o botão de iniciar enquanto o script está em execução
    start_button.config(state=DISABLED)

# Função para parar o script
def stop_script(start_button):
    stop_event.set()
    start_button.config(state=NORMAL)

# Função para criar a interface
def create_interface():
    root = Tk()
    root.title("LinkedIn BOT")
    root.geometry("400x300")  # Resolução mais compacta
    root.configure(bg="#2e3436")  # Cinza escuro típico de terminais

    # Estilo dos botões (cilíndricos e interativos)
    button_style = {
        "bg": "#ff9900",  # Laranja Ubuntu
        "fg": "white",    # Texto branco
        "font": ("Courier", 10, "bold"),
        "bd": 0,
        "width": 10,
        "height": 1,
        "relief": "flat",
        "activebackground": "#cc7a00",
        "highlightthickness": 0,
        "cursor": "hand2"
    }

    # Frame para o console
    console_frame = Frame(root, bg="#2e3436")
    console_frame.pack(pady=10)

    # Estilo e configuração para o console (com barra de rolagem)
    console = Text(console_frame, height=6, width=50, font=("Courier", 9), bg="#1c1c1c", fg="#ff9900", bd=1, relief=SOLID)
    console.pack(pady=5)

    # Label de status
    status_label = Label(root, text="Conexões: 0", bg="#2e3436", fg="#ff9900", font=("Courier", 10, "bold"))
    status_label.pack(pady=10)

    # Frame para os botões
    button_frame = Frame(root, bg="#2e3436")
    button_frame.pack(side=BOTTOM, pady=10)

    start_button = Button(button_frame, text="Iniciar", command=lambda: start_script(status_label, console, start_button), **button_style)
    start_button.pack(side=LEFT, padx=5)

    stop_button = Button(button_frame, text="Parar", command=lambda: stop_script(start_button), bg="#dc322f", fg="white", font=("Courier", 10, "bold"), bd=0, width=10, relief=FLAT, height=1, activebackground="#b71c1c")
    stop_button.pack(side=LEFT, padx=5)

    root.mainloop()

stop_event = threading.Event()

if __name__ == "__main__":
    create_interface()
