import os
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import database
import config
import notifications
import crud_produtos  # Para listar produtos
import crud_servicos  # Para listar serviços

# ======================================================================
# FUNÇÕES DE VENDAS
# ======================================================================

def registrar_venda():
    print("\n--- Registrar Nova Venda ---")
    if not database.produtos and not database.servicos:
        print(
            "❌ Não é possível registrar venda: nenhum produto ou serviço cadastrado."
        )
        return

    itens = []
    total = 0.0  # total é um <float>

    while True:
        print("\n1. Adicionar Produto")
        print("2. Adicionar Serviço")
        print("3. Finalizar Venda")
        print("0. Cancelar Venda")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            print("\nProdutos disponíveis:")
            crud_produtos.listar_produtos()
            if not database.produtos:
                print("❌ Nenhum produto cadastrado.")
                continue
            try:
                codigo_produto = int(
                    input("\nDigite o código do produto (ou '0' para voltar): ")
                )
                if codigo_produto == 0:
                    continue
                
                produto_encontrado = next(
                    (p for p in database.produtos if p["codigo"] == codigo_produto), None
                )
                if not produto_encontrado:
                    print("❌ Produto não encontrado.")
                    continue
                    
                quantidade = int(input("Quantidade vendida: "))
                if quantidade <= 0:
                    print("\n❌ Erro: A quantidade deve ser maior que zero.")
                    continue
                if quantidade > produto_encontrado["quantidade"]:
                    print(
                        f"\n❌ Erro: Estoque insuficiente. Disponível: {produto_encontrado['quantidade']} unidades."
                    )
                    continue
                
                # 'produto_encontrado["preco"]' é um <Decimal>
                subtotal_decimal = quantidade * produto_encontrado["preco"]
                
                # Converte para float para salvar no JSON
                subtotal_float = float(subtotal_decimal)
                preco_unitario_float = float(produto_encontrado["preco"])

                itens.append(
                    {
                        "tipo": "produto",
                        "codigo_item": codigo_produto,
                        "nome": produto_encontrado["nome"],
                        "quantidade": quantidade,
                        "preco_unitario": preco_unitario_float, # Salva como float
                        "subtotal": subtotal_float,           # Salva como float
                    }
                )
                produto_encontrado["quantidade"] -= quantidade # Abate do estoque
                
                total += subtotal_float # Soma o float
                
                print(
                    f"\n✅ Produto '{produto_encontrado['nome']}' ({quantidade} unidade(s)) adicionado. Subtotal: R${subtotal_float:.2f}"
                )
            except ValueError:
                print(
                    "\n❌ Erro: O código do produto e a quantidade devem ser números inteiros."
                )

        elif opcao == "2":
            print("\nServiços disponíveis:")
            crud_servicos.listar_servicos()
            if not database.servicos:
                print("❌ Nenhum serviço cadastrado.")
                continue
            try:
                codigo_servico = int(
                    input("\nDigite o código do serviço (ou '0' para voltar): ")
                )
                if codigo_servico == 0:
                    continue
                
                servico_encontrado = next(
                    (s for s in database.servicos if s["codigo"] == codigo_servico), None
                )
                if not servico_encontrado:
                    print("❌ Serviço não encontrado.")
                    continue
                
                # 'servico_encontrado["preco"]' é um <Decimal>
                subtotal_decimal = servico_encontrado["preco"]

                # Converte para float para salvar no JSON
                subtotal_float = float(subtotal_decimal)

                itens.append(
                    {
                        "tipo": "serviço",
                        "codigo_item": codigo_servico,
                        "nome": servico_encontrado["nome"],
                        "quantidade": 1,
                        "preco_unitario": subtotal_float, # Salva como float
                        "subtotal": subtotal_float,       # Salva como float
                    }
                )

                total += subtotal_float # Soma o float
                
                print(
                    f"\n✅ Serviço '{servico_encontrado['nome']}' adicionado. Subtotal: R${subtotal_float:.2f}"
                )
            except ValueError:
                print("\n❌ Erro: O código do serviço deve ser um número inteiro.")

        elif opcao == "3":
            if not itens:
                print("\n❌ Erro: Nenhum item adicionado à venda.")
                continue
            
            venda = {
                "codigo": database.proximo_codigo_venda,
                "itens": itens, # Agora a lista 'itens' só contém floats
                "total": total,
                "data": datetime.now().strftime("%d/%m/%Y"),
            }
            database.vendas.append(venda)
            database.proximo_codigo_venda += 1
            
            # Agora, o salvar_dados() não vai mais falhar
            database.salvar_dados()
            
            notifications.enviar_notificacao_venda(itens, total)
            
            # Notifica estoque baixo APÓS salvar a venda
            for item in itens:
                if item["tipo"] == "produto":
                    produto_notifica = next(
                        (p for p in database.produtos if p["codigo"] == item["codigo_item"]),
                        None,
                    )
                    if produto_notifica:
                        notifications.enviar_notificacao_estoque(
                            produto_notifica["nome"], produto_notifica["quantidade"]
                        )
                        
            print(f"\n✅ Venda registrada com sucesso! Total: R${total:.2f}")
            break

        elif opcao == "0":
            # Restaurar estoque dos produtos já adicionados
            for item in itens:
                if item["tipo"] == "produto":
                    produto_encontrado = next(
                        (p for p in database.produtos if p["codigo"] == item["codigo_item"]),
                        None,
                    )
                    if produto_encontrado:
                        produto_encontrado["quantidade"] += item["quantidade"]
            
            # Não precisa salvar, pois a transação foi cancelada
            print("\n❌ Venda cancelada.")
            break

        else:
            print("\n❌ Opção inválida.")


def listar_vendas():
    print("\n--- Lista de Vendas ---")
    if not database.vendas:
        print("Nenhuma venda registrada.")
        return
    for venda in database.vendas:
        print(f"\nVenda Código: {venda['codigo']}")
        print(f"Data: {venda['data']}")
        # Converte o total (que pode ser Decimal) para float para formatar
        print(f"Total: R${float(venda['total']):.2f}") 
        print("Itens:")
        
        # Os itens já vêm como float do JSON, então não precisamos converter aqui
        df = pd.DataFrame(
            venda["itens"],
            columns=[
                "tipo", "codigo_item", "nome", "quantidade",
                "preco_unitario", "subtotal",
            ],
        )
        
        # Formata as colunas de preço para exibição
        df['preco_unitario'] = df['preco_unitario'].map('R${:,.2f}'.format)
        df['subtotal'] = df['subtotal'].map('R${:,.2f}'.format)

        print(
            df.to_string(
                index=False,
                col_space={
                    "tipo": 12, "codigo_item": 12, "nome": 30, "quantidade": 12,
                    "preco_unitario": 15, "subtotal": 12,
                },
            )
        )
        print("-" * 110)
    print(f"\nTotal de vendas registradas: {len(database.vendas)}")


def remover_venda():
    print("\n--- Cancelar Venda ---")
    listar_vendas()
    if not database.vendas:
        return
    try:
        codigo = int(input("\nDigite o código da venda para cancelar: "))
        venda_encontrada = next((v for v in database.vendas if v["codigo"] == codigo), None)
        if venda_encontrada:
            # Restaurar estoque dos produtos
            for item in venda_encontrada["itens"]:
                if item["tipo"] == "produto":
                    produto_encontrado = next(
                        (p for p in database.produtos if p["codigo"] == item["codigo_item"]),
                        None,
                    )
                    if produto_encontrado:
                        produto_encontrado["quantidade"] += item["quantidade"]
            
            notifications.enviar_notificacao_cancelamento_venda(
                venda_encontrada["itens"], venda_encontrada["total"]
            )
            
            database.vendas.remove(venda_encontrada)
            database.salvar_dados()
            
            # Notifica estoque APÓS salvar
            for item in venda_encontrada["itens"]:
                if item["tipo"] == "produto":
                    produto_notifica = next(
                        (p for p in database.produtos if p["codigo"] == item["codigo_item"]),
                        None,
                    )
                    if produto_notifica:
                        notifications.enviar_notificacao_estoque(
                            produto_notifica["nome"], produto_notifica["quantidade"]
                        )
                        
            print("\n✅ Venda cancelada com sucesso!")
        else:
            print("❌ Venda não encontrada.")
    except ValueError:
        print("\n❌ Erro: O código deve ser um número inteiro.")


def calcular_totais_vendas():
    print("\n--- Totais de Vendas ---")
    if not database.vendas:
        print("Nenhuma venda registrada.")
        return
    
    # Converte 'total' para float para garantir que o Pandas some corretamente
    vendas_formatadas = []
    for v in database.vendas:
        v_copia = v.copy()
        v_copia["total"] = float(v_Copia["total"])
        vendas_formatadas.append(v_copia)
        
    df = pd.DataFrame(vendas_formatadas)
    
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    hoje = datetime.now()
    total_dia = df[df["data"].dt.date == hoje.date()]["total"].sum()
    total_mes = df[
        (df["data"].dt.month == hoje.month) & (df["data"].dt.year == hoje.year)
    ]["total"].sum()
    total_ano = df[df["data"].dt.year == hoje.year]["total"].sum()
    print(f"Total de vendas no dia: R${total_dia:.2f}")
    print(f"Total de vendas no mês: R${total_mes:.2f}")
    print(f"Total de vendas no ano: R${total_ano:.2f}")


def relatorio_vendas():
    print("\n--- Relatório de Vendas (Estatísticas + Gráficos + Excel) ---")
    if not database.vendas:
        print("Nenhuma venda registrada.")
        return

    # Converte 'total' para float para garantir que o Pandas use os números corretos
    vendas_formatadas = []
    for v in database.vendas:
        v_copia = v.copy()
        v_copia["total"] = float(v["total"])
        vendas_formatadas.append(v_copia)
        
    df = pd.DataFrame(vendas_formatadas)
    
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
    df = df.dropna(subset=["data"])
    if df.empty:
        print("Sem datas válidas para análise.")
        return

    valores = df["total"].astype(float)
    media_ticket = valores.mean()
    mediana_ticket = valores.median()
    modas_ticket = valores.mode()
    moda_ticket_str = "—" if modas_ticket.empty else ", ".join(
        [f"R${m:.2f}" for m in modas_ticket.tolist()]
    )

    print("\n» Estatísticas do ticket por venda")
    print(f"- Média:   R${media_ticket:.2f}")
    print(f"- Mediana: R${mediana_ticket:.2f}")
    print(f"- Moda(s): {moda_ticket_str}")

    df_dia_serie = (
        df.assign(dia=df["data"].dt.to_period("D"))
          .groupby("dia", as_index=False)["total"]
          .sum()
          .rename(columns={"total": "total_dia"})
    )
    df_dia_serie["dia"] = df_dia_serie["dia"].dt.to_timestamp()

    if not df_dia_serie.empty:
        plt.figure()
        plt.plot(df_dia_serie["dia"], df_dia_serie["total_dia"], marker="o")
        plt.title("Vendas por Dia (Série Completa)")
        plt.xlabel("Data")
        plt.ylabel("Total (R$)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        caminho_png_serie = os.path.join(
            config.PASTA, f"grafico_vendas_serie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        try:
            plt.savefig(caminho_png_serie, dpi=120)
            print(f"\n📈 Gráfico (série completa) salvo em: {caminho_png_serie}")
        except Exception as e:
            print(f"\n❌ Não foi possível salvar o gráfico da série completa: {e}")
        finally:
            plt.close()
    else:
        print("\nNão há dados suficientes para gerar o gráfico da série completa.")

    hoje = datetime.now()
    mes_atual = hoje.month
    ano_atual = hoje.year

    df_mes_atual = df[
        (df["data"].dt.month == mes_atual) & (df["data"].dt.year == ano_atual)
    ]
    if df_mes_atual.empty:
        print("\nNenhuma venda no mês atual para gerar gráfico/estatísticas mensais.")
    else:
        df_dia_mes = (
            df_mes_atual.assign(dia=df_mes_atual["data"].dt.to_period("D"))
                        .groupby("dia", as_index=False)["total"]
                        .sum()
                        .rename(columns={"total": "total_dia"})
        )
        df_dia_mes["dia"] = df_dia_mes["dia"].dt.to_timestamp()

        plt.figure()
        plt.plot(df_dia_mes["dia"], df_dia_mes["total_dia"], marker="o")
        plt.title(f"Vendas por Dia - Mês Atual ({mes_atual:02d}/{ano_atual})")
        plt.xlabel("Data")
        plt.ylabel("Total (R$)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        caminho_png_mes = os.path.join(
            config.PASTA, f"grafico_vendas_mes_atual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        try:
            plt.savefig(caminho_png_mes, dpi=120)
            print(f"📊 Gráfico (mês atual) salvo em: {caminho_png_mes}")
        except Exception as e:
            print(f"\n❌ Não foi possível salvar o gráfico do mês atual: {e}")
        finally:
            plt.close()

        media_mes_atual = df_dia_mes["total_dia"].mean()
        mediana_mes_atual = df_dia_mes["total_dia"].median()
        modas_mes_atual = df_dia_mes["total_dia"].mode()
        moda_mes_atual_str = "—" if modas_mes_atual.empty else ", ".join(
            [f"R${m:.2f}" for m in modas_mes_atual.tolist()]
        )

        print("\n» Estatísticas do mês atual (sobre totais diários)")
        print(f"- Média diária:   R${media_mes_atual:.2f}")
        print(f"- Mediana diária: R${mediana_mes_atual:.2f}")
        print(f"- Moda(s) diária(s): {moda_mes_atual_str}")

    df_mes = (
        df.assign(ano_mes=df["data"].dt.to_period("M"))
          .groupby("ano_mes", as_index=False)["total"]
          .sum()
          # ==================
          #  MUDANÇA BEM AQUI (Corrigido de total_toes para total_mes)
          # ==================
          .rename(columns={"total": "total_mes"}) 
    )
    df_mes["ano_mes_dt"] = df_mes["ano_mes"].dt.to_timestamp()

    if df_mes.empty:
        print("\nSem dados para estatísticas mensais.")
    else:
        media_mensal = df_mes["total_mes"].mean()
        mediana_mensal = df_mes["total_mes"].median()
        modas_mensal = df_mes["total_mes"].mode()
        moda_mensal_str = "—" if modas_mensal.empty else ", ".join(
            [f"R${m:.2f}" for m in modas_mensal.tolist()]
        )

        print("\n» Estatísticas mensais (sobre totais do mês)")
        print(f"- Média mensal:   R${media_mensal:.2f}")
        print(f"- Mediana mensal: R${mediana_mensal:.2f}")
        print(f"- Moda(s) mensal(is): {moda_mensal_str}")

    caminho_excel = os.path.join(
        config.PASTA, f"relatorio_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )
    try:
        with pd.ExcelWriter(caminho_excel, engine="xlsxwriter") as writer:
            estatisticas = []

            estatisticas.append(
                {"Categoria": "Ticket por venda - Média", "Valor": media_ticket}
            )
            estatisticas.append(
                {"Categoria": "Ticket por venda - Mediana", "Valor": mediana_ticket}
            )
            estatisticas.append(
                {"Categoria": "Ticket por venda - Moda(s)", "Valor": moda_ticket_str}
            )

            if not df_mes_atual.empty:
                estatisticas.append(
                    {"Categoria": "Mês atual - Média diária", "Valor": media_mes_atual}
                )
                estatisticas.append(
                    {"Categoria": "Mês atual - Mediana diária", "Valor": mediana_mes_atual}
                )
                estatisticas.append(
                    {"Categoria": "Mês atual - Moda(s) diária(s)", "Valor": moda_mes_atual_str}
                )

            if not df_mes.empty:
                estatisticas.append(
                    {"Categoria": "Mensal - Média dos totais", "Valor": media_mensal}
                )
                estatisticas.append(
                    {"Categoria": "Mensal - Mediana dos totais", "Valor": mediana_mensal}
                )
                estatisticas.append(
                    {"Categoria": "Mensal - Moda(s) dos totais", "Valor": moda_mensal_str}
                )

            df_est = pd.DataFrame(estatisticas)
            df_est.to_excel(writer, sheet_name="Estatísticas", index=False)

            df_dia_serie.to_excel(writer, sheet_name="Vendas_por_dia_serie", index=False)
            if 'df_dia_mes' in locals() and not df_dia_mes.empty:
                df_dia_mes.to_excel(writer, sheet_name="Vendas_por_dia_mes_atual", index=False)

            if not df_mes.empty:
                df_mes.rename(columns={"ano_mes_dt": "mes"}, inplace=True)
                df_mes[["mes", "total_mes"]].to_excel(writer, sheet_name="Vendas_por_mes", index=False)

        print(f"\n📄 Relatório Excel salvo em: {caminho_excel}")
    except Exception as e:
        print(f"\n❌ Não foi possível gerar o relatório Excel: {e}")