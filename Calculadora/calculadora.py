import divide
import multiplica
import soma
import subtrai

def main():
    a = float (input("Digite o primeiro número real: "))
    b = float (input("Digite o segundo número real: "))
    operador = input("Qual operção você deseja realizar (+|-|*|/): ")

    if operador == "+":
        resultado = soma.somaf(a,b)
    
    elif operador == "-":
        resultado = subtrai.subtraif(a,b)

    elif operador == "*":
        resultado = multiplica.multiplicaf(a,b)

    elif operador == "/":
        resultado = divide.dividef(a,b)
    
    else:
        resultado = "Número ou operador inválido!"

    print (f"Resultado: {resultado}")

main()