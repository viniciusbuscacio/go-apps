# go-apps — perguntas de escopo (v2, modelo repo-hub)

Decidido até aqui: go-apps é um **repo-hub** — um home explicando o projeto e
apontando pros repos; cada app/lib vive no seu próprio repositório. A lib de
update chama **go-updates**. Releases continuam por repo, isolados.

Responda abaixo de cada pergunta ("R:").

## go-apps (o hub)

**1.** O README do hub segue o padrão dos outros repos: em **inglês**, com um
screenshot + descrição curta + link pra cada projeto?

R:

**2.** Além dos links, o hub mostra uma seção de **downloads** (link direto pro
latest release de cada app)? Enquanto os repos forem privados isso só funciona
pra você logado — tudo bem?

R:

**3.** Os **docs da família** (arquitetura do mini-framework, contrato
/v1/ax + agent-api, regras de release/update) sobem pro hub como documentação
compartilhada, e cada repo mantém só o que é específico dele — ou cada repo
segue completo e o hub só linka?

R:

**4.** O hub publica o **roadmap** da série (go-updates, go-install, file
explorer, CLI...)?

R:

**5.** Criamos um **CLAUDE.md no hub** com as convenções da família (estrutura
padrão, "lógica no Go / UI só desenha", contrato de riscos, fluxo de release)
pra guiar as sessões de trabalho em qualquer repo da família?

R:

## go-updates (a lib, repo próprio)

**6.** O repo go-updates nasce **público ou privado**? Detalhe técnico
importante: módulo Go privado importado pelos apps exige GOPRIVATE + token nos
CIs de todos os apps (atrito permanente). Público, o `go get` simplesmente
funciona — e não tem nada sensível na lib. Minha recomendação: público.

R:

**7.** Escopo da lib: só a **mecânica** (check / download / verify / swap /
relaunch / cleanup) ou também o adapter Wails genérico e snippets de UI de
referência (documentados no repo pra copiar)?

R:

**8.** O contrato atual se mantém: cada app publica releases **no seu próprio
repo** com assets `<app>-<tag>-<os>-<arch>` + `checksums.txt`, e a lib
consulta o `releases/latest` daquele repo. Confirma (nada muda na mecânica,
só o código muda de casa)?

R:

**9.** Versionamento da lib: tags semver (`v0.1.0`, `v0.2.0`...), apps **pinam
a versão** no go.mod e sobem quando quiserem (`go get -u`). Ok?

R:

**10.** Migração dos apps: assim que a go-updates existir, troco o
`internal/updater` do go-notepad e do go-calc pelo import da lib. No
go-notepad isso vira o **v0.2.1** — que de quebra é o release que testa o
ciclo real de update (0.2.0 → 0.2.1) na sua máquina. Fechado?

R:

**11.** CI da go-updates: `go test` nos 3 SOs (ubuntu/windows/macos) a cada
push, sem release binário (é lib). Suficiente?

R:

## go-install (futuro)

**12.** go-install é **lib** (o wizard next-next-finish embutido no próprio
binário de cada app, modelo "se instala sozinho") ou um **app** instalador
separado?

R:

**13.** Também nasce como repo próprio (`go-install`), no mesmo modelo da
go-updates?

R:

**14.** Prioridade depois do hub + go-updates: **go-install** ou o próximo
**app** da série (file explorer / CLI)?

R:

## Privacidade e publicação

**15.** go-apps privado por enquanto — qual o **gatilho** pra abrir? (ex.:
quando a série do YouTube chegar nesses projetos)

R:

**16.** go-calc e go-notepad continuam **privados** até esse gatilho também, e
na abertura vai tudo junto (hub + repos)?

R:

## Operacional

**17.** Pendência da conversa anterior: o updater do go-calc está pronto,
testado e **não commitado**. Subo agora no repo dele + tag **v0.1.0** (primeiro
release do go-calc), antes de começar a go-updates?

R:

**18.** Ordem geral que eu proponho: (a) commit+v0.1.0 go-calc → (b) repo
go-updates com a lib extraída → (c) migração go-notepad v0.2.1 + teste do
ciclo real → (d) migração go-calc v0.1.1 → (e) README do hub. Aprova ou muda
algo?

R:

**19.** As pastas locais continuam como estão (`dev\go-calc`, `dev\go-notepad`,
`dev\go-apps`, e futuramente `dev\go-updates`), uma por repo?

R:

**20.** Registro na minha memória as convenções da família (modelo hub, nomes,
fluxo de release com checksums, contrato da lib) pra não precisar reconstruir
esse contexto nas próximas sessões — pode?

R:
