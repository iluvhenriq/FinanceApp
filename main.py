from core.database import criar_tabelas
from interface.app import App

def main():
    criar_tabelas()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
        
