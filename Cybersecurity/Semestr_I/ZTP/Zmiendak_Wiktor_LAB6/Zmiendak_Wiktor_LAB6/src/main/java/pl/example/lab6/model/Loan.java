package pl.example.lab6.model;

import java.time.LocalDate;

public class Loan {

    private Long id;
    private Long bookId;
    private String borrower;
    private LocalDate borrowedOn;
    private LocalDate dueDate;
    private boolean returned;

    public Loan() {
    }

    public Loan(Long id, Long bookId, String borrower, LocalDate borrowedOn, LocalDate dueDate, boolean returned) {
        this.id = id;
        this.bookId = bookId;
        this.borrower = borrower;
        this.borrowedOn = borrowedOn;
        this.dueDate = dueDate;
        this.returned = returned;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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

    public LocalDate getBorrowedOn() {
        return borrowedOn;
    }

    public void setBorrowedOn(LocalDate borrowedOn) {
        this.borrowedOn = borrowedOn;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }

    public boolean isReturned() {
        return returned;
    }

    public void setReturned(boolean returned) {
        this.returned = returned;
    }
}
