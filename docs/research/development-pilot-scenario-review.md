# Development-pilot Scenario Review

This is the human review page for PR #44. The 24 scenarios are a development-pilot feasibility sample, not the final benchmark and not the final-test set.

**Reviewer-note boundary:** the one-sentence expected answers below are convenience notes for the human reviewer. They are **not goldens**, are not exhaustive scoring templates, and may omit other valid equivalent answers. They are not part of the evaluator's protected semantic contract and must not be supplied to models, RAG/search contexts, fine-tuning data, evaluator calibration inputs, or future final-test construction.

For how scoring works, see [Evaluation Strategy](evaluation.md). For terminology, see the [Glossary](../glossary.md). Source links point to the exact frozen Kubernetes snapshots used for this pilot.

## Review checklist

For each scenario check technical correctness for Kubernetes v1.36.4, natural language, answerability (or intentional abstention), realism, neutral treatment of compared methods, and whether the short reviewer note captures the intended technical answer without becoming a scoring template.

The model receives only the scenario's `input_text` plus context/tools explicitly authorized by an experimental condition. It is not asked to reproduce citations, repository paths, evidence IDs, or URLs.

## Knowledge

### `dev-k-pl-01` — Polish — `direct-evidence`

**Purpose:** Direct technical fact.

**Question — exact model input:**

<pre>
W Kubernetes v1.36.4 kontener pobiera `LOG_LEVEL` z ConfigMap `app-settings` przez `env[].valueFrom.configMapKeyRef`. ConfigMap zmieniono z `info` na `debug`, ale proces w już działającym Podzie nadal widzi `info`.

Odpowiedz zwięźle na dwa pytania:
1. Czy taka zmienna środowiskowa jest automatycznie aktualizowana w już uruchomionym kontenerze?
2. Co musi się stać z Podem, aby proces zobaczył nową wartość?
</pre>

**Expected answer — reviewer note:** Environment variables sourced from a ConfigMap are not refreshed inside an already running container; the Pod must be recreated or restarted so the container starts with the new value.

**Frozen sources:** [ConfigMap](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/configuration/configmap.md)

**Input SHA-256:** `d8824e1bd0dde581e0cc43d15c84d2251dc4c91298001ddb6ea1132c2abe5a42`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-02` — Polish — `synthesis`

**Purpose:** Combine several technical facts.

**Question — exact model input:**

<pre>
Aplikacja w Kubernetes v1.36.4 zwykle potrzebuje około 90 sekund na pełne uruchomienie. Podczas tego czasu endpoint aplikacji nie powinien powodować restartów kontenera, a Pod nie powinien jeszcze otrzymywać ruchu z Service. Po zakończeniu startu aplikacja może czasem chwilowo nie być gotowa do obsługi ruchu, ale nadal działa poprawnie.

Wyjaśnij, jak role `startupProbe`, `livenessProbe` i `readinessProbe` powinny się uzupełniać w tym scenariuszu. Odpowiedź ma opisać:
- co ma chronić długi start aplikacji,
- co decyduje o kierowaniu ruchu,
- co powinno wykrywać stan wymagający restartu.
</pre>

**Expected answer — reviewer note:** Use a startup probe to protect the long startup period, readiness to control whether the Pod receives Service traffic, and liveness to detect a persistently unhealthy container that should be restarted.

**Frozen sources:** [Pod probes](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/pods/probes.md) · [Configure probes task](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes.md)

**Input SHA-256:** `72c2b8cf9a2fe836643d6f510547d37cc01c220f3d7e88ae7c37c09e7579c167`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-03` — Polish — `absent-answer-abstention`

**Purpose:** Recognize when the source does not justify a precise answer.

**Question — exact model input:**

<pre>
Nowy Pod StatefulSet `orders-2` ma stan `Running`. Zespół chce wpisać do procedury operacyjnej dokładną, gwarantowaną przez Kubernetes v1.36.4 maksymalną liczbę sekund od utworzenia Poda, po której jego nazwa DNS musi już zawsze być rozwiązywalna.

Odpowiedz, czy Kubernetes v1.36.4 ustanawia taki uniwersalny maksymalny czas. Jeżeli nie, powiedz to wprost zamiast zgadywać liczbę i opisz, jakie zachowanie można stwierdzić bez wymyślania gwarancji czasowej.
</pre>

**Expected answer — reviewer note:** Kubernetes does not define one universal maximum DNS-propagation time for this case, so the correct answer is to refuse a numeric guarantee and describe the documented StatefulSet/DNS behavior instead.

**Frozen sources:** [StatefulSet](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/statefulset.md)

**Input SHA-256:** `ffac9af9e2e8f5eb3c7ad29c2fb9ee6ea286f1f1393498f68ee7d029f59628ed`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-pl-04` — Polish — `distractor-heavy-evidence`

**Purpose:** Separate relevant facts from distractors.

**Question — exact model input:**

<pre>
W klastrze Kubernetes v1.36.4 zdefiniowano dwie PriorityClass:

- `batch-high`: `value: 900`, `preemptionPolicy: Never`
- `api-low`: `value: 100`

Pod `report` używa `batch-high`, a Pod `api` używa `api-low`. Oba Pody mają ten sam `LOG_LEVEL`, podobne requests CPU, etykietę `team=payments` i są osiągalne przez różne Service. W klastrze chwilowo brakuje zasobów, aby zaplanować `report`.

Czy `report` może przez samą swoją PriorityClass wywłaszczyć działający Pod `api`, aby zwolnić miejsce? Wyjaśnij, które podane informacje są istotne dla odpowiedzi, a które są dystraktorami.
</pre>

**Expected answer — reviewer note:** No: `preemptionPolicy: Never` prevents `report` from preempting lower-priority Pods; the priority/preemption settings and resource shortage matter, while the ConfigMap, Service and unrelated labels do not.

**Frozen sources:** [Pod priority and preemption](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/scheduling-eviction/pod-priority-preemption.md)

**Input SHA-256:** `8a16e7d5e082da798b0c14570ae9dbe3dc462a320b465d70265c7813126272d8`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-01` — English — `direct-evidence`

**Purpose:** Direct technical fact.

**Question — exact model input:**

<pre>
A Kubernetes v1.36.4 CronJob `nightly-report` uses `concurrencyPolicy: Forbid`. Its previous Job is still running when the next scheduled time arrives. Another unrelated CronJob also has a running Job.

State what happens to the new `nightly-report` occurrence and whether `Forbid` prevents Jobs from the other CronJob from running concurrently.
</pre>

**Expected answer — reviewer note:** `Forbid` skips the new occurrence when a previous Job from the same CronJob is still running, but it does not block Jobs created by other CronJobs.

**Frozen sources:** [CronJob](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/cron-jobs.md)

**Input SHA-256:** `7afd1deae655b31eda368ba6aa6bc8b9f6f2f3bfcbeffcf31ef51453654e4aee`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-02` — English — `synthesis`

**Purpose:** Combine several technical facts.

**Question — exact model input:**

<pre>
A team is defining a Kubernetes v1.36.4 CronJob whose generated Jobs should retry work after a container failure. A draft Pod template uses `restartPolicy: Always`.

Synthesize the relationship between CronJob and Job for this case:
- which object the CronJob creates for each occurrence;
- which `restartPolicy` values are permitted in the Job&#x27;s Pod template.
</pre>

**Expected answer — reviewer note:** A CronJob creates a Job for each occurrence, and a Job Pod template may use `restartPolicy: Never` or `OnFailure`, not `Always`.

**Frozen sources:** [CronJob](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/cron-jobs.md) · [Job](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/job.md)

**Input SHA-256:** `5a2e1f4673f3a844ecf7528798141c30d8a77a160e7c8c54c7c95b592bc37712`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-03` — English — `absent-answer-abstention`

**Purpose:** Recognize when the source does not justify a precise answer.

**Question — exact model input:**

<pre>
A Service selector in Kubernetes v1.36.4 has just been changed so that a different set of Pods matches it. An operations runbook needs a single exact maximum number of seconds, guaranteed by Kubernetes v1.36.4, within which the corresponding EndpointSlices must reflect the new matching Pod set.

Determine whether Kubernetes v1.36.4 defines such a universal numeric guarantee. If it does not, explicitly abstain from inventing one and summarize the behavior that can be stated without inventing an SLA.
</pre>

**Expected answer — reviewer note:** Kubernetes does not publish one universal guaranteed maximum for EndpointSlice reconciliation after a selector change, so a numeric SLA must not be invented.

**Frozen sources:** [Service and EndpointSlices](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/services-networking/service.md)

**Input SHA-256:** `b12c72e565b22f6cd7aa2a1a5afde747dd815cbd618d80a18b1c26d0d9972232`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-k-en-04` — English — `distractor-heavy-evidence`

**Purpose:** Separate relevant facts from distractors.

**Question — exact model input:**

<pre>
A Pod in Kubernetes v1.36.4 mounts key `settings.yaml` from ConfigMap `app-settings` using a volume mount with `subPath`. The ConfigMap is later updated. The Pod also has a Service on port 8080, label `tier=backend`, CPU request `250m`, and a readiness probe that is currently passing.

Will the file mounted through `subPath` receive the ConfigMap update automatically? Identify which details determine the answer and which supplied details are distractors.
</pre>

**Expected answer — reviewer note:** No: a ConfigMap file mounted with `subPath` does not receive later ConfigMap updates automatically; the Service, label, CPU request and readiness state are distractors.

**Frozen sources:** [ConfigMap](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/configuration/configmap.md)

**Input SHA-256:** `e85a2acbabff4ecaf766ca134c838fdd94453962e6c757c1f88161ea6dbacf72`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

## Procedural

### `dev-p-pl-01` — Polish — `diagnosis`

**Purpose:** Diagnose from bounded observations.

**Question — exact model input:**

<pre>
Masz wyłącznie poniższe zapisane obserwacje z Poda `checkout-7f6d` w Kubernetes v1.36.4; nie wykonuj żadnych poleceń:

`kubectl get pod checkout-7f6d` pokazuje `STATUS=Init:CrashLoopBackOff`.

Fragment `kubectl describe pod checkout-7f6d`:
- init container `prepare`: `State: Waiting`, `Reason: CrashLoopBackOff`
- `Last State: Terminated`, `Reason: Error`, `Exit Code: 1`
- główny kontener aplikacji nie został jeszcze uruchomiony.

Zwróć wyłącznie JSON z kluczami:
`stan`, `najlepsze_nastepne_sprawdzenie`, `polecenie_tylko_do_odczytu`, `uzasadnienie`.

`polecenie_tylko_do_odczytu` ma zawierać dokładnie jedno polecenie `kubectl`, które najlepiej dostarczy danych o błędzie init containera. Nie proponuj naprawy ani mutacji klastra.
</pre>

**Expected answer — reviewer note:** The init container `prepare` is repeatedly failing before the application container can start; the best next read-only check is its previous logs, for example `kubectl logs checkout-7f6d -c prepare --previous`.

**Frozen sources:** [Debug init containers](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/debug/debug-application/debug-init-containers.md)

**Input SHA-256:** `c9e57e5c525c31c9035b646e55e9f4a7c6d39db0c5dc1118add55d1e0dbf941a`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-pl-02` — Polish — `constrained-repair`

**Purpose:** Make the smallest permitted repair.

**Question — exact model input:**

<pre>
Napraw minimalnie poniższy manifest nowego Deployment dla Kubernetes v1.36.4:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: catalog
spec:
  replicas: 3
  selector:
    matchLabels:
      app: catalog
  template:
    metadata:
      labels:
        app: catalog-v2
        tier: backend
    spec:
      containers:
      - name: catalog
        image: registry.example/catalog:2.0
```

Ograniczenia:
- nie zmieniaj `apiVersion`, `kind`, `metadata.name`, `replicas`, obrazu kontenera ani `spec.selector`;
- możesz zmienić wyłącznie `spec.template.metadata.labels`;
- zachowaj etykietę `tier: backend`;
- zwróć cały poprawiony YAML i nic więcej.
</pre>

**Expected answer — reviewer note:** Change only the Pod-template label from `app: catalog-v2` to `app: catalog` and keep `tier: backend`, so the immutable Deployment selector matches the template labels.

**Frozen sources:** [Deployment](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/deployment.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `56c2b53cddca6def3d0e5db483b2d0008206843f3401da75832e0d0ccedf64a3`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-pl-03` — Polish — `ordered-action`

**Purpose:** Produce a safe bounded action sequence.

**Question — exact model input:**

<pre>
Deployment `web` w Kubernetes v1.36.4 ma kontener `web` z obrazem `registry.example/web:1.4`. Trzeba przejść na `registry.example/web:1.5` i sprawdzić powodzenie wdrożenia.

Podaj maksymalnie 5 uporządkowanych kroków z dokładnymi poleceniami `kubectl`, które:
1. zmienią wyłącznie obraz kontenera `web`,
2. będą obserwować status rolloutu,
3. zweryfikują obraz zapisany w Pod template,
4. w razie nieudanego rolloutu wskażą polecenie cofnięcia do poprzedniej rewizji.

Nie wykonuj poleceń i nie dodawaj zmian niezwiązanych z obrazem.
</pre>

**Expected answer — reviewer note:** Update only the image with `kubectl set image`, monitor with `kubectl rollout status`, read back the Pod-template image, and use `kubectl rollout undo deployment/web` only if the rollout fails.

**Frozen sources:** [Rolling update](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/run-application/update-deployment-rolling.md) · [Deployment](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/deployment.md)

**Input SHA-256:** `817ec96e8d4c5f7ae722b7f0cc181f53c0a27c0b1e17415a72c392091771a36b`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-pl-04` — Polish — `structured-artifact-schema-adherence`

**Purpose:** Produce a valid constrained Kubernetes artifact.

**Question — exact model input:**

<pre>
Utwórz kompletny manifest CronJob zgodny z Kubernetes v1.36.4 dla zadania `inventory-sync`.

Wymagania:
- `apiVersion: batch/v1`;
- uruchamianie co 15 minut;
- harmonogram interpretowany w `Etc/UTC` przez właściwe pole CronJob;
- `concurrencyPolicy: Forbid`;
- `startingDeadlineSeconds: 120`;
- obraz `registry.example/inventory-sync:3.1`;
- kontener ma nazywać się `sync`;
- polecenie kontenera: `[&quot;/app/sync&quot;]`;
- `restartPolicy: Never`;
- nie dodawaj pól niewymaganych przez zadanie.

Zwróć wyłącznie jeden dokument YAML.
</pre>

**Expected answer — reviewer note:** The manifest should use `schedule: "*/15 * * * *"`, `timeZone: Etc/UTC`, `concurrencyPolicy: Forbid`, `startingDeadlineSeconds: 120`, the requested container/image/command, and `restartPolicy: Never`.

**Frozen sources:** [CronJob](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/cron-jobs.md) · [Job](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/job.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `aaba01e847f65e7eb43029f34f60179fbf53e9b1d85cc95f09641827dee7daed`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-01` — English — `diagnosis`

**Purpose:** Diagnose from bounded observations.

**Question — exact model input:**

<pre>
Use only these captured observations for Kubernetes v1.36.4; do not execute anything:

- Pod `api-6b7d` is `Running`.
- Its liveness probe is succeeding.
- Its readiness probe is failing.
- The matching Service exists.
- The Pod IP is absent from the Service&#x27;s EndpointSlices.

Return JSON with exactly these keys:
`diagnosis`, `traffic_effect`, `next_check`, `read_only_command`.

`read_only_command` must contain exactly one non-mutating `kubectl` command suitable for checking the readiness-related evidence. Do not propose a repair.
</pre>

**Expected answer — reviewer note:** The Pod is alive but unready, so it should keep running while being excluded from Service traffic; inspect readiness-related Pod state/events with one read-only command such as `kubectl describe pod api-6b7d`.

**Frozen sources:** [Pod probes](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/pods/probes.md) · [Service and EndpointSlices](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/services-networking/service.md) · [Debug Services](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/debug/debug-application/debug-service.md)

**Input SHA-256:** `a61b8e664ae1a424ebe2976979d723b6e17544aae0f80969eadb429f9b414b69`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-02` — English — `constrained-repair`

**Purpose:** Make the smallest permitted repair.

**Question — exact model input:**

<pre>
A Pod in Kubernetes v1.36.4 is intended to read key `MODE` from ConfigMap `app-settings`, which exists in the same namespace. The manifest contains:

```yaml
env:
- name: MODE
  valueFrom:
    configMapKeyRef:
      name: app-setings
      key: MODE
```

Produce the smallest corrected YAML fragment under `env:`.

Constraints:
- only the `configMapKeyRef.name` value may change;
- keep environment variable name `MODE`;
- keep key `MODE`;
- do not add optional fields;
- output YAML only.
</pre>

**Expected answer — reviewer note:** The minimal repair is changing only `configMapKeyRef.name` from `app-setings` to `app-settings`.

**Frozen sources:** [ConfigMap](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/configuration/configmap.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `2d96a329ce95d939671ea827b94b9168d0c3edb359ce9469a67cf92e5d238d29`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-03` — English — `ordered-action`

**Purpose:** Produce a safe bounded action sequence.

**Question — exact model input:**

<pre>
Deployment `worker` in Kubernetes v1.36.4 currently has 2 replicas and must be manually scaled to 5.

Provide exactly three ordered, non-interactive `kubectl` commands:
1. set the replica count to 5;
2. read back the Deployment state;
3. list the Pods belonging to the workload using label `app=worker`.

Do not change the Pod template, image, or any autoscaling resource. Do not execute the commands.
</pre>

**Expected answer — reviewer note:** Use exactly three commands: scale the Deployment to 5 replicas, read back the Deployment, then list Pods with `-l app=worker`.

**Frozen sources:** [Scale a Deployment](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/run-application/scale-deployment.md)

**Input SHA-256:** `88393f4f74b945e47b5af9430a17311b67a1634d3c60c3a4d7a4a5b32a31f7af`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-p-en-04` — English — `structured-artifact-schema-adherence`

**Purpose:** Produce a valid constrained Kubernetes artifact.

**Question — exact model input:**

<pre>
Write one complete Kubernetes v1.36.4 Job manifest named `shard-indexer`.

Requirements:
- `apiVersion: batch/v1`;
- image `registry.example/indexer:4.0`;
- container name `indexer`;
- command `[&quot;/app/index&quot;]`;
- `completions: 4`;
- `parallelism: 2`;
- `completionMode: Indexed`;
- Pod template `restartPolicy: Never`;
- do not set a manual selector;
- do not add unrelated fields.

Return YAML only.
</pre>

**Expected answer — reviewer note:** Return one Job using `batch/v1` with the requested container, `completions: 4`, `parallelism: 2`, `completionMode: Indexed`, `restartPolicy: Never`, and no manual selector.

**Frozen sources:** [Job](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/job.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `560ecd9bb5fa3a2cd4f9e2e5b255be1b1e0c5637e3d9a9037acba46c12167b50`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

## Mixed

### `dev-m-pl-01` — Polish — `evidence-backed-configuration-decision`

**Purpose:** Make and justify a configuration decision.

**Question — exact model input:**

<pre>
Aplikacja w Kubernetes v1.36.4:
- potrzebuje zwykle 75–100 sekund na start;
- podczas startu endpoint `/healthz` może zwracać błąd, choć jest to stan oczekiwany;
- po starcie chwilowe przeciążenie powinno wyłączyć Pod z ruchu, ale nie restartować kontenera;
- trwałe zakleszczenie procesu powinno prowadzić do restartu.

Podejmij decyzję, jak rozdzielić role między `startupProbe`, `readinessProbe` i `livenessProbe`, a następnie podaj przykładowy fragment `containers[].startupProbe/readinessProbe/livenessProbe` używający HTTP GET do `/healthz` na porcie `8080`. Parametry czasowe dobierz jawnie i krótko uzasadnij; nie zakładaj obserwacji z żywego klastra.

Odpowiedź ma zawierać:
1. decyzję i krótkie techniczne uzasadnienie,
2. fragment YAML.
</pre>

**Expected answer — reviewer note:** The startup probe should cover the expected 75–100 s startup window, readiness should remove an overloaded Pod from traffic without restart, and liveness should detect a lasting deadlock; the YAML should express those three separate roles.

**Frozen sources:** [Pod probes](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/pods/probes.md) · [Configure probes task](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `a83256b1389f27edb35a01dd420e8b3387b98695163a3ff047b703dca5a53529`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-02` — Polish — `evidence-backed-bounded-procedure`

**Purpose:** Build a bounded diagnostic procedure.

**Question — exact model input:**

<pre>
W Kubernetes v1.36.4 aplikacja działa bezpośrednio pod adresami IP Podów, ale Service `payments` nie zwraca odpowiedzi.

Zapisane obserwacje:
- Service istnieje i ma selector `app=payments`;
- trzy zdrowe Pody mają etykietę `app=pay`;
- bezpośredni test do portu aplikacji na IP Poda działa;
- nie wolno teraz zmieniać żadnego obiektu.

Wskaż najbardziej uzasadnioną hipotezę konfiguracji i podaj maksymalnie 4 uporządkowane, tylko-do-odczytu kroki `kubectl`, które potwierdzą albo obalą tę hipotezę. Nie proponuj mutacji.
</pre>

**Expected answer — reviewer note:** The strongest hypothesis is a selector mismatch (`app=payments` versus Pod label `app=pay`); read-only checks should confirm the Service selector, Pod labels and resulting EndpointSlices before any mutation.

**Frozen sources:** [Service and EndpointSlices](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/services-networking/service.md) · [Debug Services](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/debug/debug-application/debug-service.md)

**Input SHA-256:** `1fb96420ce4013e5efba52435814a6741d5e13baf92bfe3fe9e7c84311d69238`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-03` — Polish — `evidence-backed-artifact-validation`

**Purpose:** Validate and minimally repair an artifact.

**Question — exact model input:**

<pre>
Oceń poniższy fragment CronJob dla Kubernetes v1.36.4:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: billing
spec:
  schedule: &quot;TZ=Europe/Warsaw 0 2 * * *&quot;
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Always
          containers:
          - name: billing
            image: registry.example/billing:5.0
            command: [&quot;/app/bill&quot;]
```

Wymaganie biznesowe: uruchomienie codziennie o 02:00 w strefie `Europe/Warsaw`.

Podaj:
1. werdykt, czy artefakt spełnia wymaganie i reguły v1.36.4;
2. listę wykrytych problemów z krótkim technicznym uzasadnieniem;
3. minimalnie poprawiony manifest YAML.

Nie dodawaj innych funkcji CronJob.
</pre>

**Expected answer — reviewer note:** The manifest is invalid because the time zone belongs in `.spec.timeZone` rather than inside `schedule`, and a Job Pod cannot use `restartPolicy: Always`; use `schedule: "0 2 * * *"`, `timeZone: Europe/Warsaw`, and a valid Job restart policy (`Never` or `OnFailure`).

**Frozen sources:** [CronJob](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/cron-jobs.md) · [Job](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/job.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `79236d780658dac4055c42fbc71f09e01bd41f703327d6464820940fc4178663`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-pl-04` — Polish — `evidence-backed-repair-plan`

**Purpose:** Explain and plan a bounded repair.

**Question — exact model input:**

<pre>
Deployment `gateway` w Kubernetes v1.36.4 pobiera `FEATURE_MODE` z ConfigMap przez zmienną środowiskową. ConfigMap zmieniono, ale działające Pody nadal mają starą wartość. Obraz, liczba replik i pozostała konfiguracja mają pozostać bez zmian.

Przygotuj plan naprawy, który:
- wyjaśnia, dlaczego sama zmiana ConfigMap nie wystarczy dla zmiennej środowiskowej;
- powoduje kontrolowane odtworzenie Podów przez zmianę wyłącznie metadanych Pod template Deployment;
- podaje minimalny fragment YAML pokazujący taką zmianę;
- zawiera krok weryfikacji rolloutu;
- nie wykonuje żadnej operacji.
</pre>

**Expected answer — reviewer note:** Changing a ConfigMap does not refresh an environment variable in existing Pods; change only Deployment Pod-template metadata (for example an annotation) to trigger a controlled rollout, then verify rollout completion.

**Frozen sources:** [ConfigMap](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/configuration/configmap.md) · [Deployment](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/deployment.md) · [Rolling update](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/run-application/update-deployment-rolling.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `1b3a8ee20eddb5e604018e9a8a77ca8ed5734b6ab3bec90aabe8620466721165`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-01` — English — `evidence-backed-configuration-decision`

**Purpose:** Make and justify a configuration decision.

**Question — exact model input:**

<pre>
A Kubernetes v1.36.4 Deployment has 4 replicas labeled `app=checkout`. Eligible nodes are spread across three zones using node label `topology.kubernetes.io/zone`. The requirement is to keep matching Pods as evenly spread across zones as possible and refuse a new placement when it would make the skew greater than 1.

Decide whether a Pod topology spread constraint is appropriate, then provide the minimal `spec.template.spec.topologySpreadConstraints` YAML fragment that expresses the requirement.

Your response must:
1. briefly justify the decision technically;
2. preserve label matching on `app=checkout`;
3. use `maxSkew: 1`;
4. make the constraint hard rather than a soft preference;
</pre>

**Expected answer — reviewer note:** A hard topology-spread constraint is appropriate: use `topology.kubernetes.io/zone`, `maxSkew: 1`, `whenUnsatisfiable: DoNotSchedule`, and a selector matching `app=checkout`.

**Frozen sources:** [Topology spread constraints](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/scheduling-eviction/topology-spread-constraints.md) · [Deployment](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/deployment.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `fc5aa48b3cc9c7f7391f86527bf40655c984ba0ebc21ee8a3cb491092c1167da`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-02` — English — `evidence-backed-bounded-procedure`

**Purpose:** Build a bounded diagnostic procedure.

**Question — exact model input:**

<pre>
A Kubernetes v1.36.4 Deployment rollout has stopped making progress after a Pod-template change. No mutation is authorized yet.

Prepare a bounded read-only investigation procedure of at most four `kubectl` commands that checks:
- rollout status;
- Deployment state and conditions;
- the ReplicaSets created for the rollout;
- the Pods and their current status.

Explain briefly what each observation contributes before any repair decision is made. Do not execute commands and do not propose a mutation.
</pre>

**Expected answer — reviewer note:** Use at most four read-only checks covering rollout status, Deployment conditions, ReplicaSets and Pods, and make no repair until those observations identify the failure mode.

**Frozen sources:** [Deployment](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/workloads/controllers/deployment.md) · [Rolling update](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/tasks/run-application/update-deployment-rolling.md)

**Input SHA-256:** `223220d0b05a101e9cd89abb4995bd2ce54604fc662689e9568f65f99ee945e9`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-03` — English — `evidence-backed-artifact-validation`

**Purpose:** Validate and minimally repair an artifact.

**Question — exact model input:**

<pre>
Validate this Kubernetes v1.36.4 container resource fragment:

```yaml
resources:
  requests:
    cpu: &quot;0.0005&quot;
    memory: &quot;128Mi&quot;
  limits:
    cpu: &quot;500m&quot;
    memory: &quot;256Mi&quot;
```

The workload owner needs the smallest change that makes the CPU request use a valid precision while preserving the intended very small request as closely as Kubernetes permits.

Return:
1. a validity verdict and technical reason;
2. the minimal corrected `resources` YAML fragment;

Do not change memory values or CPU limit.
</pre>

**Expected answer — reviewer note:** `0.0005` CPU has precision finer than 1m and is invalid; the nearest valid small request is `1m` (equivalently `0.001`) while all other resource values stay unchanged.

**Frozen sources:** [Container resources](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/configuration/manage-resources-containers.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `7a4dfc3d96b19dbc28a3c9bb8c6eda721b58610d4b36d932dbdce48d6ceb4100`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

### `dev-m-en-04` — English — `evidence-backed-repair-plan`

**Purpose:** Explain and plan a bounded repair.

**Question — exact model input:**

<pre>
A Pod template in Kubernetes v1.36.4 is pending because the only currently suitable node has this taint:

`dedicated=payments:NoSchedule`

The workload is allowed to run on that node, but the repair must not force the Pod onto that node; it should only make the taint no longer exclude it. Other scheduler constraints must remain free to choose another node.

Prepare a repair plan and the minimal Pod-template YAML fragment required for that goal. Explain why the change permits scheduling onto the tainted node without guaranteeing placement there.
</pre>

**Expected answer — reviewer note:** Add a toleration matching `dedicated=payments:NoSchedule`; it removes that taint as an exclusion but does not select or force the Pod onto the node.

**Frozen sources:** [Taints and tolerations](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/content/en/docs/concepts/scheduling-eviction/taint-and-toleration.md) · [Kubernetes OpenAPI snapshot](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/api/openapi-spec/swagger.json)

**Input SHA-256:** `94ebb59c031cbdb5469e35af036f8be3f7a5c4860014f889a9602ef2bba00fa4`

**Human review:** ☐ approve as written · ☐ revise · ☐ reject

## After approval

Approval of these inputs authorizes only the later construction of protected development-evaluator material. It does not authorize formal model experiments, final-test construction, training-data construction, live `kind`/web execution, or outcome-selected combined conditions.
