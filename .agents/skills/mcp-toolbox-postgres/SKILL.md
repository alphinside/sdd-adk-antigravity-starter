# TODO(codelab): Add YAML frontmatter above this line to activate the skill.
# Antigravity requires ---/name/description/--- to recognize a skill file.

# MCP Toolbox for PostgreSQL Configuration

Reference skill for configuring the MCP Toolbox with PostgreSQL databases.
All config goes into a single `tools.yaml` file using `---` document separators between entries.

---

## 1. Sources

A **Source** is a database connection pool. Define with `kind: source`.

### PostgreSQL Source (standalone / self-hosted)

```yaml
kind: source
name: my-pg-source
type: postgres
host: 127.0.0.1
port: 5432
database: my_db
user: ${USER_NAME}
password: ${PASSWORD}
```

### Cloud SQL PostgreSQL Source (managed)

```yaml
kind: source
name: my-cloud-sql-source
type: cloud-sql-postgres
project: my-project-id
region: us-central1
instance: my-instance-name
database: my_db
user: ${USER_NAME}
password: ${PASSWORD}
```

### PostgreSQL Source Reference

| field         | type               | required | description                                                                 |
|---------------|:------------------:|:--------:|-----------------------------------------------------------------------------|
| type          | string             | true     | Must be `"postgres"` (standalone) or `"cloud-sql-postgres"` (Cloud SQL).    |
| host          | string             | true     | IP address to connect to (e.g. `"127.0.0.1"`). Only for `postgres` type.   |
| port          | string             | true     | Port to connect to (e.g. `"5432"`). Only for `postgres` type.              |
| project       | string             | true     | GCP project ID. Only for `cloud-sql-postgres` type.                         |
| region        | string             | true     | GCP region. Only for `cloud-sql-postgres` type.                             |
| instance      | string             | true     | Cloud SQL instance name. Only for `cloud-sql-postgres` type.                |
| database      | string             | true     | Name of the Postgres database to connect to.                                |
| user          | string             | true     | Name of the Postgres user to connect as.                                    |
| password      | string             | true     | Password of the Postgres user.                                              |
| queryParams   | map[string]string   | false    | Raw query to be added to the db connection string.                          |
| queryExecMode | string             | false    | pgx query exec mode: `cache_statement` (default), `cache_describe`, `describe_exec`, `exec`, `simple_protocol`. |

> **Tip:** Use `${ENV_NAME}` for secrets instead of hardcoding.

---

## 2. Tools

A **Tool** is an action the agent can take (e.g., run SQL). Define with `kind: tool`.

### Basic Tool Structure

```yaml
kind: tool
name: search_flights_by_number
type: postgres-sql
source: my-pg-instance         # references a source name
statement: |
  SELECT * FROM flights
  WHERE airline = $1
  AND flight_number = $2
  LIMIT 10
description: |
  Use this tool to get information for a specific flight.
  Takes an airline code and flight number and returns info on the flight.
parameters:
  - name: airline
    type: string
    description: Airline unique 2 letter identifier
  - name: flight_number
    type: string
    description: 1 to 4 digit number
```

### Parameter Types

Basic types: `string`, `integer`, `float`, `boolean`, `array`, `map`.

| field          | type             | required | description                                                       |
|----------------|:----------------:|:--------:|-------------------------------------------------------------------|
| name           | string           | true     | Name of the parameter.                                            |
| type           | string           | true     | One of `"string"`, `"integer"`, `"float"`, `"boolean"`, `"array"`, `"map"` |
| description    | string           | true     | Natural language description for the agent.                       |
| default        | parameter type   | false    | Default value. If provided, `required` becomes `false`.           |
| required       | bool             | false    | Whether required. Defaults to `true`.                             |
| allowedValues  | []string         | false    | Restrict input. Supports regex.                                   |
| excludedValues | []string         | false    | Exclude input. Supports regex.                                    |
| escape         | string           | false    | String only. Escaping delimiters: `single-quotes`, `double-quotes`, `backticks`, `square-brackets`. |
| minValue       | int/float        | false    | Integer/float only. Minimum value allowed.                        |
| maxValue       | int/float        | false    | Integer/float only. Maximum value allowed.                        |

### Array Parameters

```yaml
parameters:
  - name: preferred_airlines
    type: array
    description: A list of airlines, ordered by preference.
    items:
      name: name
      type: string
      description: Name of the airline.
```

### Map Parameters

```yaml
# Generic map (mixed value types)
parameters:
  - name: execution_context
    type: map
    description: A flexible set of key-value pairs.

# Typed map (enforced value type)
parameters:
  - name: user_scores
    type: map
    description: User IDs to scores.
    valueType: integer
```

### Template Parameters (Dynamic SQL)

Use `templateParameters` for dynamic identifiers (table/column names).

> **Warning:** Template parameters are prone to SQL injection. Always use `allowedValues` or `escape` to restrict inputs. Prefer basic `parameters` when possible.

```yaml
kind: tool
name: select_columns_from_table
type: postgres-sql
source: my-pg-instance
statement: |
  SELECT {{array .columnNames}} FROM {{.tableName}}
description: |
  Use this tool to list all information from a specific table.
templateParameters:
  - name: tableName
    type: string
    description: Table to select from
  - name: columnNames
    type: array
    description: The columns to select
    items:
      name: column
      type: string
      description: Name of a column to select
      escape: double-quotes
```

### Tool Annotations (MCP metadata)

```yaml
kind: tool
name: my_query_tool
type: postgres-sql
source: my-pg-source
description: Read-only query tool
annotations:
  readOnlyHint: true       # default: false — tool only reads data
  destructiveHint: false   # default: true  — tool may create/update/delete
  idempotentHint: true     # default: false — repeated calls have no additional effect
  openWorldHint: false     # default: true  — tool interacts with external entities
```

### Authorized Invocations

```yaml
kind: tool
name: search_all_flights
type: postgres-sql
source: my-pg-instance
statement: |
  SELECT * FROM flights
authRequired:
  - my-google-auth
```

---

## 3. Embedding Models

An **EmbeddingModel** converts text into vector embeddings for semantic search. Define with `kind: embeddingModel`.

### Gemini Embedding (Google AI — API Key)

```yaml
kind: embeddingModel
name: gemini-model
type: gemini
model: gemini-embedding-001
apiKey: ${GOOGLE_API_KEY}
dimension: 768
```

### Gemini Embedding (Vertex AI — ADC)

```yaml
kind: embeddingModel
name: gemini-model
type: gemini
model: gemini-embedding-001
project: ${GOOGLE_CLOUD_PROJECT}
location: us-central1
dimension: 768
```

### Gemini Embedding Reference

| field     | type    | required | description                                            |
|-----------|:-------:|:--------:|--------------------------------------------------------|
| type      | string  | true     | Must be `gemini`.                                      |
| model     | string  | true     | Gemini model ID (e.g., `gemini-embedding-001`).        |
| dimension | integer | false    | Output vector dimensions (e.g., `768`). Must match DB column. |
| apiKey    | string  | false    | Google AI API key (uses Google AI Studio backend).     |
| project   | string  | false    | GCP project (uses Vertex AI with ADC).                 |
| location  | string  | false    | GCP location for Vertex AI (e.g., `us-central1`).     |

> Authentication priority: If `apiKey` is set → Google AI. If `project`+`location` are set → Vertex AI with ADC.

### Using Embeddings in Tools

Use the `embeddedBy` field on a parameter to auto-vectorize input:

```yaml
# Semantic search tool
kind: tool
name: search_embedding
type: postgres-sql
source: my-pg-instance
description: Search for documents by meaning.
statement: |
  SELECT id, content, embedding <-> $1 AS distance
  FROM documents
  ORDER BY distance LIMIT 5
parameters:
  - name: semantic_search_string
    type: string
    description: The search query that will be converted to a vector.
    embeddedBy: gemini-model    # references the embeddingModel name
```

### Hidden Parameter Duplication (`valueFromParam`)

For vector ingestion, avoid asking the LLM to duplicate input. Use `valueFromParam` to auto-copy:

```yaml
kind: tool
name: insert_embedding
type: postgres-sql
source: my-pg-instance
description: Insert a new document into the database.
statement: |
  INSERT INTO documents (content, embedding)
  VALUES ($1, $2);
parameters:
  - name: content
    type: string
    description: The raw text content to be stored.
  - name: vector_string
    type: string
    valueFromParam: content      # hidden from LLM, auto-copies from 'content'
    embeddedBy: gemini-model     # auto-vectorizes the copied value
```

---

## 4. Complete Example (`tools.yaml`)

```yaml
kind: embeddingModel
name: my-gemini-embedder
type: gemini
model: gemini-embedding-001
apiKey: ${GOOGLE_API_KEY}
dimension: 768

---

kind: source
name: restaurant-db
type: cloud-sql-postgres
project: ${GOOGLE_CLOUD_PROJECT}
region: ${REGION}
instance: restaurant-db
database: restaurant_db
user: postgres
password: ${DB_PASSWORD}

---

kind: tool
name: search_menu
type: postgres-sql
source: restaurant-db
description: >
  Search menu items by keyword matching against name, category, or description.
statement: |
  SELECT name, category, description, price, dietary_tags
  FROM menu_items
  WHERE name ILIKE '%' || $1 || '%'
      OR category ILIKE '%' || $1 || '%'
      OR description ILIKE '%' || $1 || '%'
  LIMIT 10
parameters:
  - name: query
    type: string
    description: Search term for menu items.

---

kind: tool
name: semantic_search_menu
type: postgres-sql
source: restaurant-db
description: >
  Search menu items using semantic similarity via embeddings.
statement: |
  SELECT name, category, description, price, dietary_tags,
         1 - (embedding <=> $1::vector) AS similarity
  FROM menu_items
  WHERE embedding IS NOT NULL
  ORDER BY embedding <=> $1::vector
  LIMIT 5
parameters:
  - name: query
    type: string
    description: Natural language description of the type of food.
    embeddedBy: my-gemini-embedder
```

---

## 5. Key Patterns & Tips

1. **Separate documents with `---`** in `tools.yaml`.
2. **Use `${ENV_NAME}`** for all secrets and project-specific values.
3. **`embeddedBy`** on a parameter auto-vectorizes the input before query execution.
4. **`valueFromParam`** hides a parameter from the LLM and auto-copies from another parameter.
5. **Parameter `$1`, `$2`** are positional — they bind in the order parameters are listed.
6. **`type: postgres-sql`** is the tool type for all PostgreSQL query tools.
7. **Annotations** provide hints to MCP clients about tool behavior (read-only, destructive, etc.).
