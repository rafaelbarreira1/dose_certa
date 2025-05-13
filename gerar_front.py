import os

html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Cadastro de Usuário</title>
</head>
<body>
    <h2>Cadastro de Usuário</h2>
    <form id="formUsuario">
        <label>Nome: <input type="text" id="nome" required></label><br>
        <label>Email: <input type="email" id="email" required></label><br>
        <label>Senha: <input type="password" id="senha" required></label><br>
        <label>Permissão:
            <select id="permissao">
                <option value="admin">Admin</option>
                <option value="visualizador">Visualizador</option>
            </select>
        </label><br>
        <label>ID do Hospital: <input type="number" id="hospital_id" required></label><br>
        <button type="submit">Cadastrar</button>
    </form>

    <pre id="resposta"></pre>

    <script>
        const token = prompt("Insira seu token JWT:");

        document.getElementById("formUsuario").addEventListener("submit", async (e) => {
            e.preventDefault();

            const payload = {
                nome: document.getElementById("nome").value,
                email: document.getElementById("email").value,
                senha: document.getElementById("senha").value,
                permissao: document.getElementById("permissao").value,
                hospital_id: parseInt(document.getElementById("hospital_id").value)
            };

            const res = await fetch("http://localhost:8000/usuarios", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            document.getElementById("resposta").textContent = JSON.stringify(data, null, 2);
        });
    </script>
</body>
</html>
"""

os.makedirs("frontend_dose_certa", exist_ok=True)
with open("frontend_dose_certa/cadastro_usuario.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Arquivo cadastro_usuario.html criado com sucesso!")
