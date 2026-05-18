import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from core.database import calcular_saldo, buscar_transacoes_mes, resumo_por_categoria
from core.email_reader import processar_emails, EMAIL, SENHA

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Finance App")
        self.geometry("1200x800")
        self.sidebar = ctk.CTkFrame(self)
        self.sidebar.grid(row = 0, column = 0, sticky = "ns")
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row = 0, column = 1, sticky = "ns")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.build_sidebar()
        self.build_dashboard()
        self.build_charts()
        self.update_dashboard()
        self.build_extrato()
        self.importar_emails()
    def build_sidebar(self):
        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="DashBoard", command=self.show_dashboard)
        self.btn_dashboard.pack(pady=10, padx=10)
        self.btn_transacoes = ctk.CTkButton(self.sidebar, text="Transações", command=self.show_transacoes)
        self.btn_transacoes.pack(pady=10, padx=10)
        self.btn_relatorio = ctk.CTkButton(self.sidebar, text="Relatórios", command=self.show_relatorios)
        self.btn_relatorio.pack(pady=10, padx=10)
        self.btn_novatransacao = ctk.CTkButton(self.sidebar, text="Nova Transação", command=self.open_new_transaction, fg_color="#1a1a2e", hover_color="#131330")
        self.btn_novatransacao.pack(pady=10, padx=10, side="bottom")
        self.btn_atualizar = ctk.CTkButton(self.sidebar, text="Atualizar", command=self.importar_emails)
        self.btn_atualizar.pack(pady=10, padx=10)
        self.btn_busca_completa = ctk.CTkButton(
            self.sidebar, text="Busca Completa",
            command=self.importar_emails_completo
        )
        self.btn_busca_completa.pack(pady=10, padx=10)
    def build_dashboard(self):
        self.card_receitas = ctk.CTkFrame(self.main_frame, width=180, height= 80)
        self.card_receitas.grid(row= 0, column = 0, padx = 10, pady= 10)
        self.card_receitas.pack_propagate(False)
        self.lbl_receitas = ctk.CTkLabel(self.card_receitas, text="RECEITAS", font=("Arial", 15))
        self.lbl_receitas.pack(pady=5)
        self.lbl_valor_receitas = ctk.CTkLabel(self.card_receitas, text="R$ 0,00", font=("Arial", 22))
        self.lbl_valor_receitas.pack(pady=5)
        self.card_gastos = ctk.CTkFrame(self.main_frame, width=180, height=80)
        self.card_gastos.grid(row= 0,column= 1,padx = 10, pady = 10)
        self.card_gastos.pack_propagate(False)
        self.lbl_gastos = ctk.CTkLabel(self.card_gastos, text="GASTOS", font =("Arial", 15))
        self.lbl_gastos.pack(pady=5)
        self.lbl_valor_gastos = ctk.CTkLabel(self.card_gastos, text = "R$ 0,00", font=("Arial", 20))
        self.lbl_valor_gastos.pack(pady=5)
        self.card_maiorgasto = ctk.CTkFrame(self.main_frame, width=180, height=80)
        self.card_maiorgasto.grid(row = 0, column = 2, padx = 10, pady = 10)
        self.card_maiorgasto.pack_propagate(False)
        self.lbl_maiorgasto = ctk.CTkLabel(self.card_maiorgasto, text="MAIOR GASTO", font= ("Arial", 15))
        self.lbl_maiorgasto.pack(pady=5)
        self.lbl_valor_maiorgasto = ctk.CTkLabel(self.card_maiorgasto, text = "0,00", font=("Arial", 15))
        self.lbl_valor_maiorgasto.pack(pady=5)
    def update_dashboard(self):
        agora = datetime.now()
        mes = agora.month
        ano = agora.year

        saldo = calcular_saldo(mes, ano)
        transacoes = buscar_transacoes_mes(mes, ano)
        resumo= resumo_por_categoria(mes, ano)
        receitas = sum(t[2] for t in transacoes if t[5] == "receita")
        gastos = sum(t[2] for t in transacoes if t[5] == "gasto")

        self.lbl_valor_receitas.configure(text=f"R$ {receitas: .2f}")
        self.lbl_valor_gastos.configure(text=f"R$ {gastos: .2f}")
        if resumo: 
            maior = max(resumo, key=lambda x: x[1])
            self.lbl_valor_maiorgasto.configure(text=f"{maior[0]} - R$ {maior[1]:.2f}")
        else:
            self.lbl_valor_maiorgasto.configure(text="Nenhum gasto")
        self.build_charts()
        self.build_extrato()
    def open_new_transaction(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Nova Transação")
        janela.geometry("400x500")
        janela.grab_set()
        ctk.CTkLabel(janela, text="Descrição").pack(pady=5)
        entry_descricao = ctk.CTkEntry(janela, width=300)
        entry_descricao.pack(pady=5)
        ctk.CTkLabel(janela, text="Valor").pack(pady=5)
        entry_valor = ctk.CTkEntry(janela, width=300)
        entry_valor.pack(pady=5)
        ctk.CTkLabel(janela, text="Data (DD/MM/AAAA)").pack(pady=5)
        entry_data = ctk.CTkEntry(janela, width=300)
        entry_data.pack(pady=5)
        ctk.CTkLabel(janela, text="Tipo").pack(pady=5)
        option_tipo = ctk.CTkOptionMenu(janela, values=["gasto", "receita"], command=lambda tipo: option_categoria.configure(
            values=["Alimentação", "Saúde", "Outros"] if tipo == "gasto" else ["Salário", "Freela", "Outros"]
        ))
        option_tipo.pack(pady=5)
        ctk.CTkLabel(janela, text="Categoria").pack(pady=5)
        option_categoria = ctk.CTkOptionMenu(janela, values=["Alimentação", "Saúde", "Outros"])
        option_categoria.pack(pady=5)
        def formatar_data(event):
            texto = entry_data.get().replace("/", "")
            novo = ""
            for i, c in enumerate(texto[:8]):
                if   i == 2 or i == 4:
                    novo += "/"
                novo += c 
            entry_data.delete(0, "end") 
            entry_data.insert(0, novo)

        entry_data.bind("<KeyRelease>", formatar_data)
        def salvar():
            from core.database import salvar_transacao
            data_obj = datetime.strptime(entry_data.get(), "%d/%m/%Y")
            data = data_obj.strftime("%Y-%m-%d")
            valor = float(entry_valor.get().replace(",", "."))
            descricao = entry_descricao.get()
            categoria = option_categoria.get()
            tipo = option_tipo.get()
            salvar_transacao(data, valor, descricao, categoria, tipo)
            self.update_dashboard()
            janela.destroy()
        ctk.CTkButton(janela, text="Salvar", command=salvar).pack(pady=20)
    def build_charts(self):

        agora = datetime.now()
        resumo = resumo_por_categoria(agora.month, agora.year)

        categorias = [r[0] for r in resumo] if resumo else ["Sem dados"]
        valores = [r[1] for r in resumo] if resumo else [1]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
        fig.patch.set_facecolor("#1a1a1a")

        ax1.bar(categorias, valores, color=["#5DCaa5", "#378ADD", "#7F77DD"])
        ax1.set_facecolor("#1a1a1a")
        ax1.tick_params(colors="white")
        ax1.set_title("Por Categoria", color="white")

        ax2.pie(valores, labels=categorias, autopct="%1.1f%%", colors=["#5DCaa5", "#377ADD", "#7F77DD"])
        ax2.set_title("Proporção", color="white")

        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    def build_extrato(self):

        agora = datetime.now()
        transacoes = buscar_transacoes_mes(agora.month, agora.year)

        frame_extrato = ctk.CTkScrollableFrame(self.main_frame, width=600, height=200)
        frame_extrato.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        for t in transacoes:
            cor = "#5DCaa5" if t[5] == "receita" else "#E24B4A"
            texto = f"{t[1]} | {t[3]} | R$ {t[2]: .2f} | {t[4]}"
            ctk.CTkLabel(frame_extrato, text=texto, text_color=cor).pack(anchor="w", pady=2)
    def importar_emails(self):
        from core.database import salvar_transacao
        from core.categorizer import categorizar
        transacoes = processar_emails(EMAIL, SENHA)
        for t in transacoes:
            categoria = categorizar(t["descricao"])
            data_obj = datetime.strptime(t["data"], "%d/%m/%Y")
            data = data_obj.strftime("%Y-%m-%d")
            salvar_transacao(data, t["valor"], t["descricao"], categoria, "gasto")
        self.update_dashboard()
    def show_transacoes(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        from core.database import buscar_transacoes_mes

        ctk.CTkLabel(self.main_frame, text="Transações", font=("Arial", 20)).pack(pady=10)
        frame = ctk.CTkScrollableFrame(self.main_frame, width=800, height=600)
        frame.pack(padx=10, pady=0, fill="both", expand=True)
        
        agora = datetime.now()
        transacoes = buscar_transacoes_mes(agora.month, agora.year)

        for t in transacoes:
            cor = "#5DCaa5" if t[5] == "receita" else "#E24B4A"
            linha = ctk.CTkFrame(frame, fg_color="transparent")
            linha.pack(fill="x", pady=2, padx=10)
            texto = f"{t[1]} | {t[3]} | R$ {t[2]:.2f} | {t[4]} | {t[5]}"
            ctk.CTkLabel(linha, text=texto, text_color=cor).pack(side="left")
            ctk.CTkButton(linha, text="Deletar", width=70, fg_color="#e74c3c",
                            command=lambda id=t[0]: self.deletar(id)).pack(side="right")
    def show_dashboard(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.build_dashboard()
        self.build_charts()
        self.update_dashboard()
        self.build_extrato()
    
    def show_relatorios(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        agora = datetime.now()

        mes = agora.month
        ano = agora.year

        transacoes = buscar_transacoes_mes(mes, ano)
        resumo = resumo_por_categoria(mes, ano)

        receitas = sum(v for _, v in resumo if v > 0)
        gastos   = abs(sum(v for _, v in resumo if v < 0))
        saldo    = receitas - gastos

        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(10, 20), padx=10)

        for titulo, valor, cor in [
            ("💰 Receitas", f"R$ {receitas:,.2f}", "#2ecc71"),
            ("💸 Gasto", f"R$ {gastos:,.2f}",      "#e74c7c"),
            ("📊 Saldo", f"R$ {saldo:,.2f}",       "#3498db"),
            ("🧾 Transações", str(len(transacoes)),"#9b59b6"),

        ]: 
            card = ctk.CTkFrame(cards_frame, corner_radius=12)
            card.pack(side="left", expand=True, fill="x", padx=8)
            ctk.CTkLabel(card, text=titulo, font=("Arial", 12), text_color="gray").pack(pady=(14, 2))
            ctk.CTkLabel(card, text=valor, font=("Arial", 20, "bold"), text_color=cor).pack(pady=(0, 14))
        ctk.CTkLabel(self.main_frame, text="Por Categoria", font=("Arial", 15, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

        if resumo:
            for cat, total in sorted(resumo, key=lambda x: abs(x[1]), reverse=True):
                cor = "#2ecc71" if total >= 0 else "#e74c3c"
                texto = f"{cat} - R$ {total:,.2f}"
                ctk.CTkLabel(self.main_frame, text=texto, text_color=cor).pack(anchor="w", padx=20, pady=2)
        else:
            ctk.CTkLabel(self.main_frame, text="Nenhum dado.", text_color="gray").pack(pady=10)
        
        ctk.CTkLabel(self.main_frame, text="Últimos 3 Meses", font=("Arial", 15, "bold")).pack(anchor="w", padx=10, pady=(16, 4))

        meses_nomes = ["Janeiro", "Feveireiro", "Março", "Abril", "Maio",
                        "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro","Dezembro"]
        
        for delta in range(2, -1, -1):
            m = mes - delta
            a = ano
            if m <= 0:
                m += 12
                a -= 1
            res = resumo_por_categoria(m, a)
            r = sum(v for _, v in res if v > 0)
            g = abs(sum(v for _, v in res if v < 0))
            s = r - g
            destaque = "→ " if m == mes else ""
            cor_s = "#2ecc71" if s >= 0 else "#e74c3c"
            texto = f"{destaque}{meses_nomes[m-1][:3]} {a} | Rec: R$ {r:,.2f} Gasto: R$ {g:,.2f} Saldo: R$ {s:,.2f}"
            ctk.CTkLabel(self.main_frame, text=texto, text_color=cor_s).pack(anchor="w", padx=20, pady=3)
    def deletar(self, id):
        from core.database import deletar_transacao
        deletar_transacao(id)
        self.show_transacoes()
    def importar_emails_completo(self):
        from core.database import salvar_transacao
        from core.categorizer import categorizar
        transacoes = processar_emails(EMAIL, SENHA, completo=True)
        for t in transacoes:
            categoria = categorizar(t["descricao"])
            data_obj = datetime.strptime(t["data"], "%d/%m/%Y")
            data = data_obj.strftime("%Y-%m-%d")
            salvar_transacao(data, t["valor"], t["descricao"], categoria, "gasto")
        self.update_dashboard()
