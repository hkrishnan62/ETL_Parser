---
title: 'Automated Conversion of ETL Mapping Documents into SQL Validation Queries'
tags:
  - Python
  - ETL testing
  - data validation
  - data pipelines
  - SQL generation
  - CI/CD
  - data engineering
authors:
  - name: Manu Prasad Prakash Bhavan Siva Prasad
    orcid: 0009-0009-5914-3392
    corresponding: true
    affiliation: 1
affiliations:
  - name: Independent Researcher, USA
    index: 1
date: 4 May 2026
bibliography: paper.bib
---

# Summary

Testing ETL (Extract-Transform-Load) pipelines is a critical yet error-prone activity in data engineering, as validation logic is commonly derived manually from source-to-target mapping documents such as Excel crosswalks. Manual translation of these mappings into SQL validation queries is time-consuming, inconsistent, and difficult to scale for large data warehouse or migration projects. We present an open-source, Python-based **Mapping-to-SQL Converter** that systematically transforms structured mapping documents into executable SQL validation queries, enabling faster test generation, consistent application of transformation rules, and scalable validation across large mapping sets.

The tool ingests CSV or Excel mapping specifications containing source/target columns, transformation rules, and key indicators. A Pandas-based parser builds an internal representation, and an SQL generator emits Common Table Expression (CTE)-based queries that perform bidirectional source-minus-target and target-minus-source comparisons using the `EXCEPT` operator. Both an aggregate-mismatch summary and a sample of discrepant rows are produced for each mapping. The system is exposed through a Flask web UI for interactive use and a CLI for batch and CI/CD integration, and is distributed under the MIT licence. The wider repository also includes optional AI-assisted authoring helpers, a browser-based SQL playground, and automated test-case generation utilities; this paper evaluates the core deterministic mapping-to-SQL conversion engine that underpins those workflows.

# Statement of need

Mapping documents are the authoritative specification of how each target field is derived from source fields, including any transformations applied [@Hames:2016]. Despite this, ETL validation has long depended on manually hand-crafting two SQL statements per mapping — one to project the transformed source, one to read the target — and comparing them via `EXCEPT` or `MINUS`. This pattern is brittle, error-prone, and impossible to scale: industry data show that a typical mapping requires roughly one hour of manual SQL coding, so a project with 1,000 mappings would consume approximately 1,000 person-hours [@QuerySurge:2024]. @Dakrory:2015 demonstrate that automated ETL testing produces superior data quality at lower cost than manual approaches, and 68% of surveyed data warehouses contain more than 250 mappings each [@QuerySurge:2024]. The gap between mapping-document authoring and SQL test creation is therefore a primary bottleneck in modern data engineering — one that automated, structured conversion is well-suited to close.

# State of the field

Commercial offerings such as QuerySurge (RTTS) embed mapping-to-SQL generation inside proprietary, license-gated platforms with AI-based "Mapping Intelligence" features [@QuerySurge:2024]. Other commercial tools such as Informatica and the open-source Talend require users to author tests manually rather than generating them from mapping artefacts. A growing body of work uses LLMs to translate natural-language descriptions into SQL — for example, the PromptQL approach reports approximately 40% prototype-development speedups [@Singamsetty:2025; @Radford:2024] — but these systems consume free-form prose rather than the structured spreadsheet mappings that QA teams already maintain. On the academic side, @Mahmoud:2015 develop an automated ETL testing framework focused on data-quality detection, and @Zhang:2022 report industrial experience showing that automated test harnesses detect ETL errors faster than human reviewers, but neither addresses mapping-to-SQL translation directly.

**Build vs. contribute.** No existing tool combines the four properties this work targets simultaneously: (i) open-source and MIT-licensed, (ii) deterministic and not LLM-dependent, (iii) operating directly on the structured spreadsheet mappings already produced by QA teams, and (iv) deployable as both a web service and a CLI for CI/CD pipelines. Extending a closed commercial platform was not possible; extending an LLM-based prompt translator would require asking teams to abandon their existing mapping documents. We therefore built a focused tool that complements rather than displaces existing assets.

# Software design

The system is organised as two modules behind a thin interface layer. The **Mapping Parser** (`mapping_parser.py`) reads a CSV or Excel mapping into a Pandas DataFrame, validates the required structural columns (`source_column`, `target_column`) plus optional `transformation` and `is_key` fields, defaults missing transformations to direct source-to-target copies when possible, and identifies join keys via the `is_key` flag. The **SQL Generator** (`sql_generator.py`) consumes the parsed mappings and the user-supplied source/target table names and emits a `WITH source_transformed AS (…)` CTE in which each row's transformation expression is aliased to its target column name. From the CTE the generator produces two set-difference queries (Source-minus-Target and Target-minus-Source), each wrapped to return both a mismatch count and a sample of discrepant rows via `UNION ALL`. A commented-out `LEFT JOIN` fallback is included for engines that lack `EXCEPT`/`MINUS`.

Three design choices were deliberate. First, **string templating over an ORM** (e.g., SQLAlchemy): the generator's logic is essentially template substitution and benefits from readable, transparent SQL output that QA engineers can audit. Second, **CTE-based formatting** rather than nested subqueries: the intermediate `source_transformed` alias makes the transformation logic explicit and the generated SQL human-readable. Third, **bidirectional checks by default**: the manual workflow frequently runs only one direction and silently misses extra rows on the other side; making both directions automatic raises the detection floor without operator effort.

The Flask UI (`app.py`) exposes the same engine via a browser, accepting an uploaded CSV or Excel mapping file and table names and returning the generated SQL in a copyable text panel. The CLI driver (`example_usage.py`) accepts the same inputs as positional arguments, making the tool scriptable inside CI workflows where mapping changes in version control trigger automated regeneration of the validation suite. The repository also ships companion utilities for automated ETL test-case generation, an interactive SQL playground for ad hoc query experimentation, and optional AI assistance for transformation suggestions and natural-language mapping bootstrapping. These adjunct features sit outside the paper's main evaluation but share the same parser and validation abstractions.

On a typical 9-row mapping with mixed transformations, the generator emits two ~50-line SQL queries in sub-second time. Throughput exceeds 100 mapping conversions per hour for large mapping files — comparable to the ~200 mappings/hour figure reported for QuerySurge AI's commercial implementation [@QuerySurge:2024].

# Research impact statement

Functional correctness was evaluated on a mix of simple and complex mapping files of varying sizes. In every case, the generated SQL ran without syntax errors against PostgreSQL and matched the queries an experienced developer would write manually for the same mapping. The tool therefore produces validation logic that is operationally interchangeable with hand-coded SQL for the mapping patterns it supports.

The expected efficiency gain is substantial. Industry benchmarks place manual mapping-to-SQL effort at approximately one hour per mapping, so the QuerySurge-reported "1,000 mappings in 5 hours vs. 1,000 hours manually" speedup [@QuerySurge:2024] is the realistic target ratio. Our timing tests, while not a formal user study, are consistent with this two-orders-of-magnitude improvement.

Real-world relevance was confirmed through informal feedback from data engineers, who noted that the tool addresses an existing bottleneck rather than imposing a new authoring format. Because mapping spreadsheets already exist in most ETL projects, adoption requires no upstream workflow change. The bidirectional default also surfaces classes of defect — extra rows on either side, silent transformation regressions — that single-direction manual checks routinely miss.

**Limitations.** We have not conducted a large-scale quantitative user study or a head-to-head benchmark against commercial tools; the evaluation rests on functional verification, timing on representative mappings, and practitioner feedback. The parser assumes a well-formed mapping document and treats unstructured free-text business rules as opaque, requiring human intervention for non-standard transformations. Database-specific functions (e.g., Snowflake `TO_DATE`, Oracle date syntax) require manual adjustment of the generated SQL. Complex multi-table joins beyond simple key relationships, recursive logic, and procedural transformations fall outside the current scope.

**Availability and reproducibility.** The source code, example mapping files, and deployment configuration (Dockerfile, `render.yaml`) are available on GitHub at <https://github.com/hkrishnan62/ETL_Parser> under the MIT licence. A live web instance runs on Render at <https://etl-mapping-converter-to-sql.onrender.com>. A reproducibility package containing sample output queries and tool screenshots is archived on Zenodo [@Zenodo:2025].

**Future directions.** Planned extensions include LLM-assisted interpretation of free-form mapping descriptions for cases where business rules are documented in natural language [@Singamsetty:2025], pluggable SQL-dialect support (PostgreSQL, Oracle, Hive, Snowflake), incremental/watermark-based testing for near-real-time pipelines, native CI/CD connectors for Jenkins and GitHub Actions, and a syntax-highlighted web UI with execution previews.

# AI usage disclosure

OpenAI's ChatGPT was used to assist with sentence phrasing, language refinement, and grammar polishing during preparation of this manuscript. All ideas, analyses, system design decisions, and technical contributions are solely the author's own. AI-assisted manuscript text was reviewed and edited by the author for accuracy and faithfulness to the underlying technical work.

# Acknowledgements

The author thanks the data engineering practitioners whose informal feedback during interviews helped shape the practical relevance of this work. No external funding or institutional support was received for this research, and the author declares no competing interests.

# References
