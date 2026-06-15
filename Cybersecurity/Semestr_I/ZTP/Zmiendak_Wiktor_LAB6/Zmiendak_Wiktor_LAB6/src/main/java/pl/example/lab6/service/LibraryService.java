package pl.example.lab6.service;

import pl.example.lab6.dto.BookForm;
import pl.example.lab6.dto.LoanForm;
import pl.example.lab6.model.Book;
import pl.example.lab6.view.BookListItem;
import pl.example.lab6.view.DashboardView;
import pl.example.lab6.view.LoanListItem;

import java.util.List;

public interface LibraryService {

    List<BookListItem> getBooks();

    Book createBook(BookForm form);

    Book getBook(long bookId);

    void createLoan(LoanForm form);

    List<LoanListItem> getLoans(boolean activeOnly);

    void returnLoan(long loanId);

    DashboardView getDashboard();
}
