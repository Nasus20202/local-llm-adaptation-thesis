# Development-pilot Scenario Human Review Catalog

## What this document is

This is the **primary human-review view for PR #44**. It lists all 24 development-pilot scenario inputs so the researcher does not need to inspect JSON.

These 24 families are **only the development pilot / feasibility sample**. They are not the final benchmark and they are not the final-test set. Pilot evidence is used to validate task solvability, evaluator behavior, headroom, feasibility, and the later study design. Additional family-disjoint material will be constructed later under separate gates, including any training material required by F1 and the eventual protected final-test set.

The pilot remains exactly 8 knowledge + 8 procedural + 8 mixed families, with 4 Polish + 4 English families in each class.

## What the model receives

For the base scenario export, the canonical scenario payload is **only `input_text`**. The surrounding JSON is repository governance and custody metadata, not prompt content.

The base model does **not** receive family IDs, source/provenance metadata, source-evidence identifiers, OpenAPI schema identities, hashes, condition profiles, review metadata, evaluator metadata, or other scenario-record fields. A later experimental condition may add only context or tools explicitly authorized by that condition contract.

**Model-facing custody is not the same thing as prompt-visible content.**

## How to review

Review the scenario prose without consulting model outputs or protected answers. For each item, check:

- technical correctness and realism for Kubernetes v1.36.4;
- natural Polish or English wording;
- answerability (or intentional unanswerability for abstention);
- unambiguous constraints and response form;
- whether the item tests the stated capability rather than trivia;
- whether it is suitable for a pilot that can reveal meaningful adaptation differences without being selected around observed model performance.

The exact scenario inputs below are the unchanged `input_text` values; every individual input SHA-256 remains unchanged.

## Pilot index

| ID            | Class      | Language | Subtype                                  |
| ------------- | ---------- | -------- | ---------------------------------------- |
| `dev-k-pl-01` | Knowledge  | Polish   | `direct-evidence`                        |
| `dev-k-pl-02` | Knowledge  | Polish   | `synthesis`                              |
| `dev-k-pl-03` | Knowledge  | Polish   | `absent-answer-abstention`               |
| `dev-k-pl-04` | Knowledge  | Polish   | `distractor-heavy-evidence`              |
| `dev-k-en-01` | Knowledge  | English  | `direct-evidence`                        |
| `dev-k-en-02` | Knowledge  | English  | `synthesis`                              |
| `dev-k-en-03` | Knowledge  | English  | `absent-answer-abstention`               |
| `dev-k-en-04` | Knowledge  | English  | `distractor-heavy-evidence`              |
| `dev-p-pl-01` | Procedural | Polish   | `diagnosis`                              |
| `dev-p-pl-02` | Procedural | Polish   | `constrained-repair`                     |
| `dev-p-pl-03` | Procedural | Polish   | `ordered-action`                         |
| `dev-p-pl-04` | Procedural | Polish   | `structured-artifact-schema-adherence`   |
| `dev-p-en-01` | Procedural | English  | `diagnosis`                              |
| `dev-p-en-02` | Procedural | English  | `constrained-repair`                     |
| `dev-p-en-03` | Procedural | English  | `ordered-action`                         |
| `dev-p-en-04` | Procedural | English  | `structured-artifact-schema-adherence`   |
| `dev-m-pl-01` | Mixed      | Polish   | `evidence-backed-configuration-decision` |
| `dev-m-pl-02` | Mixed      | Polish   | `evidence-backed-bounded-procedure`      |
| `dev-m-pl-03` | Mixed      | Polish   | `evidence-backed-artifact-validation`    |
| `dev-m-pl-04` | Mixed      | Polish   | `evidence-backed-repair-plan`            |
| `dev-m-en-01` | Mixed      | English  | `evidence-backed-configuration-decision` |
| `dev-m-en-02` | Mixed      | English  | `evidence-backed-bounded-procedure`      |
| `dev-m-en-03` | Mixed      | English  | `evidence-backed-artifact-validation`    |
| `dev-m-en-04` | Mixed      | English  | `evidence-backed-repair-plan`            |

## Knowledge scenarios

### `dev-k-pl-01` — Polish — `direct-evidence`

**Purpose:** Tests direct factual grounding against the frozen Kubernetes source snapshot.

**Exact model scenario input:**

> W Kubernetes v1.36.4 kontener pobiera `LOG_LEVEL` z ConfigMap `app-settings` przez `env[].valueFrom.configMapKeyRef`. ConfigMap zmieniono z `info` na `debug`, ale proces w już działającym Podzie nadal widzi `info`.
>
> Odpowiedz zwięźle na dwa pytania:
>
> 1. Czy taka zmienna środowiskowa jest automatycznie aktualizowana w już uruchomionym kontenerze?
> 2. Co musi się stać z Podem, aby proces zobaczył nową wartość?
>
> Na końcu wskaż ścieżkę źródłową w zatwierdzonym snapshotcie, która uzasadnia odpowiedź.

**Input SHA-256:** `c656ada790aaba970c8b9b0c1349a6da2b2dc085805e8d89adf2bde6b7a66e6c`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-02` — Polish — `synthesis`

**Purpose:** Tests combining multiple documented facts without inventing missing behavior.

**Exact model scenario input:**

> Aplikacja w Kubernetes v1.36.4 zwykle potrzebuje około 90 sekund na pełne uruchomienie. Podczas tego czasu endpoint aplikacji nie powinien powodować restartów kontenera, a Pod nie powinien jeszcze otrzymywać ruchu z Service. Po zakończeniu startu aplikacja może czasem chwilowo nie być gotowa do obsługi ruchu, ale nadal działa poprawnie.
>
> Wyjaśnij, jak role `startupProbe`, `livenessProbe` i `readinessProbe` powinny się uzupełniać w tym scenariuszu. Odpowiedź ma opisać:
>
> - co ma chronić długi start aplikacji,
> - co decyduje o kierowaniu ruchu,
> - co powinno wykrywać stan wymagający restartu.
>
> Wskaż ścieżki źródłowe z zatwierdzonego snapshotu.

**Input SHA-256:** `d11afa3ea3e5d84aedf2550d1139e860076d95672a4d21da994336d58d0d686d`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-03` — Polish — `absent-answer-abstention`

**Purpose:** Tests calibrated abstention when the approved source does not provide the requested universal guarantee.

**Exact model scenario input:**

> Nowy Pod StatefulSet `orders-2` ma stan `Running`. Zespół chce wpisać do procedury operacyjnej dokładną, gwarantowaną przez Kubernetes v1.36.4 maksymalną liczbę sekund od utworzenia Poda, po której jego nazwa DNS musi już zawsze być rozwiązywalna.
>
> Na podstawie wyłącznie zatwierdzonego snapshotu odpowiedz, czy dokumentacja ustanawia taki uniwersalny maksymalny czas. Jeżeli nie ustanawia, powiedz to wprost zamiast zgadywać liczbę i wskaż, jakie zachowanie opisuje źródło. Podaj ścieżkę źródłową.

**Input SHA-256:** `886f8cb466f09b8e978fac2602803bf03bdcbaed1df6193e8d389710bafc5940`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-04` — Polish — `distractor-heavy-evidence`

**Purpose:** Tests selection of relevant facts while ignoring plausible but irrelevant details.

**Exact model scenario input:**

> W klastrze Kubernetes v1.36.4 zdefiniowano dwie PriorityClass:
>
> - `batch-high`: `value: 900`, `preemptionPolicy: Never`
> - `api-low`: `value: 100`
>
> Pod `report` używa `batch-high`, a Pod `api` używa `api-low`. Oba Pody mają ten sam `LOG_LEVEL`, podobne requests CPU, etykietę `team=payments` i są osiągalne przez różne Service. W klastrze chwilowo brakuje zasobów, aby zaplanować `report`.
>
> Czy `report` może przez samą swoją PriorityClass wywłaszczyć działający Pod `api`, aby zwolnić miejsce? Wyjaśnij, które podane informacje są istotne dla odpowiedzi, a które są dystraktorami. Wskaż ścieżkę źródłową.

**Input SHA-256:** `61d32a7d4a79dd3a4a2f482315ff08f87ff83136c00bd5bb1e72dcf9730f61f8`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-01` — English — `direct-evidence`

**Purpose:** Tests direct factual grounding against the frozen Kubernetes source snapshot.

**Exact model scenario input:**

> A Kubernetes v1.36.4 CronJob `nightly-report` uses `concurrencyPolicy: Forbid`. Its previous Job is still running when the next scheduled time arrives. Another unrelated CronJob also has a running Job.
>
> State what happens to the new `nightly-report` occurrence and whether `Forbid` prevents Jobs from the other CronJob from running concurrently. Cite the approved source path.

**Input SHA-256:** `b2df1948e85a1579975ea9b57f72791ccd64a12bd9e5b61b43de2bac2a2189ef`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-02` — English — `synthesis`

**Purpose:** Tests combining multiple documented facts without inventing missing behavior.

**Exact model scenario input:**

> A team is defining a Kubernetes v1.36.4 CronJob whose generated Jobs should retry work after a container failure. A draft Pod template uses `restartPolicy: Always`.
>
> Using the approved snapshot, synthesize the relationship between CronJob and Job for this case:
>
> - which object the CronJob creates for each occurrence;
> - which `restartPolicy` values are permitted in the Job's Pod template.
>
> Cite the relevant approved source paths.

**Input SHA-256:** `f46203f0eb9c7238a770005d8de7ceedd30e8d57e152928670f742e6f55a8ce4`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-03` — English — `absent-answer-abstention`

**Purpose:** Tests calibrated abstention when the approved source does not provide the requested universal guarantee.

**Exact model scenario input:**

> A Service selector in Kubernetes v1.36.4 has just been changed so that a different set of Pods matches it. An operations runbook needs a single exact maximum number of seconds, guaranteed by the approved documentation, within which the corresponding EndpointSlices must reflect the new matching Pod set.
>
> Determine whether the approved snapshot states such a universal numeric guarantee. If it does not, explicitly abstain from inventing one and summarize only what the source actually promises. Cite the source path.

**Input SHA-256:** `a4109d2ce0c94de90886c27e5926950d415342769f2bd6b96fcd43683cb159d7`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-04` — English — `distractor-heavy-evidence`

**Purpose:** Tests selection of relevant facts while ignoring plausible but irrelevant details.

**Exact model scenario input:**

> A Pod in Kubernetes v1.36.4 mounts key `settings.yaml` from ConfigMap `app-settings` using a volume mount with `subPath`. The ConfigMap is later updated. The Pod also has a Service on port 8080, label `tier=backend`, CPU request `250m`, and a readiness probe that is currently passing.
>
> Will the file mounted through `subPath` receive the ConfigMap update automatically? Identify which details determine the answer and which supplied details are distractors. Cite the approved source path.

**Input SHA-256:** `0d69ac1a6d3f1bda16cf71d388546954b0d5945f10e8cc43101520b2988b0ec3`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

## Procedural scenarios

### `dev-p-pl-01` — Polish — `diagnosis`

**Purpose:** Tests bounded diagnosis from supplied observations and a constrained next evidence-gathering step.

**Exact model scenario input:**

> Masz wyłącznie poniższe zapisane obserwacje z Poda `checkout-7f6d` w Kubernetes v1.36.4; nie wykonuj żadnych poleceń:
>
> `kubectl get pod checkout-7f6d` pokazuje `STATUS=Init:CrashLoopBackOff`.
>
> Fragment `kubectl describe pod checkout-7f6d`:
>
> - init container `prepare`: `State: Waiting`, `Reason: CrashLoopBackOff`
> - `Last State: Terminated`, `Reason: Error`, `Exit Code: 1`
> - główny kontener aplikacji nie został jeszcze uruchomiony.
>
> Zwróć wyłącznie JSON z kluczami:
> `stan`, `najlepsze_nastepne_sprawdzenie`, `polecenie_tylko_do_odczytu`, `uzasadnienie`.
>
> `polecenie_tylko_do_odczytu` ma zawierać dokładnie jedno polecenie `kubectl`, które według zatwierdzonego źródła najlepiej dostarczy danych o błędzie init containera. Nie proponuj naprawy ani mutacji klastra.

**Input SHA-256:** `a8634afc3e778b7296a64474dcce2a43d810f9e3129ca49bc4de2a515c60eaeb`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-pl-02` — Polish — `constrained-repair`

**Purpose:** Tests a minimal repair while preserving explicitly fixed parts of the artifact.

**Exact model scenario input:**

> Napraw minimalnie poniższy manifest nowego Deployment dla Kubernetes v1.36.4:
>
> ```yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: catalog
> spec:
>   replicas: 3
>   selector:
>     matchLabels:
>       app: catalog
>   template:
>     metadata:
>       labels:
>         app: catalog-v2
>         tier: backend
>     spec:
>       containers:
>         - name: catalog
>           image: registry.example/catalog:2.0
> ```
>
> Ograniczenia:
>
> - nie zmieniaj `apiVersion`, `kind`, `metadata.name`, `replicas`, obrazu kontenera ani `spec.selector`;
> - możesz zmienić wyłącznie `spec.template.metadata.labels`;
> - zachowaj etykietę `tier: backend`;
> - zwróć cały poprawiony YAML i nic więcej.

**Input SHA-256:** `56c2b53cddca6def3d0e5db483b2d0008206843f3401da75832e0d0ccedf64a3`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-pl-03` — Polish — `ordered-action`

**Purpose:** Tests an ordered, bounded operational procedure with explicit command constraints.

**Exact model scenario input:**

> Deployment `web` w Kubernetes v1.36.4 ma kontener `web` z obrazem `registry.example/web:1.4`. Trzeba przejść na `registry.example/web:1.5` i sprawdzić powodzenie wdrożenia.
>
> Podaj maksymalnie 5 uporządkowanych kroków z dokładnymi poleceniami `kubectl`, które:
>
> 1. zmienią wyłącznie obraz kontenera `web`,
> 2. będą obserwować status rolloutu,
> 3. zweryfikują obraz zapisany w Pod template,
> 4. w razie nieudanego rolloutu wskażą polecenie cofnięcia do poprzedniej rewizji.
>
> Nie wykonuj poleceń i nie dodawaj zmian niezwiązanych z obrazem.

**Input SHA-256:** `817ec96e8d4c5f7ae722b7f0cc181f53c0a27c0b1e17415a72c392091771a36b`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-pl-04` — Polish — `structured-artifact-schema-adherence`

**Purpose:** Tests generation of a valid Kubernetes artifact under explicit schema and output constraints.

**Exact model scenario input:**

> Utwórz kompletny manifest CronJob zgodny z Kubernetes v1.36.4 dla zadania `inventory-sync`.
>
> Wymagania:
>
> - `apiVersion: batch/v1`;
> - uruchamianie co 15 minut;
> - harmonogram interpretowany w `Etc/UTC` przez właściwe pole CronJob;
> - `concurrencyPolicy: Forbid`;
> - `startingDeadlineSeconds: 120`;
> - obraz `registry.example/inventory-sync:3.1`;
> - kontener ma nazywać się `sync`;
> - polecenie kontenera: `["/app/sync"]`;
> - `restartPolicy: Never`;
> - nie dodawaj pól niewymaganych przez zadanie.
>
> Zwróć wyłącznie jeden dokument YAML.

**Input SHA-256:** `aaba01e847f65e7eb43029f34f60179fbf53e9b1d85cc95f09641827dee7daed`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-01` — English — `diagnosis`

**Purpose:** Tests bounded diagnosis from supplied observations and a constrained next evidence-gathering step.

**Exact model scenario input:**

> Use only these captured observations for Kubernetes v1.36.4; do not execute anything:
>
> - Pod `api-6b7d` is `Running`.
> - Its liveness probe is succeeding.
> - Its readiness probe is failing.
> - The matching Service exists.
> - The Pod IP is absent from the Service's EndpointSlices.
>
> Return JSON with exactly these keys:
> `diagnosis`, `traffic_effect`, `next_check`, `read_only_command`.
>
> `read_only_command` must contain exactly one non-mutating `kubectl` command suitable for checking the readiness-related evidence. Do not propose a repair.

**Input SHA-256:** `a61b8e664ae1a424ebe2976979d723b6e17544aae0f80969eadb429f9b414b69`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-02` — English — `constrained-repair`

**Purpose:** Tests a minimal repair while preserving explicitly fixed parts of the artifact.

**Exact model scenario input:**

> A Pod in Kubernetes v1.36.4 is intended to read key `MODE` from ConfigMap `app-settings`, which exists in the same namespace. The manifest contains:
>
> ```yaml
> env:
>   - name: MODE
>     valueFrom:
>       configMapKeyRef:
>         name: app-setings
>         key: MODE
> ```
>
> Produce the smallest corrected YAML fragment under `env:`.
>
> Constraints:
>
> - only the `configMapKeyRef.name` value may change;
> - keep environment variable name `MODE`;
> - keep key `MODE`;
> - do not add optional fields;
> - output YAML only.

**Input SHA-256:** `2d96a329ce95d939671ea827b94b9168d0c3edb359ce9469a67cf92e5d238d29`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-03` — English — `ordered-action`

**Purpose:** Tests an ordered, bounded operational procedure with explicit command constraints.

**Exact model scenario input:**

> Deployment `worker` in Kubernetes v1.36.4 currently has 2 replicas and must be manually scaled to 5.
>
> Provide exactly three ordered, non-interactive `kubectl` commands:
>
> 1. set the replica count to 5;
> 2. read back the Deployment state;
> 3. list the Pods belonging to the workload using label `app=worker`.
>
> Do not change the Pod template, image, or any autoscaling resource. Do not execute the commands.

**Input SHA-256:** `88393f4f74b945e47b5af9430a17311b67a1634d3c60c3a4d7a4a5b32a31f7af`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-04` — English — `structured-artifact-schema-adherence`

**Purpose:** Tests generation of a valid Kubernetes artifact under explicit schema and output constraints.

**Exact model scenario input:**

> Write one complete Kubernetes v1.36.4 Job manifest named `shard-indexer`.
>
> Requirements:
>
> - `apiVersion: batch/v1`;
> - image `registry.example/indexer:4.0`;
> - container name `indexer`;
> - command `["/app/index"]`;
> - `completions: 4`;
> - `parallelism: 2`;
> - `completionMode: Indexed`;
> - Pod template `restartPolicy: Never`;
> - do not set a manual selector;
> - do not add unrelated fields.
>
> Return YAML only.

**Input SHA-256:** `560ecd9bb5fa3a2cd4f9e2e5b255be1b1e0c5637e3d9a9037acba46c12167b50`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

## Mixed scenarios

### `dev-m-pl-01` — Polish — `evidence-backed-configuration-decision`

**Purpose:** Tests a source-grounded technical decision plus a verifiable configuration artifact.

**Exact model scenario input:**

> Aplikacja w Kubernetes v1.36.4:
>
> - potrzebuje zwykle 75–100 sekund na start;
> - podczas startu endpoint `/healthz` może zwracać błąd, choć jest to stan oczekiwany;
> - po starcie chwilowe przeciążenie powinno wyłączyć Pod z ruchu, ale nie restartować kontenera;
> - trwałe zakleszczenie procesu powinno prowadzić do restartu.
>
> Podejmij decyzję, jak rozdzielić role między `startupProbe`, `readinessProbe` i `livenessProbe`, a następnie podaj przykładowy fragment `containers[].startupProbe/readinessProbe/livenessProbe` używający HTTP GET do `/healthz` na porcie `8080`. Parametry czasowe dobierz jawnie i krótko uzasadnij; nie zakładaj obserwacji z żywego klastra.
>
> Odpowiedź ma zawierać:
>
> 1. decyzję i uzasadnienie oparte na źródłach,
> 2. fragment YAML,
> 3. ścieżki źródłowe z zatwierdzonego snapshotu.

**Input SHA-256:** `bfaa6eb5e11e4c805baca3b4f38ea6d265d6f92f04cf2066d7f2876c27ea4894`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-02` — Polish — `evidence-backed-bounded-procedure`

**Purpose:** Tests a source-grounded diagnosis plus a bounded verification procedure.

**Exact model scenario input:**

> W Kubernetes v1.36.4 aplikacja działa bezpośrednio pod adresami IP Podów, ale Service `payments` nie zwraca odpowiedzi.
>
> Zapisane obserwacje:
>
> - Service istnieje i ma selector `app=payments`;
> - trzy zdrowe Pody mają etykietę `app=pay`;
> - bezpośredni test do portu aplikacji na IP Poda działa;
> - nie wolno teraz zmieniać żadnego obiektu.
>
> Na podstawie zatwierdzonej dokumentacji wskaż najbardziej uzasadnioną hipotezę konfiguracji i podaj maksymalnie 4 uporządkowane, tylko-do-odczytu kroki `kubectl`, które potwierdzą albo obalą tę hipotezę. Nie proponuj mutacji. Wskaż ścieżki źródłowe.

**Input SHA-256:** `4e32f0d0de7e633ff3c450fa701b05187609a1d8b61f16d55acd86bf1db6da04`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-03` — Polish — `evidence-backed-artifact-validation`

**Purpose:** Tests evidence-backed validation of an artifact followed by a minimal correction.

**Exact model scenario input:**

> Oceń poniższy fragment CronJob dla Kubernetes v1.36.4:
>
> ```yaml
> apiVersion: batch/v1
> kind: CronJob
> metadata:
>   name: billing
> spec:
>   schedule: "TZ=Europe/Warsaw 0 2 * * *"
>   jobTemplate:
>     spec:
>       template:
>         spec:
>           restartPolicy: Always
>           containers:
>             - name: billing
>               image: registry.example/billing:5.0
>               command: ["/app/bill"]
> ```
>
> Wymaganie biznesowe: uruchomienie codziennie o 02:00 w strefie `Europe/Warsaw`.
>
> Podaj:
>
> 1. werdykt, czy artefakt spełnia wymaganie i reguły v1.36.4;
> 2. listę wykrytych problemów popartą ścieżkami źródłowymi;
> 3. minimalnie poprawiony manifest YAML.
>
> Nie dodawaj innych funkcji CronJob.

**Input SHA-256:** `d56115ec70ff370cb5d1bb7fa9e94ba4f7a642623614eac15bf82fa22152a9c0`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-04` — Polish — `evidence-backed-repair-plan`

**Purpose:** Tests an evidence-grounded repair plan bounded by the stated constraints.

**Exact model scenario input:**

> Deployment `gateway` w Kubernetes v1.36.4 pobiera `FEATURE_MODE` z ConfigMap przez zmienną środowiskową. ConfigMap zmieniono, ale działające Pody nadal mają starą wartość. Obraz, liczba replik i pozostała konfiguracja mają pozostać bez zmian.
>
> Przygotuj plan naprawy, który:
>
> - wyjaśnia na podstawie źródła, dlaczego sama zmiana ConfigMap nie wystarczy dla zmiennej środowiskowej;
> - powoduje kontrolowane odtworzenie Podów przez zmianę wyłącznie metadanych Pod template Deployment;
> - podaje minimalny fragment YAML pokazujący taką zmianę;
> - zawiera krok weryfikacji rolloutu;
> - nie wykonuje żadnej operacji.
>
> Wskaż ścieżki źródłowe.

**Input SHA-256:** `bc39e796e0b62e1df2d93ff61009d4f1706d6773f187854446d2d668850258d7`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-01` — English — `evidence-backed-configuration-decision`

**Purpose:** Tests a source-grounded technical decision plus a verifiable configuration artifact.

**Exact model scenario input:**

> A Kubernetes v1.36.4 Deployment has 4 replicas labeled `app=checkout`. Eligible nodes are spread across three zones using node label `topology.kubernetes.io/zone`. The requirement is to keep matching Pods as evenly spread across zones as possible and refuse a new placement when it would make the skew greater than 1.
>
> Decide whether a Pod topology spread constraint is appropriate, then provide the minimal `spec.template.spec.topologySpreadConstraints` YAML fragment that expresses the requirement.
>
> Your response must:
>
> 1. justify the decision from the approved source;
> 2. preserve label matching on `app=checkout`;
> 3. use `maxSkew: 1`;
> 4. make the constraint hard rather than a soft preference;
> 5. cite approved source paths.

**Input SHA-256:** `bd1108fc89c76990c58c759f45bb0257749a31b09b3661d221b1d69a45efa586`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-02` — English — `evidence-backed-bounded-procedure`

**Purpose:** Tests a source-grounded diagnosis plus a bounded verification procedure.

**Exact model scenario input:**

> A Kubernetes v1.36.4 Deployment rollout has stopped making progress after a Pod-template change. No mutation is authorized yet.
>
> Prepare a bounded read-only investigation procedure of at most four `kubectl` commands that checks:
>
> - rollout status;
> - Deployment state and conditions;
> - the ReplicaSets created for the rollout;
> - the Pods and their current status.
>
> Explain briefly what each observation contributes before any repair decision is made. Cite the approved source paths. Do not execute commands and do not propose a mutation.

**Input SHA-256:** `a3c7465921ff340d9b8072495c3ee14f401014f645fe3769f9927750e4e64ce5`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-03` — English — `evidence-backed-artifact-validation`

**Purpose:** Tests evidence-backed validation of an artifact followed by a minimal correction.

**Exact model scenario input:**

> Validate this Kubernetes v1.36.4 container resource fragment:
>
> ```yaml
> resources:
>   requests:
>     cpu: "0.0005"
>     memory: "128Mi"
>   limits:
>     cpu: "500m"
>     memory: "256Mi"
> ```
>
> The workload owner needs the smallest change that makes the CPU request use a valid precision while preserving the intended very small request as closely as Kubernetes permits.
>
> Return:
>
> 1. a validity verdict and evidence-based reason;
> 2. the minimal corrected `resources` YAML fragment;
> 3. the approved source path.
>
> Do not change memory values or CPU limit.

**Input SHA-256:** `52825ccbe96adcf65cb2ff07b11e899b783beaf1af4248d7187db6e6ea414adf`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-04` — English — `evidence-backed-repair-plan`

**Purpose:** Tests an evidence-grounded repair plan bounded by the stated constraints.

**Exact model scenario input:**

> A Pod template in Kubernetes v1.36.4 is pending because the only currently suitable node has this taint:
>
> `dedicated=payments:NoSchedule`
>
> The workload is allowed to run on that node, but the repair must not force the Pod onto that node; it should only make the taint no longer exclude it. Other scheduler constraints must remain free to choose another node.
>
> Prepare an evidence-backed repair plan and the minimal Pod-template YAML fragment required for that goal. Explain why the change permits scheduling onto the tainted node without guaranteeing placement there. Cite the approved source path.

**Input SHA-256:** `d0350b038cdce939e25dd8eeebf39b450e53f48f6eac853b9c5f369d7991a721`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

## What happens after this review

Human approval of these candidate inputs authorizes only the next sequenced step: protected development-evaluator construction. It does not authorize formal experiments, final-test construction or access, training, live `kind`, live W1, outcome-selected C2, or unrestricted harness execution.

The final benchmark size and final family composition are deliberately **not fixed by this 24-item pilot**. They will be decided from the approved methodology and pilot evidence without consulting final-test outcomes.
