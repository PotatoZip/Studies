package pl.example.lab6.service;

import org.springframework.stereotype.Component;
import pl.example.lab6.model.Book;
import pl.example.lab6.model.Loan;
import pl.example.lab6.view.BookListItem;
import pl.example.lab6.view.LoanListItem;

@Component
public class LibraryViewMapper {

    public BookListItem toBookListItem(Book book) {
        return new BookListItem(
                book.getId(),
                book.getTitle(),
                book.getAuthor(),
                book.getTotalCopies(),
                book.getAvailableCopies(),
                book.getAvailableCopies() > 0);
    }

    public LoanListItem toLoanListItem(Loan loan, Book book) {
        return new LoanListItem(
                loan.getId(),
                loan.getBookId(),
                book.getTitle(),
                loan.getBorrower(),
                loan.getBorrowedOn(),
                loan.getDueDate(),
                loan.isReturned());
    }
}
