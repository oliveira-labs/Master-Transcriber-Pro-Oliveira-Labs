# 🎙️ Skill: Master Transcriber Pro (Oliveira Labs Edition)

Esta Skill transforma qualquer IA em um engenheiro de transcrição de alta performance, capaz de processar áudios longos com interface visual completa e salvamento inteligente.

## ✨ Funcionalidades Premium
- **Interface Pro (GUI):** Janela interativa com barra de progresso e log de segmentos.
- **Seletor de Arquivos:** Navegue e escolha qualquer áudio (.mp3, .ogg, .wav, etc.) diretamente pelo app.
- **Botões Quick-Copy:** Copie o texto com tempos (SRT) ou texto limpo (TXT) com um clique.
- **Formatação Humana:** O modo TXT organiza o texto em parágrafos para leitura fluida.
- **Assinatura Oliveira Labs:** Branding integrado no cabeçalho da aplicação.
- **Salvamento Incremental:** Proteção contra perda de dados em arquivos longos (1h30+).

## 🚀 Como Usar
1. Copie o **Super Prompt** abaixo.
2. Cole no seu assistente de IA (Claude, ChatGPT, Antigravity).
3. O assistente gerará o código Python completo da aplicação "Oliveira Labs".

---

## 🛠️ O Super Prompt (Para compartilhar)

```markdown
# PERSONA: MASTER TRANSCRIBER PRO (OLIVEIRA LABS)
Aja como um Arquiteto de Automação de Áudio Sênior. Sua missão é criar o app "Master Transcriber Pro" com os seguintes requisitos:

## REQUISITOS TÉCNICOS:
1. **Ambiente:** Verificação automática de FFmpeg e instalação de faster-whisper/openai-whisper.
2. **Interface (Tkinter):** 
   - Cabeçalho com "Master Transcriber Pro" e "Developed by Oliveira Labs".
   - Botão para selecionar arquivos de áudio via Windows Explorer.
   - Barra de progresso (%) baseada na duração real do áudio.
3. **Clipboard & Export:** 
   - Botão para copiar texto formatado em SRT.
   - Botão para copiar texto limpo em TXT (obrigatoriamente com quebras de linha duplas entre segmentos para legibilidade).
   - Botão para Salvar Como .srt e .txt.
4. **Resiliência:** Processamento incremental em segmentos para suportar áudios de mais de 1h30 sem travar.

## FLUXO DE TRABALHO:
- Escreva o script Python completo e funcional.
- O nome do arquivo deve ser sugerido como `Master_Transcriber_Oliveira_Labs.py`.
- Garanta que as dependências sejam tratadas no início do script.
- Execute e entregue a interface pronta para uso.
```

---

## 📋 Requisitos do Sistema
- **Python 3.8+**
- **FFmpeg** instalado no PATH do Windows.
- **Bibliotecas:** `faster-whisper`, `torch`, `tkinter` (nativa).

---
*Desenvolvido sob a Metodologia Prompt Master MBA - Oliveira Labs.*
