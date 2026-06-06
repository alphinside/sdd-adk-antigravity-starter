# Data Model: Table Reservation System

## Entities

### `reservations`

Stores the details of each customer table reservation.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `SERIAL` | `PRIMARY KEY` | Unique identifier for each reservation. |
| `customer_name` | `VARCHAR(255)` | `NOT NULL` | The name of the customer making the booking. |
| `email` | `VARCHAR(255)` | `NOT NULL` | Contact email address. |
| `phone` | `VARCHAR(50)` | `NOT NULL` | Contact phone number. |
| `party_size` | `INTEGER` | `NOT NULL` | Number of guests in the booking. Must be $\ge 1$ and $\le 20$. |
| `reservation_date` | `DATE` | `NOT NULL` | The date of the reservation. |
| `reservation_time` | `TIME` | `NOT NULL` | The time slot of the reservation. |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | The timestamp when the record was created. |

## Validation Rules

1. **Party Size**:
   - Must be an integer.
   - Must be greater than or equal to 1.
   - Must be less than or equal to 20 (maximum table size).
2. **Contact Info**:
   - `email` must be a valid email format.
   - `phone` must not be empty and should match standard phone formats.
3. **Reservation Date & Time**:
   - Must be in the future relative to the booking execution timestamp.
4. **Seating Capacity Limit**:
   - The total sum of `party_size` for all reservations on a given `reservation_date` and `reservation_time` must not exceed **40**.
