# Windows-Environment-Variables-Edito

---

### ✅ Funcionalidades:

* Ver e editar variáveis de ambiente do utilizador (`HKEY_CURRENT_USER`).
* Adicionar nova variável.
* Apagar variável existente.
* Guardar alterações.
* Sair da aplicação.

---

### 📦 Pré-requisitos:

Instalar PyQt5:

```bash
pip install PyQt5
```

---

### 🧪 Como usar:

1. **Executa o script** em Windows 10 com Python.
2. A janela mostra as variáveis do utilizador.
3. Seleciona uma variável para editar, ou insere nome e valor novos para adicionar.
4. Usa os botões:

   * **Editar**: modifica a variável existente.
   * **Escrever**: adiciona nova variável.
   * **Apagar**: remove a variável selecionada.
   * **OK**: recarrega a lista.
   * **Sair**: fecha a aplicação.

---

### ⚠️ Nota:

* Esta aplicação edita variáveis **do utilizador atual** (`HKEY_CURRENT_USER\Environment`).
* Para editar variáveis do sistema (`HKEY_LOCAL_MACHINE`), seria necessário executar como **administrador** e alterar o caminho no `winreg`.

---

