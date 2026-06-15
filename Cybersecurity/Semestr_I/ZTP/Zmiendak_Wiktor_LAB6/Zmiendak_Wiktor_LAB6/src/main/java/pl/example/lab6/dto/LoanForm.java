package pl.example.lab6.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class LoanForm {

    @NotNull(message = "Book id is required")
    private Long bookId;

    @NotBlank(message = "Borrower is required")
    private String borrower;

    public LoanForm() {
    }

    public LoanForm(Long bookId, String borrower) {
        this.bookId = bookId;
        this.borrower = borrower;
    }

    public Long getBookId() {
        return bookId;
    }

    public void setBookId(Long bookId) {
        this.bookId = bookId;
    }

    public String getBorrower() {
        return borrower;
    }

    public void setBorrower(String borrower) {
        this.borrower = borrower;
    }
}
