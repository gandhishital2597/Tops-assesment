# Section A: Conceptual Understanding — Answers

### 1. Why REST APIs are preferred for mobile and frontend-heavy apps

- **Decoupling:** The backend (Django) and frontend (React, mobile app, etc.) evolve independently. The same API can serve a web app, an iOS app, and an Android app simultaneously.
- **Stateless & lightweight:** REST uses JSON over HTTP, which is far lighter than server-rendered HTML — important on mobile networks with limited bandwidth/battery.
- **Cacheable:** GET requests can be cached at the HTTP layer (browser, CDN, proxy), improving performance for repeated reads like "list all doctors."
- **Standardized:** Reuses HTTP verbs (GET/POST/PUT/DELETE) and status codes, so any client (Postman, mobile SDK, JS fetch) can talk to it without custom protocols.
- **Scalability:** Stateless requests mean any server in a load-balanced cluster can handle any request — no server-side session affinity needed.

### 2. Serializers as a validation layer + field-level validation

DRF serializers do two jobs: (1) convert between Python/Django model instances and JSON (serialization/deserialization), and (2) **validate** incoming data before it ever touches the database — similar to Django Forms.

Validation happens in layers, checked in this order:
1. **Field-level validators** (e.g., `max_length`, `required`) defined on the field itself.
2. **`validate_<field_name>` methods** — custom per-field validation.
3. **`validate(self, data)`** — object-level validation across multiple fields.

Example of custom field-level validation:

```python
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'city']

    def validate_name(self, value):
        if any(ch.isdigit() for ch in value):
            raise serializers.ValidationError("Name cannot contain digits.")
        return value.strip()
```

If validation fails, `serializer.is_valid()` returns `False` and `serializer.errors` contains a clear, field-mapped error dict — DRF automatically turns this into a `400 Bad Request` response.

### 3. Importance of correct HTTP status codes (201 vs 200)

- **200 OK** means "the request succeeded and here's existing/updated data" — used for successful GET, and often PUT/PATCH.
- **201 Created** specifically means "a *new* resource was created" — used after a successful POST. DRF's `CreateModelMixin` returns this automatically along with a `Location` header pointing to the new resource (when applicable).

Why it matters:
- **Client automation:** Frontend code branches on status code (`if (response.status === 201) showSuccessToast()`), not on parsing the body — wrong codes break this logic silently.
- **Semantic clarity / debugging:** A 200 on a failed creation, or a 201 on a GET, misleads anyone debugging the API or building monitoring/alerting around it.
- **HTTP spec compliance:** Tools like Postman, API gateways, and caching layers behave differently based on status codes (e.g., caching is normally only valid for 200, not 201).

### 4. Why pagination is required when listing doctors

- **Database performance:** Without pagination, `Doctor.objects.all()` executes a query that pulls *every row* and serializes *all of them* into one JSON response. As the table grows from hundreds to millions of rows, this becomes a full table scan with no `LIMIT`, consuming memory and CPU on both DB and app server.
- **Network/response time:** Sending 100,000 doctor records in one response is slow to transmit and slow for the client to parse/render.
- **Predictable load:** Pagination (`LIMIT`/`OFFSET` under the hood) keeps each query's cost roughly constant regardless of table size, since the DB only needs to fetch a bounded page of rows (especially efficient with an index on the ordering column).
- **Better UX:** Clients can request data incrementally (infinite scroll, "Next" button) instead of waiting for a giant payload.

### 5. Benefits of ViewSets over APIView for rapid CRUD development

| | `APIView` | `ViewSet` (e.g. `ModelViewSet`) |
|---|---|---|
| CRUD logic | You manually write `get`, `post`, `put`, `delete` methods | Inherited automatically (`list`, `retrieve`, `create`, `update`, `destroy`) |
| URLs | You manually write each `path()` | `DefaultRouter` auto-generates all URLs from one `register()` call |
| Boilerplate | High — repeated queryset/serializer logic per view | Minimal — just set `queryset` and `serializer_class` |
| Consistency | Easy to diverge from REST conventions across views | Enforces consistent REST patterns project-wide |

For a standard CRUD resource like "Doctor," `ModelViewSet` + `DefaultRouter` gets you a fully working `GET/POST/PUT/PATCH/DELETE` API in ~10 lines, versus 40-60 lines of repetitive `APIView` code.

### 6. Atomic Transactions (`transaction.atomic`) for data integrity

`transaction.atomic()` wraps a block of database operations so they execute as a single, indivisible unit: either **all** succeed and commit, or if **any** exception is raised, **all** changes in that block are rolled back — nothing partial is saved.

Why it matters for creating related doctor records: imagine creating a `Doctor` and then, in the same request, creating a related `Clinic` or `Availability` record. If the doctor saves successfully but the related record creation throws an error (e.g., a validation failure or DB constraint), you'd be left with an "orphan" doctor record with no associated data — corrupting referential integrity. Wrapping both writes in `transaction.atomic()` guarantees the doctor row is rolled back too, so the database never reflects a half-finished operation.

```python
def perform_create(self, serializer):
    with transaction.atomic():
        serializer.save()
```
