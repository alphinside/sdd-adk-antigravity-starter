# Feature Specification: Table Reservation System

**Feature Branch**: `001-table-reservation-api`  
**Created**: 2026-06-06  
**Status**: Draft  
**Input**: User description: "Create a backend API with FastAPI for a table reservation system. Endpoints needed: (1) Create a reservation (POST /reservations), (2) List all reservations (GET /reservations). Use PostgreSQL for data storage. Include BDD scenarios for: submitting a valid reservation, attempting to book a fully booked slot, and listing existing reservations."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Table Reservation (Priority: P1)

As a restaurant customer, I want to book a table for a specific date, time, and number of guests, so that I can secure a spot for dining.

**Why this priority**: This is the core functionality of the system. Without booking capability, the system has no utility.

**Independent Test**: Can be fully tested by submitting a booking request for an available slot and verifying that a confirmation is received.

**Acceptance Scenarios**:

1. **Given** the restaurant has available capacity for 4 guests on 2026-06-10 at 19:00, **When** the customer submits a reservation with their name, email, and phone number, **Then** the reservation is successfully confirmed and a reservation ID is returned.
2. **Given** the customer attempts to make a reservation, **When** the requested date or time is in the past, **Then** the reservation is rejected with an error message.
3. **Given** the customer attempts to make a reservation, **When** the party size is invalid (less than 1 or greater than the maximum allowed table size of 20), **Then** the reservation is rejected with a validation error.

---

### User Story 2 - Prevent Overbooking (Priority: P2)

As a restaurant owner, I want the system to reject reservations that exceed the restaurant's seating capacity for a given time slot, so that we do not overbook our venue.

**Why this priority**: Overbooking leads to a poor customer experience and operational issues for the restaurant staff.

**Independent Test**: Can be tested by filling all available capacity for a specific time slot, attempting to book one additional guest, and verifying that the system rejects the booking.

**Acceptance Scenarios**:

1. **Given** the restaurant's capacity is fully booked for 2026-06-10 at 19:00, **When** a customer attempts to book a table for 2 guests for that same slot, **Then** the booking is rejected and the user is notified that the slot is fully booked.

---

### User Story 3 - List Reservations (Priority: P3)

As a restaurant staff member, I want to view a list of all existing reservations, so that I can manage seating and prepare for arriving guests.

**Why this priority**: Crucial for restaurant operations, enabling staff to plan their shift and welcome customers.

**Independent Test**: Can be tested by creating two separate reservations, requesting the reservation list, and verifying that both reservations are returned.

**Acceptance Scenarios**:

1. **Given** there are active reservations in the system, **When** a staff member requests the list of all reservations, **Then** they receive a complete list of those reservations including guest details, party size, and slot times.
2. **Given** there are no reservations in the system, **When** a staff member requests the list of all reservations, **Then** they receive an empty list.

---

### Edge Cases

- **Concurrent Booking Requests**: Two customers attempt to book the final available table at the exact same moment. One request must succeed and the other must be gracefully rejected due to lack of capacity.
- **Out of Range Date**: Attempting to book a table too far in the future (e.g., more than 1 year in advance) should be restricted or handled gracefully.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow customers to submit reservation requests including customer name, email, phone number, party size, date, and time.
- **FR-002**: The system MUST validate all input parameters: party size must be a positive integer, email and phone number must be in correct formats, and the date/time must be in the future.
- **FR-003**: The system MUST enforce venue capacity limits by only confirming a reservation if the requested party size does not exceed the remaining capacity for the given slot. Capacity is defined as a static total seating capacity configured globally for any active reservation slot (e.g., maximum 40 seats).
- **FR-004**: The system MUST allow retrieving all recorded reservations.
- **FR-005**: The system MUST handle concurrent reservation requests safely, ensuring capacity limits are never exceeded.
- **FR-006**: The system MUST authenticate list retrieval requests using a simple pre-shared token/API key. Customer reservation requests (POST /reservations) do not require authentication.

### Key Entities *(include if feature involves data)*

- **Reservation**: Represents a booking made by a customer.
  - Attributes: Reservation ID (unique identifier), Customer Name, Email, Phone Number, Party Size, Date, Time, Status (e.g., Confirmed, Cancelled).
- **Time Slot Capacity**: Tracks the maximum and remaining capacity for a specific date and time.
  - Attributes: Date, Time, Max Capacity, Remaining Capacity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Customers can complete and submit a table reservation request in under 5 seconds.
- **SC-002**: Staff can retrieve the list of all reservations in under 1 second.
- **SC-003**: The system maintains 100% data consistency, permitting zero overbookings even during high concurrent traffic (e.g., 50 parallel requests).
- **SC-004**: 100% of invalid inputs (past dates, negative party size, invalid emails) are rejected with clear error messages.
