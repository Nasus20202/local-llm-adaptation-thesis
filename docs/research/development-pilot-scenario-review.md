# Development-pilot Scenario Human Review Catalog

## What this document is

This is the **primary human-review view for PR #44**. It lists all 24 development-pilot scenario inputs so the researcher does not need to inspect JSON.

These 24 families are **only the development pilot / feasibility sample**. They are not the final benchmark and they are not the final-test set. Pilot evidence is used to validate task solvability, evaluator behavior, headroom, feasibility, and the later study design. Additional family-disjoint material will be constructed later under separate gates, including any training material required by F1 and the eventual protected final-test set.

The pilot remains exactly 8 knowledge + 8 procedural + 8 mixed families, with 4 Polish + 4 English families in each class.

## What the model receives

For the base scenario export, the canonical scenario payload is **only `input_text`**. The surrounding JSON is repository governance and custody metadata, not prompt content.

The model is **not asked to reproduce citations, source paths, evidence IDs, or URLs**. Those identities remain evaluator/harness-side provenance. A later experimental condition may add only context or tools explicitly authorized by that condition contract.

**Model-facing custody is not the same thing as prompt-visible content.**

## How answers will be scored fairly

Open answers are judged by **meaning, not wording overlap**. The protected reference will encode required concepts, acceptable alternatives, unsupported/contradictory claims, constraints, and only construct-critical exact literals.

- A correct paraphrase receives the same credit as wording similar to Kubernetes documentation.
- Copying documentation verbatim receives **no bonus**.
- String similarity, token overlap, ROUGE/BLEU-like similarity, and edit distance do not contribute to the open-answer score.
- Exact matching is used only when an exact technical literal or explicit output format is itself part of the task.
- Ambiguous semantic equivalence is routed to the calibrated human rubric.
- Extra copied material can hurt only when it adds irrelevant, unsupported, contradictory, or incorrect claims.

## How to review

Review the scenario prose without consulting model outputs or protected answers. For each item, check:

- technical correctness and realism for Kubernetes v1.36.4;
- natural Polish or English wording;
- answerability (or intentional unanswerability for abstention);
- unambiguous constraints and response form;
- whether the item tests the stated capability rather than trivia;
- whether the wording is neutral across closed-book, prompting, fine-tuning, RAG, and combined conditions.

The exact scenario inputs below reflect the human-directed citation/source-reference correction. Updated SHA-256 values identify the revised prompt bytes.

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

**Purpose:** Tests direct technical correctness against the frozen Kubernetes version.

**Exact model scenario input:**

> W Kubernetes v1.36.4 kontener pobiera `LOG_LEVEL` z ConfigMap `app-settings` przez `env[].valueFrom.configMapKeyRef`. ConfigMap zmieniono z `info` na `debug`, ale proces w już działającym Podzie nadal widzi `info`.
>
> Odpowiedz zwięźle na dwa pytania:
>
> 1. Czy taka zmienna środowiskowa jest automatycznie aktualizowana w już uruchomionym kontenerze?
> 2. Co musi się stać z Podem, aby proces zobaczył nową wartość?

**Input SHA-256:** `d8824e1bd0dde581e0cc43d15c84d2251dc4c91298001ddb6ea1132c2abe5a42`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-02` — Polish — `synthesis`

**Purpose:** Tests combining multiple technical facts without inventing missing behavior.

**Exact model scenario input:**

> Aplikacja w Kubernetes v1.36.4 zwykle potrzebuje około 90 sekund na pełne uruchomienie. Podczas tego czasu endpoint aplikacji nie powinien powodować restartów kontenera, a Pod nie powinien jeszcze otrzymywać ruchu z Service. Po zakończeniu startu aplikacja może czasem chwilowo nie być gotowa do obsługi ruchu, ale nadal działa poprawnie.
>
> Wyjaśnij, jak role `startupProbe`, `livenessProbe` i `readinessProbe` powinny się uzupełniać w tym scenariuszu. Odpowiedź ma opisać:
>
> - co ma chronić długi start aplikacji,
> - co decyduje o kierowaniu ruchu,
> - co powinno wykrywać stan wymagający restartu.

**Input SHA-256:** `72c2b8cf9a2fe836643d6f510547d37cc01c220f3d7e88ae7c37c09e7579c167`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-03` — Polish — `absent-answer-abstention`

**Purpose:** Tests calibrated abstention when Kubernetes does not define the requested universal guarantee.

**Exact model scenario input:**

> Nowy Pod StatefulSet `orders-2` ma stan `Running`. Zespół chce wpisać do procedury operacyjnej dokładną, gwarantowaną przez Kubernetes v1.36.4 maksymalną liczbę sekund od utworzenia Poda, po której jego nazwa DNS musi już zawsze być rozwiązywalna.
>
> Odpowiedz, czy Kubernetes v1.36.4 ustanawia taki uniwersalny maksymalny czas. Jeżeli nie, powiedz to wprost zamiast zgadywać liczbę i opisz, jakie zachowanie można stwierdzić bez wymyślania gwarancji czasowej.

**Input SHA-256:** `ffac9af9e2e8f5eb3c7ad29c2fb9ee6ea286f1f1393498f68ee7d029f59628ed`

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
> Czy `report` może przez samą swoją PriorityClass wywłaszczyć działający Pod `api`, aby zwolnić miejsce? Wyjaśnij, które podane informacje są istotne dla odpowiedzi, a które są dystraktorami.

**Input SHA-256:** `8a16e7d5e082da798b0c14570ae9dbe3dc462a320b465d70265c7813126272d8`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-01` — English — `direct-evidence`

**Purpose:** Tests direct technical correctness against the frozen Kubernetes version.

**Exact model scenario input:**

> A Kubernetes v1.36.4 CronJob `nightly-report` uses `concurrencyPolicy: Forbid`. Its previous Job is still running when the next scheduled time arrives. Another unrelated CronJob also has a running Job.
>
> State what happens to the new `nightly-report` occurrence and whether `Forbid` prevents Jobs from the other CronJob from running concurrently.

**Input SHA-256:** `7afd1deae655b31eda368ba6aa6bc8b9f6f2f3bfcbeffcf31ef51453654e4aee`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-02` — English — `synthesis`

**Purpose:** Tests combining multiple technical facts without inventing missing behavior.

**Exact model scenario input:**

> A team is defining a Kubernetes v1.36.4 CronJob whose generated Jobs should retry work after a container failure. A draft Pod template uses `restartPolicy: Always`.
>
> Synthesize the relationship between CronJob and Job for this case:
>
> - which object the CronJob creates for each occurrence;
> - which `restartPolicy` values are permitted in the Job's Pod template.

**Input SHA-256:** `5a2e1f4673f3a844ecf7528798141c30d8a77a160e7c8c54c7c95b592bc37712`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-03` — English — `absent-answer-abstention`

**Purpose:** Tests calibrated abstention when Kubernetes does not define the requested universal guarantee.

**Exact model scenario input:**

> A Service selector in Kubernetes v1.36.4 has just been changed so that a different set of Pods matches it. An operations runbook needs a single exact maximum number of seconds, guaranteed by Kubernetes v1.36.4, within which the corresponding EndpointSlices must reflect the new matching Pod set.
>
> Determine whether Kubernetes v1.36.4 defines such a universal numeric guarantee. If it does not, explicitly abstain from inventing one and summarize the behavior that can be stated without inventing an SLA.

**Input SHA-256:** `b12c72e565b22f6cd7aa2a1a5afde747dd815cbd618d80a18b1c26d0d9972232`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-04` — English — `distractor-heavy-evidence`

**Purpose:** Tests selection of relevant facts while ignoring plausible but irrelevant details.

**Exact model scenario input:**

> A Pod in Kubernetes v1.36.4 mounts key `settings.yaml` from ConfigMap `app-settings` using a volume mount with `subPath`. The ConfigMap is later updated. The Pod also has a Service on port 8080, label `tier=backend`, CPU request `250m`, and a readiness probe that is currently passing.
>
> Will the file mounted through `subPath` receive the ConfigMap update automatically? Identify which details determine the answer and which supplied details are distractors.

**Input SHA-256:** `e85a2acbabff4ecaf766ca134c838fdd94453962e6c757c1f88161ea6dbacf72`

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
> `polecenie_tylko_do_odczytu` ma zawierać dokładnie jedno polecenie `kubectl`, które najlepiej dostarczy danych o błędzie init containera. Nie proponuj naprawy ani mutacji klastra.

**Input SHA-256:** `c9e57e5c525c31c9035b646e55e9f4a7c6d39db0c5dc1118add55d1e0dbf941a`

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

**Purpose:** Tests a technically justified decision plus a verifiable configuration artifact.

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
> 1. decyzję i krótkie techniczne uzasadnienie,
> 2. fragment YAML.

**Input SHA-256:** `a83256b1389f27edb35a01dd420e8b3387b98695163a3ff047b703dca5a53529`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-02` — Polish — `evidence-backed-bounded-procedure`

**Purpose:** Tests a technically justified diagnosis plus a bounded verification procedure.

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
> Wskaż najbardziej uzasadnioną hipotezę konfiguracji i podaj maksymalnie 4 uporządkowane, tylko-do-odczytu kroki `kubectl`, które potwierdzą albo obalą tę hipotezę. Nie proponuj mutacji.

**Input SHA-256:** `1fb96420ce4013e5efba52435814a6741d5e13baf92bfe3fe9e7c84311d69238`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-03` — Polish — `evidence-backed-artifact-validation`

**Purpose:** Tests technical validation of an artifact followed by a minimal correction.

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
> 2. listę wykrytych problemów z krótkim technicznym uzasadnieniem;
> 3. minimalnie poprawiony manifest YAML.
>
> Nie dodawaj innych funkcji CronJob.

**Input SHA-256:** `79236d780658dac4055c42fbc71f09e01bd41f703327d6464820940fc4178663`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-04` — Polish — `evidence-backed-repair-plan`

**Purpose:** Tests a technically justified repair plan bounded by the stated constraints.

**Exact model scenario input:**

> Deployment `gateway` w Kubernetes v1.36.4 pobiera `FEATURE_MODE` z ConfigMap przez zmienną środowiskową. ConfigMap zmieniono, ale działające Pody nadal mają starą wartość. Obraz, liczba replik i pozostała konfiguracja mają pozostać bez zmian.
>
> Przygotuj plan naprawy, który:
>
> - wyjaśnia, dlaczego sama zmiana ConfigMap nie wystarczy dla zmiennej środowiskowej;
> - powoduje kontrolowane odtworzenie Podów przez zmianę wyłącznie metadanych Pod template Deployment;
> - podaje minimalny fragment YAML pokazujący taką zmianę;
> - zawiera krok weryfikacji rolloutu;
> - nie wykonuje żadnej operacji.

**Input SHA-256:** `1b3a8ee20eddb5e604018e9a8a77ca8ed5734b6ab3bec90aabe8620466721165`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-01` — English — `evidence-backed-configuration-decision`

**Purpose:** Tests a technically justified decision plus a verifiable configuration artifact.

**Exact model scenario input:**

> A Kubernetes v1.36.4 Deployment has 4 replicas labeled `app=checkout`. Eligible nodes are spread across three zones using node label `topology.kubernetes.io/zone`. The requirement is to keep matching Pods as evenly spread across zones as possible and refuse a new placement when it would make the skew greater than 1.
>
> Decide whether a Pod topology spread constraint is appropriate, then provide the minimal `spec.template.spec.topologySpreadConstraints` YAML fragment that expresses the requirement.
>
> Your response must:
>
> 1. briefly justify the decision technically;
> 2. preserve label matching on `app=checkout`;
> 3. use `maxSkew: 1`;
> 4. make the constraint hard rather than a soft preference;

**Input SHA-256:** `fc5aa48b3cc9c7f7391f86527bf40655c984ba0ebc21ee8a3cb491092c1167da`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-02` — English — `evidence-backed-bounded-procedure`

**Purpose:** Tests a technically justified diagnosis plus a bounded verification procedure.

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
> Explain briefly what each observation contributes before any repair decision is made. Do not execute commands and do not propose a mutation.

**Input SHA-256:** `223220d0b05a101e9cd89abb4995bd2ce54604fc662689e9568f65f99ee945e9`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-03` — English — `evidence-backed-artifact-validation`

**Purpose:** Tests technical validation of an artifact followed by a minimal correction.

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
> 1. a validity verdict and technical reason;
> 2. the minimal corrected `resources` YAML fragment;
>
> Do not change memory values or CPU limit.

**Input SHA-256:** `7a4dfc3d96b19dbc28a3c9bb8c6eda721b58610d4b36d932dbdce48d6ceb4100`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-04` — English — `evidence-backed-repair-plan`

**Purpose:** Tests a technically justified repair plan bounded by the stated constraints.

**Exact model scenario input:**

> A Pod template in Kubernetes v1.36.4 is pending because the only currently suitable node has this taint:
>
> `dedicated=payments:NoSchedule`
>
> The workload is allowed to run on that node, but the repair must not force the Pod onto that node; it should only make the taint no longer exclude it. Other scheduler constraints must remain free to choose another node.
>
> Prepare a repair plan and the minimal Pod-template YAML fragment required for that goal. Explain why the change permits scheduling onto the tainted node without guaranteeing placement there.

**Input SHA-256:** `94ebb59c031cbdb5469e35af036f8be3f7a5c4860014f889a9602ef2bba00fa4`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

## What happens after this review

Human approval of these candidate inputs authorizes only the next sequenced step: protected development-evaluator construction. The protected evaluator will encode semantic atomic criteria and deterministic construct-critical checks without exposing answer-bearing material to the model.

The final benchmark size and final family composition are deliberately **not fixed by this 24-item pilot**. They will be decided from the approved methodology and pilot evidence without consulting final-test outcomes.
