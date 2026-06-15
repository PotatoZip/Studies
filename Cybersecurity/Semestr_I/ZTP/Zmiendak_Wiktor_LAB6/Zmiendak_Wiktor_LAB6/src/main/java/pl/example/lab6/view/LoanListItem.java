package pl.example.lab6.view;

import java.time.LocalDate;

public record LoanListItem(
        Long id,
        Long bookId,
        String bookTitle,
        String borrower,
        LocalDate borrowedOn,
        LocalDate dueDate,
        boolean returned
) {
}
