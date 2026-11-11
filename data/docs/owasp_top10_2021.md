# OWASP Top 10 (edição 2021, resumo)

## A01 Broken Access Control
Falhas de controle de acesso permitem que usuários ajam fora das permissões previstas, como ler dados de outros usuários ou alterar registros alheios. Mitigação: negar por padrão, aplicar controle de acesso no servidor e registrar falhas de acesso.

## A02 Cryptographic Failures
Falta de proteção adequada de dados sensíveis em trânsito e em repouso, por exemplo uso de algoritmos fracos, chaves mal gerenciadas ou ausência de TLS. Mitigação: criptografar dados sensíveis, usar algoritmos atuais e gerenciar chaves corretamente.

## A03 Injection
Dados não confiáveis enviados a um interpretador como parte de um comando ou consulta, como SQL injection e injeção de comandos. Mitigação: consultas parametrizadas, validação de entrada e uso de APIs seguras.

## A04 Insecure Design
Falhas de projeto, anteriores à implementação, por falta de controles de segurança no desenho. Mitigação: modelagem de ameaças, padrões de design seguro e ciclo de vida de desenvolvimento seguro (Secure SDLC).

## A05 Security Misconfiguration
Configurações inseguras ou padrão, serviços desnecessários habilitados, mensagens de erro verbosas e contas padrão ativas. Mitigação: hardening, ambientes reproduzíveis e revisão de configurações.

## A06 Vulnerable and Outdated Components
Uso de bibliotecas, frameworks e componentes com vulnerabilidades conhecidas ou sem suporte. Mitigação: inventário de dependências, atualização contínua e ferramentas de análise de composição de software, como OWASP Dependency-Check.

## A07 Identification and Authentication Failures
Fraquezas na confirmação da identidade, como senhas fracas, ausência de autenticação multifator e sessões mal gerenciadas. Mitigação: MFA, políticas de senha e proteção contra força bruta.

## A08 Software and Data Integrity Failures
Falta de verificação de integridade em atualizações, dados e pipelines de CI/CD, incluindo dependências não verificadas. Mitigação: assinaturas digitais, verificação de integridade e pipelines protegidos.

## A09 Security Logging and Monitoring Failures
Registro e monitoramento insuficientes impedem detectar e responder a ataques. Mitigação: logs de eventos relevantes, alertas e plano de resposta a incidentes.

## A10 Server-Side Request Forgery (SSRF)
A aplicação busca um recurso remoto a partir de uma URL fornecida pelo usuário sem validação, permitindo acessar serviços internos. Mitigação: validar URLs, usar listas de permissão e segmentar a rede.
