# urirun-contract-capture-click

**Format `urirun-contract-*`: README opisuje intencję, lokalny LLM proponuje kontrakt,
generator deterministycznie robi kod, bramy egzekwują — CI tylko weryfikuje.**

## Co ten projekt robi (źródło intencji dla LLM)

**Handoff CZĘŚCIOWY** między dwoma procesami — pokazuje krawędź, która niesie *podzbiór* wejścia:

- `screen/query/capture` — **query**. Robi zrzut ekranu. Zwraca `oneOf`: wariant **Sukces**
  (`kind=screenshot`, `path`, `bytes`, `fullSize: [int]`, `via`) albo **Degraded**
  (`degraded=true`, `degradedReason` — np. placeholder portalu zamiast realnej klatki).
- `abs/command/click` — **command**. Klika piksel `(x,y)` w przestrzeni ekranu `(sw,sh)` przez
  surowe urządzenie absolutne uinput.

Krawędź `WIRES` mapuje `sw ← fullSize.0`, `sh ← fullSize.1` — rozmiar ekranu ze zrzutu zasila
przestrzeń kliknięcia. To handoff **częściowy**: `x,y` są wymagane i pochodzą z osobnego kroku
locate, nie z tej krawędzi. `consumer_input_check` zwraca `mode=partial` i typuje tylko niesione pola.

Błędy: `capture-backend-missing`, `portal-denied`, `uinput-unavailable`.

## Pipeline

```bash
make gen        # contracts.json → src/handlers_generated.py
make check      # conform (efekt↔czasownik, oneOf, przykłady) + anty-dryf — bez LLM
```

Kontrakt używa schematu-listy `["int"]` (dla `fullSize`/`screen`) oraz `oneOf` (Sukces|Degraded).

## Wariant wielopakietowy (dwa procesy, transport)

```bash
PORT=8801 python packages/producer/service.py &     # screen/query/capture
PORT=8802 python packages/consumer/service.py &      # abs/command/click
python orchestrator/drive.py                          # capture ─HTTP→ click, PARTIAL handoff, exit 0/1
```

Orchestrator: woła zrzut, wydłubuje `sw,sh` z `fullSize` przez ścieżkę kropkową, potwierdza
`partial`, dokłada `x,y` (krok locate), woła klik. Konsument odrzuca brak wymaganych `x,y` (→ 422).

## Licencja

Apache-2.0 · Tom Sapletta · https://tom.sapletta.com
