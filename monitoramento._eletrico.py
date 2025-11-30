!git status
!git add .
!git commit -m "Aula 1 - estrutura inicial"
!git push
# modulo extra, linhas 123-140

#======== Lista de Listas ============
# - lista simples guarda valores, mas uma de listas pode guardas várias informações sobre o mesmo elemento
# - Cada circuito presente nesta lista de circuitos possuem repesctivamente: nome, tipo, tensão, corrente, fator de potência, frequência, data de medição.
circuitos = [
    ["Circuito 1", "iluminacao", 220.0, 8.5, 0.95, 60.0, "05/11/2025"],
    ["Motor Bomba", "motor", 220.0, 14.0, 0.78, 60.0, "05/11/2025"],
]

for c in circuitos:
    print("Nome:", c[0], "| Tipo:", c[1], "| V:", c[2], "| I:", c[3], "| fp:", c[4])

# - adicionei exatamente os códigos de exemplo (alimentador principal e banco de tomadas sala 2)
circuitos.append(["Alimentador Principal", "alimentador", 220.0, 25.0, 0.92, 60.0, "05/11/2025"])
circuitos.append(["Banco Tomadas Sala 2", "tomada", 127.0, 9.5, 0.88, 60.0, "03/11/2025"])
for c in circuitos:
    print(c)


#============ Dicionário ============
# - guarda informações no formato chave : valor
# - Será usado para guardar limites elétricos por tipo de circuito que estão na lista de listas anteriormente
limites = {
    "iluminacao": {"i_max": 10.0, "fp_min": 0.9, "tensao_nom": 220},
    "motor": {"i_max": 20.0, "fp_min": 0.75, "tensao_nom": 220},
    "tomada": {"i_max": 15.0, "fp_min": 0.8, "tensao_nom": 127},
    "alimentador": {"i_max": 40.0, "fp_min": 0.92, "tensao_nom": 220},
}

tolerancia_tensao = 0.10  # 10%

def dentro_da_faixa(circuito):
    nome, tipo, v, i, fp, f, data = circuito
    regra = limites.get(tipo, None)
    if not regra:
        return True
    if not (regra["tensao_nom"] * (1 - tolerancia_tensao) <= v <= regra["tensao_nom"] * (1 + tolerancia_tensao)):
        return False
    if i > regra["i_max"]:
        return False
    if fp < regra["fp_min"]:
        return False
    return True

for c in circuitos:
    print(c[0], "está dentro da faixa?", dentro_da_faixa(c))


# ========== Strings ================
# - muitas vezes as medições chegam em texto, aqui as informações serão separadas e atualizarão a lista
def registrar_medicao(linha):
    partes = linha.split(";")
    nome = partes[0].strip()
    medidas = {}
    for pedaco in partes[1:]:
        pedaco = pedaco.strip()
        if "=" in pedaco:
            k, v = pedaco.split("=")
            medidas[k.strip().lower()] = v.strip()

    for c in circuitos:
        if c[0] == nome:
            if "v" in medidas:
                c[2] = float(medidas["v"])
            if "i" in medidas:
                c[3] = float(medidas["i"])
            if "fp" in medidas:
                c[4] = float(medidas["fp"])
            if "f" in medidas:
                c[5] = float(medidas["f"])
            break

registrar_medicao("Circuito 1; V=213; I=11.2; fp=0.82; f=60")
for c in circuitos:
    print(c)


# ========== Arquivo ============
# - para não perder os dados, pode salvar em arquivos
# - Salvar circuito e verificar quem está fora de faixa
def salvar_circuitos(nome_arquivo="circuitos.txt"):
    with open(nome_arquivo, "w") as arq:
        for c in circuitos:
            linha = f"{c[0]};{c[1]};{c[2]};{c[3]};{c[4]};{c[5]};{c[6]}\n"
            arq.write(linha)
    print("Circuitos salvos em", nome_arquivo)

def gerar_relatorio_nao_conforme(nome_arquivo="relatorio_nao_conforme.txt"):
    with open(nome_arquivo, "w") as arq:
        arq.write("RELATÓRIO DE NÃO CONFORMIDADE\n\n")
        for c in circuitos:
            if not dentro_da_faixa(c):
                arq.write(f"Circuito: {c[0]}\n")
                arq.write(f"  Tipo: {c[1]} | V={c[2]} V | I={c[3]} A | fp={c[4]} | f={c[5]} Hz\n\n")
    print("Relatório gerado.")

salvar_circuitos()
gerar_relatorio_nao_conforme()

# ======== Análises Elétricos ============
# - identificar fatores de menor potência
def resumo_eletrico():
    menor_fp = min(circuitos, key=lambda x: x[4])

# - Contar quantos estão fora da caixa
    fora = [c for c in circuitos if not dentro_da_faixa(c)]
  
# - encontrar o mais sobrecarregado
    mais_sobrecarregado = max(circuitos, key=lambda x: x[3])

# - prints do resultado desses cálculos
    print("Circuito com menor fator de potência:", menor_fp[0], "-", menor_fp[4])
    print("Total de circuitos fora da faixa:", len(fora))
    print("Circuito mais sobrecarregado:", mais_sobrecarregado[0], "-", mais_sobrecarregado[3], "A")

resumo_eletrico()


# ================ Módulo Extra - UPS ==============
# = Registro de UPS, o usuário precisa inserir o valor da tensão (V) de entrada e saída, quando a entrada é maior que 200 V, aparece no arquivo "UPS acionada", em qualquer entrada e saída inserida é inserida no arquivo um novo registro
def modulo_extra():
    print("Monitoramento de UPS")
    print("Para funcionar insira o valor da tensão de entrada e saída")

    entrada = float(input("Insira o valor de tensão (V) de entrada: "))
    saida = float(input("Insira o valor de tensão (V) de saída: "))

    with open("registroUPS.txt", "a") as arq:
        arq.write(f"Entrada={entrada} V | Saída={saida} V\n")
        
        if entrada < 200:
            arq.write("UPS acionada\n")

    print("Registro salvo!")
      
modulo_extra()


# ================ Menu Final ==============
# - Serve para rodar o sistema completo
def main():
    print("=== Sistema de Monitoramento Elétrico ===")
    print("1 - Registrar medição")
    print("2 - Salvar circuitos")
    print("3 - Gerar relatório de não conformidade")
    print("4 - Resumo elétrico")
    print("5 - Monitoramento de UPS")
    opc = input("Escolha: ")
    if opc == "1":
        linha = input("Digite: Nome; V=...; I=...; fp=...; f=...\n")
        registrar_medicao(linha)
    elif opc == "2":
        salvar_circuitos()
    elif opc == "3":
        gerar_relatorio_nao_conforme()
    elif opc == "4":
        resumo_eletrico()
    elif opc == "5":
        modulo_extra()
    else:
        print("Opção inválida")

if __name__ == "__main__":
  main()
